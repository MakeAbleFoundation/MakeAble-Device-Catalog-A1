#!/usr/bin/env python3
"""Convert the P1S catalogue's 3mf projects to the Bambu Lab A1, keeping every plate as laid out.

  a1.py convert <file.3mf> [...]    rewrite each file in place (skips files already on the A1)
  a1.py fit <out.json> <file.3mf> [...]
                                    slice each converted full plate with Orca; trim any that run
                                    past the 14 h cap (copies nearest the middle stay) and rename
  a1.py check <repo> <out.json>     every 3mf against its P1S original (upstream/main)
  a1.py data <repo>                 fold the A1 slices into Validation/data for the reports
  a1.py previews <repo>             redraw the plate previews from the files
  a1.py brims                       list the parts that get a bed-slinger brim
  a1.py preset <out.json>           write the `PETG A1 Tuned` user preset for Bambu Studio

The rule is the same one settings.build uses for the P1S, applied P1S -> A1:
  1. machine keys            -> always the A1 system preset (bed, kinematics, start G-code,
                                no excluded corner)
  2. process keys            -> a value still equal to the X1C system preset (the P1S uses the
                                X1C process presets) moves to the A1 sibling preset; any other
                                value was a choice (the designer's, or a catalogue override)
                                and stays. Same for the per-object settings baked into
                                model_settings.config.
  3. filament keys           -> per slot, a value still equal to the old filament preset moves
                                to the A1 one; a hand-set value stays
  4. bed-slinger brim        -> parts that are tall for their footprint get an outer brim,
                                unless the designer set the brim themselves (see BRIM_*)
Meshes, positions, plates, thumbnails and the designer's pictures are copied untouched.
"""
import json, os, re, sys, zipfile
from resolve_preset import resolve
from settings import META_KEYS, coerce, norm, preset_keys, same

OLD_MACHINE, NEW_MACHINE = "Bambu Lab P1S 0.4 nozzle", "Bambu Lab A1 0.4 nozzle"
OLD_SUFFIX, NEW_SUFFIX = " @BBL X1C", " @BBL A1"

# The user's own PETG tuning (Bambu Studio user preset `PETG P1S Tuned`, which inherits
# `Bambu PETG Basic @BBL X1C`), carried over onto the A1's PETG Basic as `PETG A1 Tuned`.
PETG_TUNED = {
    "fan_max_speed": ["65"], "fan_min_speed": ["20"],
    "filament_max_volumetric_speed": ["8"],
    "filament_retract_before_wipe": ["70%"], "filament_retraction_length": ["1.6"],
    "filament_retraction_speed": ["40"], "filament_wipe_distance": ["2"],
    "filament_z_hop": ["0.4"], "filament_z_hop_types": ["Normal Lift"],
    "nozzle_temperature": ["240"], "nozzle_temperature_initial_layer": ["250"],
    "textured_plate_temp": ["60"], "textured_plate_temp_initial_layer": ["65"],
}
PETG_OLD, PETG_NEW = "PETG P1S Tuned", "PETG A1 Tuned"
FILAMENTS = {  # old preset -> (new preset, the system preset each one is built on)
    "Bambu PLA Basic @BBL X1C": ("Bambu PLA Basic @BBL A1", None),
    PETG_OLD: (PETG_NEW, "Bambu PETG Basic @BBL A1"),
}
FILAMENT_BASE_OLD = {PETG_OLD: "Bambu PETG Basic @BBL X1C"}

# The A1 moves the bed under the part, so a part that is tall for its footprint can rock
# loose. Added only where the brim is still on the slicer's `auto_brim` default and the
# designer did not pick a brim themselves; anything they set (KeyWings' deliberate no_brim,
# the cup holder's painted ears) is left alone.
BRIM_SLENDER = 2.3         # height / narrowest footprint width
BRIM_TALL = (60.0, 1.5)    # or: at least this tall (mm) and this slender
BRIM_WIDTH = "5"

HERE = os.path.dirname(os.path.abspath(__file__))


def tuned(base, overrides):
    d = preset_keys(resolve("filament", base))
    d.update(overrides)
    return d


_FIL = {}


def filament(name):
    """Effective keys of a filament preset, old or new, without needing the user folder."""
    if name not in _FIL:
        if name == PETG_OLD:
            _FIL[name] = tuned(FILAMENT_BASE_OLD[name], PETG_TUNED)
        elif name == PETG_NEW:
            _FIL[name] = tuned(FILAMENTS[PETG_OLD][1], PETG_TUNED)
        else:
            _FIL[name] = preset_keys(resolve("filament", name))
    return _FIL[name]


def filament_system_parent(name):
    return FILAMENTS[PETG_OLD][1] if name == PETG_NEW else name


def process_pair(old_name):
    if not old_name.endswith(OLD_SUFFIX):
        raise ValueError(f"unexpected process preset {old_name!r}")
    new_name = old_name[:-len(OLD_SUFFIX)] + NEW_SUFFIX
    return (preset_keys(resolve("process", old_name)), preset_keys(resolve("process", new_name)),
            new_name, resolve("process", new_name))


def moved_keys(old, new):
    """Keys where the two system presets disagree: the only ones the conversion may touch."""
    return sorted(k for k in set(old) | set(new) if not same(old.get(k), new.get(k), k))


def _chunks(v, n):
    per = max(1, len(v) // n)
    return [v[i * per:(i + 1) * per] for i in range(n)], per


def convert_project(cfg, protect=()):
    """Return (new cfg, log). `protect` = keys the designer set on purpose: never moved."""
    log = dict(machine=0, process={}, process_kept={}, filament={}, filament_kept={})
    out = dict(cfg)
    if out.get("printer_settings_id") != OLD_MACHINE:
        raise ValueError(f"not a P1S project: {out.get('printer_settings_id')}")

    # 1. machine
    old_m = preset_keys(resolve("machine", OLD_MACHINE))
    new_m = preset_keys(resolve("machine", NEW_MACHINE))
    for k in set(old_m) - set(new_m):
        if k in out and same(out[k], old_m[k], k):
            out.pop(k)
    for k, v in new_m.items():
        if k not in out or not same(out[k], v, k):
            log["machine"] += 1
        out[k] = v
    out["printer_settings_id"] = NEW_MACHINE
    out["upward_compatible_machine"] = list(
        resolve("machine", NEW_MACHINE).get("upward_compatible_machine") or [])

    # 2. process
    old_p, new_p, new_name, new_full = process_pair(out["print_settings_id"])
    for k in moved_keys(old_p, new_p):
        if k not in out or k not in new_p:
            continue
        cur = out[k]
        at_default = k in old_p and (same(cur, old_p[k], k) or same(coerce(old_p[k], cur), cur, k))
        if at_default and k not in protect:
            out[k] = coerce(new_p[k], cur)
            log["process"][k] = (norm(cur)[0], norm(out[k])[0])
        else:
            log["process_kept"][k] = norm(cur)[0]
    out["print_settings_id"] = new_name
    if new_full.get("compatible_printers"):
        out["print_compatible_printers"] = list(new_full["compatible_printers"])

    # 3. filaments, slot by slot
    olds = list(out["filament_settings_id"])
    news = [FILAMENTS[o][0] for o in olds]
    n = len(olds)
    keys = set()
    for o, w in zip(olds, news):
        keys |= set(filament(o)) | set(filament(w))
    keys -= META_KEYS
    for k in sorted(keys):
        cur = out.get(k)
        if cur is None:
            vals = [filament(w).get(k) for w in news]
            if all(v is not None for v in vals):
                out[k] = [norm(v)[0] for v in vals]
                log["filament"][k] = ("-", out[k][0])
            continue
        if not isinstance(cur, list) or len(cur) % n:
            continue          # a per-extruder or print-level key that filament presets also carry
        chunks, per = _chunks([str(x) for x in cur], n)
        new_v = []
        for c, o, w in zip(chunks, olds, news):
            ov, nv = filament(o).get(k), filament(w).get(k)
            if nv is None:
                new_v += c
                continue
            nv = norm(nv)
            nv = nv[:per] if len(nv) >= per else nv * per
            if ov is None or same(c, (norm(ov) * per)[:per] if len(norm(ov)) < per else norm(ov)[:per], k):
                if not same(c, nv, k):
                    log["filament"][k] = (c[0], nv[0])
                new_v += nv
            else:
                if not same(c, nv, k):
                    log["filament_kept"][k] = c[0]
                new_v += c
        out[k] = new_v
    out["filament_settings_id"] = news
    out["filament_ids"] = [str(resolve("filament", filament_system_parent(w)).get("filament_id")
                               or "") for w in news]
    out["default_filament_profile"] = ["Bambu PLA Basic @BBL A1"]
    out["default_print_profile"] = "0.20mm Standard @BBL A1"

    # what differs from the system presets now, as Studio records it
    pkeys = sorted(k for k in new_p if k in out and k not in keys
                   and not same(out[k], new_p[k], k)
                   and not same(coerce(new_p[k], out[k]), out[k], k))
    fdiff = []
    for i, w in enumerate(news):
        sysp = filament(filament_system_parent(w))
        fdiff.append(";".join(sorted(k for k, v in filament(w).items()
                                     if k in sysp and not same(v, sysp[k], k))))
    out["different_settings_to_system"] = [";".join(pkeys)] + fdiff + [""]
    return out, log


META_RE = re.compile(r'(<metadata key="([^"]+)" value=")([^"]*)("\s*/>)')


def convert_model_settings(xml, process_old, process_new, brim_names=()):
    """Per-object/per-part baked settings: X1C defaults -> A1 defaults; brims for `brim_names`."""
    moved = {k for k in moved_keys(process_old, process_new) if k in process_new}
    log = dict(objects=0, brims=[])

    def sub(m):
        k, v = m.group(2), m.group(3)
        if k in moved and k in process_old and same(v, norm(process_old[k])[0], k):
            log["objects"] += 1
            return m.group(1) + norm(process_new[k])[0] + m.group(4)
        return m.group(0)

    xml = META_RE.sub(sub, xml)
    if not brim_names:
        return xml, log

    def obj(m):
        block = m.group(0)
        head = block.split("<part", 1)[0]
        name = re.search(r'<metadata key="name" value="([^"]*)"', head)
        if not name or name.group(1) not in brim_names:
            return block
        bt = re.search(r'<metadata key="brim_type" value="([^"]*)"', head)
        if bt and bt.group(1) != "auto_brim":
            return block
        rest = block[len(head):]
        for k, v in (("brim_type", "outer_only"), ("brim_width", BRIM_WIDTH)):
            pat = re.compile(r'(<metadata key="%s" value=")[^"]*(")' % k)
            if pat.search(head):
                head = pat.sub(r"\g<1>%s\g<2>" % v, head, count=1)
            else:
                head = re.sub(r'(<object id="\d+">\n)',
                              r'\1    <metadata key="%s" value="%s"/>\n' % (k, v), head, count=1)
        log["brims"].append(name.group(1))
        return head + rest

    xml = re.sub(r'<object id="\d+">.*?</object>', obj, xml, flags=re.S)
    return xml, log


def brim_parts():
    """Part names that get a bed-slinger brim, from the P1S build's footprint metrics."""
    data = json.load(open(os.path.join(HERE, "..", "data", "build_data.json")))
    out = {}
    for r in data:
        if "brim_type" in (r.get("info") or {}).get("from_reference", {}):
            continue    # the designer chose the brim
        for part, met in (r.get("metrics") or {}).items():
            f = met.get("footprint") or {}
            s, h = f.get("slenderness") or 0, f.get("height") or 0
            if s >= BRIM_SLENDER or (h >= BRIM_TALL[0] and s >= BRIM_TALL[1]):
                out[part] = dict(device=r["id"], height=h, min_width=f.get("min_width"),
                                 slenderness=s)
    return out


def convert(path, brims=None):
    """Rewrite one 3mf in place. Returns a log dict, or None if it is already an A1 file."""
    zin = zipfile.ZipFile(path)
    cfg = json.loads(zin.read("Metadata/project_settings.config"))
    if cfg.get("printer_settings_id") == NEW_MACHINE:
        return None
    m = re.match(r"(\d+) ", os.path.basename(path))
    protect = set()
    if m:
        data = {r["id"]: r for r in json.load(open(os.path.join(HERE, "..", "data",
                                                                 "build_data.json")))}
        r = data.get(int(m.group(1))) or {}
        protect = set((r.get("info") or {}).get("from_reference", {}))
    old_p, new_p, _, _ = process_pair(cfg["print_settings_id"])
    new_cfg, log = convert_project(cfg, protect)
    brims = brim_parts() if brims is None else brims
    ms, mlog = convert_model_settings(zin.read("Metadata/model_settings.config").decode(),
                                      old_p, new_p, set(brims))
    log.update(mlog)
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "Metadata/project_settings.config":
                data = json.dumps(new_cfg, indent=4, ensure_ascii=False).encode()
            elif info.filename == "Metadata/model_settings.config":
                data = ms.encode()
            zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            zi.compress_type, zi.external_attr = info.compress_type, info.external_attr
            zout.writestr(zi, data)
    zin.close()
    os.replace(tmp, path)
    return log


INDEXED = ("Metadata/layer_heights_profile.txt", "Metadata/brim_ear_points.txt")
RANGES = "Metadata/layer_config_ranges.xml"


def object_centres(path):
    """[(object id, name, (x, y) bed-space bbox centre)] in build order."""
    import p3mf
    out = []
    for part in p3mf.Ref(path).parts():
        p3mf.load_geometry(part)
        xy = part.verts[:, :2]
        c = (xy.min(axis=0) + xy.max(axis=0)) / 2 + part.base_xy
        out.append((part.key.rsplit("::", 1)[1], part.name, (float(c[0]), float(c[1]))))
    return out


def trim(path, units, count):
    """Keep `units` copies (or whole kits) of a `count`-unit plate - the ones nearest the
    middle of the plate, as build.apply_cap does - by deleting the other objects. Nothing
    left on the plate moves. Returns the ids removed."""
    import math
    objs = object_centres(path)
    by_name = {}
    for oid, name, c in objs:
        by_name.setdefault(name, []).append((math.hypot(c[0] - 128, c[1] - 128), oid))
    keep = set()
    for name, lst in by_name.items():
        if len(lst) % count:
            raise RuntimeError(f"{path}: {len(lst)} x {name} is not a whole number of "
                               f"{count} units")
        per = len(lst) // count
        keep |= {oid for _, oid in sorted(lst)[:per * units]}
    drop = [oid for oid, _, _ in objs if oid not in keep]
    order = [oid for oid, _, _ in objs]
    new_index = {}
    for oid in order:
        if oid in keep:
            new_index[order.index(oid) + 1] = len(new_index) + 1

    zin = zipfile.ZipFile(path)
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            name = info.filename
            if name in ("3D/3dmodel.model", "Metadata/model_settings.config", RANGES) \
                    or name in INDEXED:
                t = data.decode("utf-8")
                if name == "3D/3dmodel.model":
                    for oid in drop:
                        t = re.sub(r'\n?[ \t]*<object id="%s"[ >].*?</object>' % oid, "", t,
                                   count=1, flags=re.S)
                        t = re.sub(r'\n?[ \t]*<item objectid="%s"[^>]*/>' % oid, "", t, count=1)
                elif name == "Metadata/model_settings.config":
                    for oid in drop:
                        t = re.sub(r'\n?[ \t]*<object id="%s">.*?</object>' % oid, "", t,
                                   count=1, flags=re.S)
                        t = re.sub(r'\n?[ \t]*<model_instance>\s*<metadata key="object_id" '
                                   r'value="%s"/>.*?</model_instance>' % oid, "", t,
                                   count=1, flags=re.S)
                        t = re.sub(r'\n?[ \t]*<assemble_item object_id="%s"[^>]*/>' % oid, "", t)
                elif name == RANGES:
                    def ren(m):
                        i = int(m.group(1))
                        return (f'<object id="{new_index[i]}">{m.group(2)}</object>'
                                if i in new_index else "")
                    t = re.sub(r'<object id="(\d+)">(.*?)</object>', ren, t, flags=re.S)
                else:
                    lines = []
                    for line in t.splitlines():
                        m = re.match(r"object_id=(\d+)\|(.*)$", line)
                        if m and int(m.group(1)) not in new_index:
                            continue
                        if m:
                            line = f"object_id={new_index[int(m.group(1))]}|{m.group(2)}"
                        lines.append(line)
                    t = "\n".join(lines) + ("\n" if t.endswith("\n") else "")
                data = t.encode("utf-8")
            zi = zipfile.ZipInfo(name, date_time=info.date_time)
            zi.compress_type, zi.external_attr = info.compress_type, info.external_attr
            zout.writestr(zi, data)
    zin.close()
    os.replace(tmp, path)
    return drop


def fit_one(path):
    """Slice one converted full plate; while it runs past devices.MAX_HOURS, keep fewer
    copies (fitplate's rule) and slice again. Supplied plates are reported, never trimmed.
    Returns (final path, record)."""
    import math, tempfile
    import devices, validate
    from fitplate import hours
    m = re.match(r"(\d+) (.*) - (PLA|PETG) x(\d+)\.3mf$", os.path.basename(path))
    did, count = int(m.group(1)), int(m.group(4))
    dev = next(d for d in devices.DEVICES if d["id"] == did)
    rec = dict(id=did, slug=dev["slug"], count_p1s=count, trims=[])
    while True:
        with tempfile.TemporaryDirectory() as d:
            s = validate.slice_project(path, d)
        p1 = s["plates"].get(1, {})
        t = hours(p1.get("total_time"))
        rec.update(ok=s["ok"], count=count, total_time=p1.get("total_time"),
                   used_g=p1.get("used_g"), used_cm3=p1.get("used_cm3"),
                   warnings=s["warnings"], conflict=s.get("conflict"), clamped=s["clamped"])
        print(f"  {did:02d} x{count:<3} -> " + (f"{p1.get('total_time')}, {p1.get('used_g', 0):.0f} g"
              if s["ok"] else f"FAILED {s['warnings'][:2]}"), flush=True)
        if not s["ok"] or t <= devices.MAX_HOURS:
            break
        if dev.get("supplied"):
            rec["over_cap"] = True
            break
        units = max(1, min(count - 1, math.floor(count * devices.MAX_HOURS / t)))
        trim(path, units, count)
        new = os.path.join(os.path.dirname(path),
                           f"{m.group(1)} {m.group(2)} - {m.group(3)} x{units}.3mf")
        os.replace(path, new)
        rec["trims"].append((count, units, p1.get("total_time")))
        path, count = new, units
    rec["file"] = os.path.basename(path)
    return path, rec


def fit_all(paths, out_json, workers=4):
    from multiprocessing import Pool
    with Pool(workers) as pool:
        results = pool.map(fit_one, paths, chunksize=1)
    data = {}
    if os.path.exists(out_json):
        data = json.load(open(out_json))
    for _, rec in results:
        data[rec["slug"]] = rec
    json.dump(dict(sorted(data.items(), key=lambda kv: kv[1]["id"])), open(out_json, "w"),
              indent=2)
    return results


UPSTREAM = "upstream/main"     # the P1S catalogue this one was converted from
LEFTOVER = re.compile(r"P1S|X1C|X1 Carbon|X1E|BBL A1M")


def p1s_original(repo, relpath):
    """The P1S version of a file, from the upstream branch (matched on its number, since a
    trimmed plate carries a different copy count in its name)."""
    import subprocess
    d = os.path.dirname(relpath)
    names = subprocess.run(["git", "-C", repo, "ls-tree", "--name-only",
                            UPSTREAM + (":" + d if d else "")],
                           capture_output=True, text=True, check=True).stdout.splitlines()
    base = os.path.basename(relpath)
    m = re.match(r"(\d+) ", base)
    hit = [n for n in names if (n.startswith(m.group(0)) if m else n == base)]
    src = os.path.join(os.path.dirname(relpath), hit[0]) if hit else relpath
    return subprocess.run(["git", "-C", repo, "show", f"{UPSTREAM}:{src}"],
                          capture_output=True, check=True).stdout


def _objects(ms_xml):
    out = {}
    for m in re.finditer(r'<object id="(\d+)">(.*?)</object>', ms_xml, re.S):
        head = m.group(2).split("<part", 1)[0]
        out[m.group(1)] = dict(re.findall(r'<metadata key="([^"]+)" value="([^"]*)"', head))
    return out


def check(repo, relpath, brims=None):
    """Structural + conversion check of one A1 file against its P1S original."""
    import io
    brims = brim_parts() if brims is None else brims
    probs, notes = [], []
    z = zipfile.ZipFile(os.path.join(repo, relpath))
    old = zipfile.ZipFile(io.BytesIO(p1s_original(repo, relpath)))
    if set(z.namelist()) != set(old.namelist()):
        probs.append(f"members changed: {sorted(set(z.namelist()) ^ set(old.namelist()))}")
    cfg = json.loads(z.read("Metadata/project_settings.config"))
    ocfg = json.loads(old.read("Metadata/project_settings.config"))
    want = {"printer_settings_id": NEW_MACHINE, "printer_model": "Bambu Lab A1",
            "bed_exclude_area": [], "printable_height": "256",
            "printable_area": ["0x0", "256x0", "256x256", "0x256"],
            "curr_bed_type": "Textured PEI Plate"}
    for k, v in want.items():
        if cfg.get(k) != v:
            probs.append(f"{k} is {cfg.get(k)!r}, expected {v!r}")
    if not cfg.get("print_settings_id", "").endswith(NEW_SUFFIX):
        probs.append(f"process preset {cfg.get('print_settings_id')}")
    for f in cfg.get("filament_settings_id", []):
        if f not in ("Bambu PLA Basic @BBL A1", PETG_NEW):
            probs.append(f"filament preset {f}")
    for name in ("Metadata/project_settings.config", "Metadata/model_settings.config"):
        left = sorted(set(LEFTOVER.findall(z.read(name).decode("utf-8", "replace"))))
        if left:
            probs.append(f"{name} still mentions {left}")

    # project keys: only machine, filament and the machine-tied process keys may change
    old_p, new_p, _, _ = process_pair(ocfg["print_settings_id"])
    allowed = (set(preset_keys(resolve("machine", NEW_MACHINE)))
               | set(preset_keys(resolve("machine", OLD_MACHINE)))
               | set(moved_keys(old_p, new_p)) | META_KEYS | {"print_compatible_printers",
               "printer_model", "default_print_profile", "default_filament_profile",
               "upward_compatible_machine"})
    for f in set(ocfg["filament_settings_id"]) | set(cfg["filament_settings_id"]):
        allowed |= set(filament(f))
    changed = sorted(k for k in set(cfg) | set(ocfg)
                     if cfg.get(k) != ocfg.get(k) and k not in allowed)
    if changed:
        probs.append(f"process keys changed that should not have: {changed}")

    # meshes byte for byte
    for n in old.namelist():
        if n.startswith("3D/Objects/") and n in z.namelist() and z.read(n) != old.read(n):
            probs.append(f"mesh {n} differs from the P1S file")

    # per-object settings: only the machine-tied ones, and brims where added
    moved = set(moved_keys(old_p, new_p))
    new_objs, old_objs = _objects(z.read("Metadata/model_settings.config").decode()), \
        _objects(old.read("Metadata/model_settings.config").decode())
    for oid, md in new_objs.items():
        o = old_objs.get(oid)
        if o is None:
            probs.append(f"object {oid} is not in the P1S file")
            continue
        for k in set(md) | set(o):
            if md.get(k) == o.get(k) or k in moved:
                continue
            if k in ("brim_type", "brim_width") and md.get("name") in brims:
                continue
            probs.append(f"object {oid} ({md.get('name')}): {k} {o.get(k)} -> {md.get(k)}")
    dropped = len(old_objs) - len(new_objs)
    if dropped:
        notes.append(f"{dropped} objects removed for the print-time cap")
    if any(md.get("name") in brims and md.get("brim_type") == "outer_only"
           and old_objs[oid].get("brim_type") != "outer_only" for oid, md in new_objs.items()):
        notes.append("bed-slinger brim added")

    # every object is built, has settings and sits on a plate; per-object extras line up
    model = z.read("3D/3dmodel.model").decode()
    items = re.findall(r'<item objectid="(\d+)"', model)
    res = re.findall(r'<object id="(\d+)"', model)
    ms = z.read("Metadata/model_settings.config").decode()
    inst = re.findall(r'<metadata key="object_id" value="(\d+)"/>', ms)
    if not (set(items) == set(res) == set(new_objs) == set(inst)):
        probs.append(f"object lists disagree: build {len(items)}, resources {len(res)}, "
                     f"settings {len(new_objs)}, plate instances {len(inst)}")
    for name in INDEXED:
        if name in z.namelist():
            idx = [int(x) for x in re.findall(r"^object_id=(\d+)\|", z.read(name).decode(), re.M)]
            if idx and max(idx) > len(items):
                probs.append(f"{name} points past the last object ({max(idx)} > {len(items)})")
    return dict(problems=probs, notes=notes)


def update_data(repo):
    """Fold the A1 results into the report data (build_data.json, slices_devices.json,
    selfcheck.json), keeping the P1S slices alongside for the comparison table."""
    import devices
    D = os.path.join(repo, "Validation", "data")
    rows = json.load(open(os.path.join(D, "build_data.json")))
    fits = json.load(open(os.path.join(D, "a1_slices_devices.json")))
    p1s_path = os.path.join(D, "slices_devices_p1s.json")
    if not os.path.exists(p1s_path):
        os.replace(os.path.join(D, "slices_devices.json"), p1s_path)
    p1s = json.load(open(p1s_path))
    brims = brim_parts()
    x1c, a1p, _, _ = process_pair("0.20mm Standard @BBL X1C")
    moved = {k: (norm(x1c[k])[0], norm(a1p[k])[0]) for k in moved_keys(x1c, a1p)
             if k in x1c and k in a1p}
    slices, conv_brims = {}, {}
    for r in rows:
        f = fits[r["slug"]]
        path = os.path.join(repo, "Full Plates", f["file"])
        z = zipfile.ZipFile(path)
        cfg = json.loads(z.read("Metadata/project_settings.config"))
        objs = _objects(z.read("Metadata/model_settings.config").decode())
        old_p1 = ((p1s.get(r["slug"]) or {}).get("plates") or {})
        old_p1 = old_p1.get("1") or old_p1.get(1) or {}
        added = sorted({md.get("name") for md in objs.values()
                        if md.get("name") in brims and md.get("brim_type") == "outer_only"})
        dev = next(d for d in devices.DEVICES if d["id"] == r["id"])
        already = [n for n in added if n in (dev.get("part_overrides") or {})]
        added = [n for n in added if n not in already]
        for n in added + already:
            conv_brims[n] = dict(brims[n], already=n in already)
        r["a1"] = dict(p1s_count=f["count_p1s"], p1s=old_p1, trims=f["trims"], brims=added,
                       process=moved)
        r["file"], r["count"] = f["file"], f["count"]
        r["path"] = path
        r["objects"] = len(objs) if objs else r["objects"]
        if f["trims"]:
            r["capped_from"] = r.get("capped_from") or f["count_p1s"]
            r["layout"] = re.sub(r"\(capped from \d+", f"(capped from {r['capped_from']}",
                                 r.get("layout", "")) if "capped" in r.get("layout", "") else \
                f"{r.get('layout', '')} (capped from {r['capped_from']} for print time)"
        r["filaments"] = list(dict.fromkeys(cfg["filament_settings_id"]))
        r["profile"]["preset"] = cfg["print_settings_id"]
        if objs:
            vals = sorted({md.get("brim_type", "auto_brim") for md in objs.values()},
                          key=lambda v: (len(v), v))
            r["profile"]["brim"] = "/".join(vals)
        info = r.get("info") or {}
        for k, (a, b) in moved.items():
            if k in info.get("from_reference", {}):
                info["from_reference"][k] = [b, info["from_reference"][k][1]]
            if k in info.get("kept_p1s", {}):
                info["kept_p1s"][k] = [info["kept_p1s"][k][0], b]
        if info.get("target_preset"):
            info["target_preset"] = cfg["print_settings_id"]
        if r.get("spacing"):
            r["spacing"]["corner"] = None
        slices[r["slug"]] = dict(ok=f["ok"], plates={"1": {k: f.get(k) for k in
                                                          ("total_time", "used_g", "used_cm3")}},
                                 warnings=f["warnings"], clamped=f["clamped"],
                                 conflict=f["conflict"])
    json.dump(rows, open(os.path.join(D, "build_data.json"), "w"), indent=2)
    json.dump(slices, open(os.path.join(D, "slices_devices.json"), "w"), indent=2)
    json.dump(dict(process=moved, brims=conv_brims,
                   filaments={"Bambu PLA Basic @BBL X1C": "Bambu PLA Basic @BBL A1",
                              PETG_OLD: PETG_NEW}),
              open(os.path.join(D, "a1_conversion.json"), "w"), indent=2)
    print(f"updated {len(rows)} rows")


def previews(repo):
    """Redraw every full plate's top view from the file itself (A1 bed: no excluded corner)."""
    import p3mf, verify
    from p3mf import Placement
    out = os.path.join(repo, "Validation", "plate previews")
    rows = json.load(open(os.path.join(repo, "Validation", "data", "build_data.json")))
    for r in rows:
        path = os.path.join(repo, "Full Plates", r["file"])
        try:
            parts = p3mf.Ref(path).parts()
        except RuntimeError as e:
            print(f"  {r['id']:02d} preview kept ({e})")
            continue
        pls = []
        for p in parts:
            p3mf.load_geometry(p)
            p.key = p.name
            pls.append(Placement(p, 0.0, p.base_xy[0], p.base_xy[1], 1))
        verify.preview(pls, os.path.join(out, f"{r['id']:02d} {r['slug']}.png"))
    print("previews redrawn")


def write_preset(out):
    """`PETG A1 Tuned` as a Bambu Studio user preset (File > Import > Import Configs)."""
    d = {"type": "filament", "name": PETG_NEW, "from": "User", "instantiation": "true",
         "inherits": FILAMENTS[PETG_OLD][1], "filament_settings_id": [PETG_NEW],
         "version": "2.2.0.4"}
    d.update(PETG_TUNED)
    d["filament_extruder_variant"] = ["Direct Drive Standard"]
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    json.dump(d, open(out, "w", encoding="utf-8"), indent=4, ensure_ascii=False)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "preset":
        write_preset(sys.argv[2])
    elif cmd == "brims":
        for k, v in brim_parts().items():
            print(f"{v['device']:02d}  {k:40} {v['height']:6.1f} mm on {v['min_width']:5.1f} mm "
                  f"(x{v['slenderness']})")
    elif cmd == "convert":
        brims = brim_parts()
        for p in sys.argv[2:]:
            lg = convert(p, brims)
            if lg is None:
                print(f"skip (already A1)  {os.path.basename(p)}")
                continue
            print(f"A1  {os.path.basename(p)}: machine {lg['machine']} keys, process "
                  f"{lg['process']}, kept {lg['process_kept']}, filament "
                  f"{len(lg['filament'])} keys (kept by hand: {sorted(lg['filament_kept'])}), "
                  f"object values {lg['objects']}, brims {sorted(set(lg['brims']))}", flush=True)
    elif cmd == "check":
        # a1.py check <repo> <out.json>: every 3mf in the repo against its P1S original
        import glob
        repo, out = sys.argv[2], sys.argv[3]
        brims = brim_parts()
        rels = sorted(os.path.relpath(p, repo) for p in
                      glob.glob(os.path.join(repo, "Full Plates", "*.3mf"))
                      + glob.glob(os.path.join(repo, "*.3mf")))
        res = {r: check(repo, r, brims) for r in rels}
        json.dump(res, open(out, "w"), indent=2)
        for r, v in res.items():
            print(f"{'OK  ' if not v['problems'] else 'FAIL'} {r}"
                  + "".join(f"\n       ! {p}" for p in v["problems"])
                  + "".join(f"\n         {n}" for n in v["notes"]))
        print(f"{len(res)} files, {sum(len(v['problems']) for v in res.values())} problems")
    elif cmd == "data":
        update_data(sys.argv[2])
    elif cmd == "previews":
        previews(sys.argv[2])
    elif cmd == "fit":
        # a1.py fit <out.json> <full plate.3mf> [...]
        for path, rec in fit_all(sys.argv[3:], sys.argv[2]):
            print(f"{rec['id']:02d} {rec['file']}: {rec['total_time']} "
                  f"{'OK' if rec['ok'] else 'FAILED'}"
                  + (f", trimmed {rec['trims']}" if rec["trims"] else "")
                  + (" OVER CAP (supplied plate)" if rec.get("over_cap") else ""))
    else:
        sys.exit(__doc__)
