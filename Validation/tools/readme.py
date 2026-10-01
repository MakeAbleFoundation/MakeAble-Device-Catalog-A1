#!/usr/bin/env python3
"""Write the folder's README.md from the build + validation data."""
import json, os, sys
import devices, report

EXCLUDED = [
    ("Other/EyeDropperAid.3mf", "MakeAble 'Eye Dropper Squeezer Aid' - a different model "
     "from the Printables Eye Drop Assist on the list"),
    ("Other/jar-opener+(1).3mf", "MakeAble 'Jar/Pop Bottle and Can Assist' - not the "
     "OPENSESAME3000 jar tool"),
    ("Other/4+in+1+button+aid,+key+turner,+zipper+aid,+handle.3mf",
     "MakeAble 4-in-1 aid - not the Clothes Button & Zipper Hook helper"),
    ("Other/Bottle_Opener_30.stl + .gcode", "a third bottle opener, sliced for a Prusa MK3S"),
    ("Toothbrush Grip (PLA)/toothbrush.STL", "the flat MyMiniFactory toothbrush, not the "
     "round arthritis grip you picked"),
    ("Walking Stick Holder/", "not on the catalogue list"),
    ("Other/DRAG+v2.3mf", "byte-identical copy of the DRAG folder's 3mf"),
    ("Other/Tube_Opener.3mf", "plain mesh export with no settings in it"),
    ("Aug*.3mf, Combined*.3mf, Bag_Carrier_x4.3mf", "earlier working files, not designer sources"),
    ("Clothes Button .../*.stl (loose)", "the loose STLs differ from the 3mf: its pins are "
     "scaled to 95% and its hook carries painted seams"),
]

# second batch (New Devices/): parts of a download that were deliberately not printed
EXCLUDED_2 = [
    ("adjustable-cane-holder-model_files/Design History Files/, Alternative Files/",
     "the designer's earlier versions and work-in-progress latch; their 'Recommended Print "
     "Files' are used"),
    ("universal-travel-coffee-gimbal-model_files/Optional *.stl",
     "optional extras (long bolt, nut, cup and flat-surface adapters, vertical gimbal, TPU "
     "bar wrap); the kit is gimbal + clamp + bolt + washer"),
    ("universal-travel-coffee-gimbal-model_files/MPC Washer.3mf, *.step, *.f3d",
     "a plain mesh of the washer STL that is used, and the CAD sources"),
    ("Full Size Playing Card Holder - 2863434/files/holder.stl, case-*.stl",
     "the original 3-row holder and the storage cases; the 4-row holder is the one on the list"),
    ("Full Size Playing Card Holder - 2863434/files/holder-4rows.stl",
     "same shape as holder-4row.stl"),
    ("adaptive-pencil-grip-model_files/Test print.stl", "a small pencil-fit test piece"),
    ("PRJ___YOUNGER+GRIP_Glue-in+Magnets_.3mf",
     "the earlier glue-in-magnets profile, replaced by the no-magnets plate"),
    ("ToothSqeez_ExterGear_SeigaihaPattern.3mf, plates 4-6",
     "the 1.0, 1.3 and 1.6 mm key shafts for thicker tube ends; the kit uses the 0.7 mm "
     "standard shaft"),
    ("Fingergrip+Press (1).3mf", "one file, three devices: each strength gets its own plate"),
]

CAT1_SHARED_NOTES = {
    "initial_layer_print_height": "Bottle Cap Opener's profile uses 0.15 mm",
    "initial_layer_speed": "the slowest any designer asked for (DRAG); others use 20-50 mm/s",
    "initial_layer_infill_speed": "slowest of the set",
}


def fmt(v, dash="-"):
    return dash if v in (None, "", 0) else v


def p1(sl, slug):
    s = sl.get(slug, {})
    return (s.get("plates") or {}).get("1") or (s.get("plates") or {}).get(1) or {}


def designer_printers(rows, by_slug):
    """The printers the designers' own profiles were saved for, other than the A1."""
    import p3mf
    seen = []
    for r in rows:
        d = by_slug[r["slug"]]
        if d.get("stl"):
            continue
        model = p3mf.Ref(d["ref"]).settings.get("printer_model", "")
        name = model.replace("Bambu Lab ", "")
        if name and name != "A1" and name not in seen:
            seen.append(name)
    return ", ".join(seen)


def shared_rows(cat_n, data):
    """The three print-level values of one catalogue and who wanted something else."""
    sh = data["shared"]
    one = lambda v: v[0] if isinstance(v, list) else v
    if cat_n == 1:
        notes = CAT1_SHARED_NOTES
    else:
        rows = data["rows"]
        short = lambda t: t.split(" (")[0]
        h = one(sh["initial_layer_print_height"])
        other_h = [f"{short(r['title'])}'s profile uses {r['device_first_layer']} mm"
                   for r in rows if float(r["device_first_layer"]) != float(h)]
        sp = [float(r["device_first_layer_speed"]) for r in rows]
        slow = [short(r["title"]) for r in rows
                if float(r["device_first_layer_speed"]) == min(sp)]
        rest = sorted({v for v in sp if v != min(sp)})
        span = (f"{rest[0]:g} mm/s" if len(rest) == 1 else f"{rest[0]:g}-{rest[-1]:g} mm/s")
        notes = {
            "initial_layer_print_height": "; ".join(other_h) or "every device uses it",
            "initial_layer_speed": (f"the slowest any designer asked for ({', '.join(slow)})"
                                    + (f"; the others use {span}" if rest else "")),
            "initial_layer_infill_speed": "slowest of the set",
        }
    return [
        f"| first layer height | {one(sh['initial_layer_print_height'])} mm | "
        f"{notes['initial_layer_print_height']} |",
        f"| first layer speed | {one(sh['initial_layer_speed'])} mm/s | "
        f"{notes['initial_layer_speed']} |",
        f"| first layer infill speed | {one(sh['initial_layer_infill_speed'])} mm/s | "
        f"{notes['initial_layer_infill_speed']} |",
    ]


def spacing_reason(r):
    pr = r["profile"]
    if pr["support"] in ("1", "some") and "tree" in pr["support_type"]:
        return "its tree supports flare out well past the part"
    if pr["support"] in ("1", "some"):
        return "its supports reach past the part"
    return "its brim reaches past the part"


def conversion_section(a1, rows, sl):
    """What the P1S -> A1 conversion changed, and how to repeat it."""
    L = ["## Converted from the P1S catalogue", ""]
    L.append("Every file was converted in place from the P1S edition by "
             "`Validation/tools/a1.py`. Nothing on a plate was moved and no mesh was touched. "
             "What changed:")
    L.append("")
    L.append("- **Printer**: `Bambu Lab A1 0.4 nozzle` system preset - bed with no excluded "
             "corner, 256 mm build height, the A1's start/end G-code, motion limits and "
             "bed-slinger structure.")
    pr = a1.get("process") or {}
    if pr:
        L.append("- **Process preset**: each `@BBL X1C` preset swapped for its `@BBL A1` "
                 "sibling (same layer height and name). Only four values differ between the "
                 "two, and each moved only where the file still had the X1C default: "
                 + ", ".join(f"`{k}` {a} -> {b}" for k, (a, b) in sorted(pr.items())) + ". "
                 "Every value a designer chose (walls, infill, supports, line widths, their "
                 "own speeds...) is untouched, on the project and on every object.")
    L.append("- **Filament**: `Bambu PLA Basic @BBL X1C` -> `Bambu PLA Basic @BBL A1` "
             "(65 C bed instead of 55 C, 60-80% fan instead of 100%, 6 s minimum layer time); "
             "`PETG P1S Tuned` -> `PETG A1 Tuned` (same tuning, A1 base: flow ratio 0.94).")
    if a1.get("brims"):
        L.append(f"- **Brims**: added on {len([b for b in a1['brims'].values() if not b.get('already')])} "
                 "tall parts, see *Brims for a moving bed*.")
    trimmed = [r for r in rows if (r.get("a1") or {}).get("trims")]
    if trimmed:
        L.append("- **Copies**: " + ", ".join(
            f"{r['title']} {r['a1']['p1s_count']} -> {r['count']}" for r in trimmed)
            + f" to stay under {devices.MAX_HOURS:.0f} h.")
    L.append("")
    L.append("| # | device | P1S time | A1 time | change |")
    L.append("|---|---|---|---|---|")
    import fitplate
    for r in rows:
        x = (r.get("a1") or {})
        t0 = (x.get("p1s") or {}).get("total_time")
        t1 = p1(sl, r["slug"]).get("total_time")
        d = ""
        if t0 and t1:
            h0, h1 = fitplate.hours(t0), fitplate.hours(t1)
            pct = round(100 * (h1 - h0) / h0)
            d = f"{pct:+d}%" if pct else "same"
            if x.get("trims"):
                d += f" (with {r['count']} instead of {x['p1s_count']})"
        L.append(f"| {r['id']:02d} | {r['title']} | {fmt(t0)} | {fmt(t1)} | {d} |")
    L.append("")
    L.append("To pull later changes from the P1S catalogue: merge `upstream/main`, then run "
             "`a1.py convert` on the changed files, `a1.py fit` on changed full plates, and "
             "`a1.py check` (see `Validation/tools/a1_all.sh`).")
    L.append("")
    return L


def main(out):
    D = f"{out}/Validation/data"
    rows = json.load(open(f"{D}/build_data.json"))
    refs = json.load(open(f"{D}/slices_refs.json"))
    sl = json.load(open(f"{D}/slices_devices.json"))
    chk = json.load(open(f"{D}/selfcheck.json"))
    by_slug = {d["slug"]: d for d in devices.DEVICES}
    supplied = [r for r in rows if r.get("supplied")]
    cats = []
    for n, c in sorted(devices.CATALOGUES.items()):
        if os.path.exists(f"{out}/{c['file']}") and os.path.exists(f"{D}/{c['data']}"):
            cats.append((n, c, json.load(open(f"{D}/{c['data']}"))))

    a1 = json.load(open(f"{D}/a1_conversion.json")) if os.path.exists(f"{D}/a1_conversion.json") else {}
    L = ["# MakeAble assistive devices - print files for the Bambu Lab A1", ""]
    L.append("Every file here is set up for a **Bambu Lab A1, 0.4 nozzle, textured PEI "
             "plate**, saved in Bambu Studio 2.2.2 format. Open one, check the plate, hit "
             "slice. Nothing needs to be re-arranged or re-configured.")
    L.append("")
    L.append("This is the A1 edition of [MakeAble-Device-Catalog]"
             "(https://github.com/MakeAbleFoundation/MakeAble-Device-Catalog), which is set up "
             "for the P1S: the same devices, the same files and the same plate arrangements, "
             "converted to the A1. See *Converted from the P1S catalogue* below for exactly "
             "what changed.")
    L.append("")
    L.append("## Printer this is for")
    L.append("")
    L.append("| | |")
    L.append("|---|---|")
    L.append("| Printer | Bambu Lab **A1** (256 x 256 x 256 mm build volume) |")
    L.append("| Nozzle | 0.4 mm hardened/stainless (stock) |")
    L.append("| Build plate | Textured PEI |")
    L.append("| Slicer | Bambu Studio 2.2.2 or newer (OrcaSlicer 2.4.2 also opens them) |")
    L.append("| Filaments | PLA (`Bambu PLA Basic @BBL A1`) and PETG (`PETG A1 Tuned`) - one "
             "per plate |")
    L.append("")
    L.append("`PETG A1 Tuned` is saved inside every PETG file, so it works on any computer. To "
             "have it as a named preset in Bambu Studio too, import "
             "`Validation/presets/PETG A1 Tuned.json` (File > Import > Import Configs).")
    L.append("")
    L.append("These files are **not** for the A1 mini (180 mm bed), P1S, X1C, P2S or H2 series "
             "without re-checking: the A1's machine settings, start G-code and motion limits "
             "are baked into every plate. For the P1S, use the original catalogue.")
    L.append("")
    L.append("## Repository layout")
    L.append("")
    L.append("- `Full Plates/` - one file per device, filled with as many copies as fit.")
    if len(cats) <= 1:
        L.append("- `Catalogue - one device per plate.3mf` - every device on its own plate, "
                 "one copy each, same settings.")
    else:
        for n, c, data in cats:
            ids = [r["slug"] for r in data["rows"]]
            first, last = by_slug[ids[0]]["id"], by_slug[ids[-1]]["id"]
            L.append(f"- `{c['file']}` - devices {first:02d}-{last:02d}, each on its own "
                     "plate, one copy each, same settings.")
    L.append("- `Validation/` - what was checked, per file, plus plate previews. "
             "`Validation/tools/` holds the Python scripts that built, converted and checked "
             "the plates; `Validation/presets/` holds the PETG preset.")
    L.append("")
    L.append("## Full plates")
    L.append("")
    L.append("| # | file | material | per plate | print time | filament | layer | walls | infill | supports | vs designer's file |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        q = p1(sl, r["slug"])
        pr = r["profile"]
        rs = refs.get(r["slug"]) or {}
        per_unit = (q.get("used_cm3", 0) / r["count"]) if r["count"] else 0
        ref_per = min((rs.get("per_unit_cm3") or {}).values(), default=None)
        match = f"{100 * per_unit / ref_per:.0f}%" if (ref_per and per_unit) else "-"
        sup = {"1": "yes", "some": "some parts"}.get(pr["support"], "no")
        L.append(f"| {r['id']:02d} | {r['file']} | {r['material']} | {r['count']} "
                 f"{report.unit_word(r)} | {fmt(q.get('total_time'))} | "
                 f"{fmt(round(q.get('used_g', 0), 0))} g | {pr['layer']} mm | "
                 f"{pr['walls']} | {pr['infill']} | {sup} | {match} |")
    L.append("")
    tot_g = sum(p1(sl, r["slug"]).get("used_g", 0) for r in rows)
    L.append(f"All {len(rows)} plates together: about {tot_g/1000:.1f} kg of filament.")
    L.append("")
    L.append("The last column is the check that matters: filament per copy on your plate "
             "against a slice of the designer's own untouched file. 100% means the part "
             "comes out exactly as they set it up. A few percent under 100% comes from the "
             "printer profile, not the part: the A1's elephant-foot compensation shaving the "
             "first layer (their printer profile did not apply it), and the A1 PETG preset's "
             "0.94 flow ratio. A dash means there is nothing to compare against "
             "(loose STLs, or a size variant that shares another file's profile"
             + (", or a supplied plate, which is its own reference" if supplied
                else "") + ").")
    L.append("")
    capped = [r for r in rows if r.get("capped_from")]
    if capped:
        L.append("## Print-time cap")
        L.append("")
        L.append(f"No plate runs longer than {devices.MAX_HOURS:.0f} hours (the slicer's "
                 "estimate). Where a full plate would take longer, it holds fewer copies - "
                 "the ones in the middle of the plate, kept together. The A1 accelerates "
                 "more gently than the P1S, so a few plates hold fewer copies than the P1S "
                 "edition:")
        L.append("")
        for r in capped:
            was = (r.get("a1") or {}).get("p1s_count")
            L.append(f"- **{r['title']}**: {r['count']} of the {r['capped_from']} {r['unit']} "
                     f"that fit ({fmt(p1(sl, r['slug']).get('total_time'))})"
                     + (f" - the P1S edition holds {was}" if was and was != r["count"] else ""))
        L.append("")
    if len(cats) <= 1:
        L.append("## Catalogue file")
        L.append("")
    else:
        L.append("## Catalogue files")
        L.append("")
        L.append("A Bambu Studio project holds at most 36 plates, so the one-per-plate "
                 "catalogue comes in two files.")
        L.append("")
    for n, c, data in cats:
        L.append(f"`{c['file']}` holds {len(data['rows'])} plates, one device each, in the "
                 "same order as the table above. "
                 "Each plate keeps its own layer height, wall count, infill and support "
                 "settings - those are baked onto the objects, so switching the process preset "
                 "in Studio will not silently wipe them.")
        L.append("")
        if n == cats[0][0]:
            L.append("Filament slot 1 is PLA, slot 2 is PETG, and every plate uses one or the "
                     "other, so you only ever load one spool per plate.")
            L.append("")
        L.append("Three settings cannot vary per plate in Bambu Studio, so the file uses the "
                 "most conservative value any device asked for:")
        L.append("")
        L.append("| setting | catalogue | who wanted something else |")
        L.append("|---|---|---|")
        L += shared_rows(n, data)
        L.append("")
    L.append("If you want a device exactly as its designer set it up, use its file in "
             "`Full Plates/` - those keep every value.")
    L.append("")
    L.append("## Spacing")
    L.append("")
    L.append("Parts sit at least 5 mm apart, measured on their real outlines rather than "
             "bounding boxes, which is what lets the C-shaped ones nest into each other. "
             "Where a profile adds a brim or supports, those reach past the part itself, "
             "so the plate is sliced and the spacing widened until the slicer stops "
             "reporting conflicting toolpaths:")
    L.append("")
    for r in rows:
        if not r.get("supplied") and r.get("gap", 5) != 5:
            L.append(f"- **{r['title']}**: {r['gap']:.0f} mm apart - {spacing_reason(r)}.")
    L.append("")
    for r in rows:
        if by_slug[r["slug"]].get("keep_layout") and "designer" in r.get("layout", ""):
            L.append(f"**{r['title']}** is too big for the packer's 5 mm margins, so it uses "
                     "the designer's own plate arrangement, centred.")
            L.append("")
    for r in supplied:
        sp = r["spacing"]
        clean = (sl.get(r["slug"]) or {}).get("ok")
        L.append(f"**{r['title']}** is a supplied plate, arranged by hand in Bambu Studio and "
                 f"kept exactly as it is: its parts are {report.fmt_mm(sp['gap'], 'over 10 mm')} "
                 f"apart and {report.fmt_mm(sp['edge'])} from the plate edge. "
                 + ("It slices with no conflicting toolpaths." if clean
                    else "It does NOT slice clean - see its validation page."))
        L.append("")
    L.append("The plates were packed for the P1S, which cannot print in an 18 x 28 mm patch "
             "at the front-left corner. The A1 has no such patch, so that corner is simply "
             "empty; the arrangements were kept exactly as they were rather than re-packed.")
    L.append("")
    brims = a1.get("brims") or {}
    if brims:
        L.append("## Brims for a moving bed")
        L.append("")
        L.append("The A1 moves the bed back and forth under the part, so a part that is tall "
                 "for its footprint can rock loose late in the print. Parts that stand at "
                 "least 2.3 times taller than their narrowest footprint width, or 60 mm tall "
                 "and 1.5 times, get a 5 mm outer brim, unless the designer chose the brim "
                 "themselves:")
        L.append("")
        for name, b in brims.items():
            title = next((r["title"] for r in rows if r["id"] == b["device"]), "")
            how = ("already has an outer brim in its profile" if b.get("already")
                   else "outer brim added")
            L.append(f"- **{title}** - {name}: {b['height']:g} mm tall on a "
                     f"{b['min_width']:g} mm footprint - {how}")
        kept = [(r, a) for r in rows for a in r["advisories"] if "brim off" in a]
        for r, a in kept:
            L.append(f"- **{r['title']}**: left without a brim, as the designer set it ({a.split(': ', 1)[1]})")
        L.append("")
    L.append("## How the settings were decided")
    L.append("")
    L.append("For each device, in order:")
    L.append("")
    L.append("1. **Machine settings** always come from the A1 system preset. Nothing from "
             f"the designer's printer ({designer_printers(rows, by_slug)}) is carried over - "
             "no start/end gcode, no bed shape, no kinematics.")
    L.append("2. **Filament**: `PETG A1 Tuned` for PETG (your PETG tuning on Bambu's A1 PETG "
             "Basic: 240/250 C nozzle, 60/65 C bed, 20-65% fan, 8 mm3/s, 1.6 mm retraction, "
             "0.4 mm z-hop), `Bambu PLA Basic @BBL A1` for PLA.")
    L.append("3. **Speeds, accelerations and elephant-foot compensation** follow the A1 "
             "preset, *unless* the designer had deliberately changed that value on their "
             "own printer - then their number wins.")
    L.append("4. **Everything else** - walls, infill, shells, supports, brim, seams, line "
             "widths, variable layer heights - is the designer's own value from their 3mf.")
    L.append("5. **Loose STLs** have no designer profile: they get the A1 0.20 mm Standard "
             "profile plus only the settings the designer states on the model page.")
    L.append("6. Anything changed on purpose beyond that is listed per file in "
             "`Validation/per file/`.")
    if supplied:
        L.append("7. **Supplied plates**, arranged by hand in Bambu Studio ("
                 + ", ".join(r["title"] for r in supplied)
                 + "), are delivered exactly as saved, settings included.")
    L.append("")
    L.append("## How they were checked")
    L.append("")
    L.append("Bambu Studio's command-line slicer crashes on macOS (a known upstream bug), "
             "so slicing checks were run with OrcaSlicer 2.4.2, which reads the same "
             "project format. Per file:")
    L.append("")
    L.append("- the plate slices with no errors, and the time and filament are recorded;")
    L.append(f"- the plate finishes inside {devices.MAX_HOURS:.0f} hours;")
    L.append("- filament per copy is compared against a slice of the designer's untouched "
             "file, and against the weight quoted on the model page;")
    L.append("- every part is inside the plate, with at least 5 mm between parts (checked "
             "on the real outlines, not bounding boxes)" + ("; a supplied plate keeps its own "
                                                            "spacing" if supplied else "") + ";")
    L.append("- meshes are byte-identical to the designer's, so painted seams survive;")
    L.append("- each object carries its settings, and every object is on a plate;")
    L.append("- against the P1S edition: meshes byte for byte identical, and no setting "
             "changed except the machine, the filament presets, the four machine-tied process "
             "values and the added brims.")
    L.append("")
    probs = sum(len(v["problems"]) for v in chk.values())
    L.append(f"Structural checks: {len(chk)} files, {probs} problems. "
             + ("All clean." if not probs else "See Validation/selfcheck.json."))
    L.append("")
    hw = [(r, by_slug[r["slug"]]["hardware"]) for r in rows
          if by_slug[r["slug"]].get("hardware")]
    if hw:
        L.append("## Also needed (not printed)")
        L.append("")
        for r, h in hw:
            L.append(f"- **{r['title']}**: {h}")
        L.append("")
    fixed = [(r, report.MESH_FIXES[k]) for r in rows for k in report.MESH_FIXES
             if by_slug[r["slug"]].get(k)]
    if fixed:
        L.append("## Changed on purpose")
        L.append("")
        for r, f in fixed:
            L.append(f"- **{r['title']}**: {f}.")
        L.append("")
    adv = [(r, a) for r in rows for a in r["advisories"]]
    if adv:
        L.append("## Worth knowing (nothing was changed)")
        L.append("")
        for r, a in adv:
            L.append(f"- **{r['title']}**: {a}")
        L.append("")
    if a1:
        L += conversion_section(a1, rows, sl)
    L.append("## Where each file came from")
    L.append("")
    L.append("| # | device | designer source file (kept locally, not in this repo) | model page |")
    L.append("|---|---|---|---|")
    for r in rows:
        d = by_slug[r["slug"]]
        src = d.get("ref") or (d.get("stl") or ["-"])[0]
        src = report.source_label(src)
        if len(d.get("stl") or []) > 1:
            src += f" (+{len(d['stl']) - 1} more)"
        link = f"[page]({d['link']})" if d.get("link") else "-"
        L.append(f"| {r['id']:02d} | {r['title']} | `{src}` | {link} |")
    L.append("")
    L.append("Each MakerWorld link's profile id was matched against the `DesignProfileId` "
             "stored inside the local 3mf, so these are the exact profiles that were linked. "
             "The links for 19-21 (Arthritis Toothbrush Grip, One-Handed Page Holder, "
             "Smartphone Magnification Stand) were added afterwards from the model pages "
             "themselves.")
    L.append("")
    L.append("## Look-alikes that were left out")
    L.append("")
    for f, why in EXCLUDED:
        L.append(f"- `{f}` - {why}")
    if any(r["id"] > 30 for r in rows):
        L.append("")
        L.append("From the second batch (`New Devices/`):")
        L.append("")
        for f, why in EXCLUDED_2:
            L.append(f"- `{f}` - {why}")
    L.append("")
    L.append("## Still open")
    L.append("")
    eda = [r["id"] for r in rows if r["slug"].startswith("eda-")]
    L.append(f"- **Eye Drop Assist (files {min(eda)}-{max(eda)})**: the three Printables pages sit behind a "
             "bot check, so the designer's own print settings could not be read. Those "
             "files use the A1 0.20 mm Standard profile in PLA. They also need a decision: "
             "whether a pliers and an eyepiece pair up into one device (in which case they "
             "should be kit plates) or are alternatives.")
    if "cup-holder" in {r["slug"] for r in rows}:
        L.append("- **Universal Cup Holder**: the designer's painted brim ears are carried "
                 "over, but OrcaSlicer (used for these checks) does not read painted ears. "
                 "Worth a glance at the first layer in Bambu Studio's preview before the "
                 "first print.")
    L.append("")
    open(f"{out}/README.md", "w").write("\n".join(L) + "\n")
    print(f"wrote {out}/README.md")


if __name__ == "__main__":
    main(sys.argv[1])
