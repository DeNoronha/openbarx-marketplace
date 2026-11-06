#!/usr/bin/env python3
"""Check index.json: the schema rules that matter, unique ids, and that every widget folder is listed.

Usage: python3 tools/validate.py [--fetch]   (--fetch also downloads each item and checks its sha256)
"""
import hashlib, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KINDS = {"widget", "bar-app", "hotkey-pack"}
REQUIRED = ["id", "kind", "name", "version", "summary", "publisher", "license"]
PER_KIND = {"widget": ["format", "targets", "download", "sha256", "source"], "hotkey-pack": ["download", "sha256", "actions", "platform"]}

def main():
    errors = []
    idx = json.load(open(os.path.join(ROOT, "index.json"), encoding="utf-8"))
    if idx.get("format") != 1: errors.append("index format must be 1")
    seen = set()
    for n, item in enumerate(idx.get("items", [])):
        where = f"items[{n}] ({item.get('id', '?')})"
        for key in REQUIRED + PER_KIND.get(item.get("kind"), []):
            if key not in item or item[key] in ("", None, []): errors.append(f"{where}: missing {key}")
        if item.get("kind") not in KINDS: errors.append(f"{where}: unknown kind {item.get('kind')}")
        if not re.fullmatch(r"[a-z0-9]+(\.[A-Za-z0-9_-]+)+", item.get("id", "")): errors.append(f"{where}: id is not reverse-DNS")
        if item.get("id") in seen: errors.append(f"{where}: duplicate id")
        seen.add(item.get("id"))
        if "sha256" in item and not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]): errors.append(f"{where}: sha256 is not 64 hex digits")
        if "--fetch" in sys.argv and item.get("download"):
            data = urllib.request.urlopen(item["download"], timeout=30).read()
            if hashlib.sha256(data).hexdigest() != item.get("sha256"): errors.append(f"{where}: download does not match sha256")
    widgets = os.path.join(ROOT, "widgets")
    for d in sorted(os.listdir(widgets)) if os.path.isdir(widgets) else []:
        if os.path.isdir(os.path.join(widgets, d)) and d not in seen: errors.append(f"widgets/{d} is not listed in index.json")
    for e in errors: print("error:", e)
    print(f"{len(idx.get('items', []))} items, {len(errors)} errors")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
