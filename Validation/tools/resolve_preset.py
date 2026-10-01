#!/usr/bin/env python3
"""Flatten a Bambu system preset (follow `inherits`) into a standalone dict."""
import json, os, sys

ROOT = "/Applications/BambuStudio.app/Contents/Resources/profiles/BBL"
USER = os.path.expanduser("~/Library/Application Support/BambuStudio/user")
# presets this repo ships (PETG A1 Tuned), so a rebuild does not depend on one machine's Studio
REPO_PRESETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "presets")


def _find(kind, name):
    p = os.path.join(ROOT, kind, name + ".json")
    if os.path.exists(p):
        return p
    q = os.path.join(REPO_PRESETS, name + ".json")
    if kind == "filament" and os.path.exists(q):
        return q
    if os.path.isdir(USER):
        for uid in os.listdir(USER):
            q = os.path.join(USER, uid, kind, name + ".json")
            if os.path.exists(q):
                return q
    raise FileNotFoundError(f"{kind}/{name}")


def resolve(kind, name, _seen=None):
    _seen = _seen or set()
    if name in _seen:
        raise RuntimeError("inheritance loop at " + name)
    _seen.add(name)
    d = json.load(open(_find(kind, name), encoding="utf-8"))
    parent = d.pop("inherits", None)
    if parent:
        base = resolve(kind, parent, _seen)
        base.update(d)
        d = base
    d["name"] = name
    return d


if __name__ == "__main__":
    kind, name, out = sys.argv[1], sys.argv[2], sys.argv[3]
    d = resolve(kind, name)
    d.pop("instantiation", None)
    json.dump(d, open(out, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
    print(f"{out}: {len(d)} keys")
