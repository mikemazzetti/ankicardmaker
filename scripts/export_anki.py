#!/usr/bin/env python3
"""Export the whole Anki collection to version-controlled JSON, one file per deck.

Talks to the AnkiMCP add-on's local HTTP MCP server (http://127.0.0.1:3141/),
so Anki must be open with the AnkiMCP add-on installed. Media binaries are NOT
exported — only note text and any [sound:]/<img> references inside fields.

Usage:  python3 scripts/export_anki.py [--out anki-export]
Re-run any time to refresh the snapshot, then commit the diff.
"""
import json, sys, os, re, time, datetime, urllib.request

URL = "http://127.0.0.1:3141/"
OUT = "anki-export"
if "--out" in sys.argv:
    OUT = sys.argv[sys.argv.index("--out") + 1]

_id = [0]
def _post(method, params=None, notify=False):
    _id[0] += 1
    body = {"jsonrpc": "2.0", "method": method}
    if not notify: body["id"] = _id[0]
    if params is not None: body["params"] = params
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
        headers={"content-type": "application/json",
                 "accept": "application/json, text/event-stream"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read().decode()
    if notify: return None
    if "data:" in raw:
        for line in raw.splitlines():
            if line.startswith("data:"): raw = line[5:].strip()
    return json.loads(raw)

def call(name, arguments):
    r = _post("tools/call", {"name": name, "arguments": arguments})
    if "error" in r: raise SystemExit("TOOL ERROR " + name + ": " + json.dumps(r["error"]))
    return r["result"]["structuredContent"]

def sanitize(seg):
    seg = seg.replace("/", "-").strip()
    return re.sub(r'[<>:"\\|?*]', "_", seg)

def deck_path(name):
    return os.path.join(OUT, *[sanitize(s) for s in name.split("::")])

def find_ids(query):
    ids, offset = [], 0
    while True:
        r = call("find_notes", {"query": query, "limit": 100, "offset": offset})
        batch = r.get("noteIds", [])
        ids.extend(batch)
        if not r.get("hasMore") or not batch: break
        offset += 100
    return ids

def main():
    _post("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                         "clientInfo": {"name": "export", "version": "1"}})
    _post("notifications/initialized", notify=True)

    decks = [d for d in call("list_decks", {})["decks"] if not d.get("is_filtered")]
    os.makedirs(OUT, exist_ok=True)
    index, grand_total = [], 0
    t0 = time.time()

    for d in decks:
        name = d["name"]
        # notes directly in this deck, excluding sub-decks (each note filed once)
        ids = find_ids(f'deck:"{name}" -deck:"{name}::*"')
        if not ids:
            index.append((name, 0)); continue
        notes = []
        for i in range(0, len(ids), 100):
            chunk = ids[i:i+100]
            info = call("notes_info", {"notes": chunk})
            for n in info["notes"]:
                notes.append({
                    "noteId": n["noteId"],
                    "modelName": n.get("modelName"),
                    "tags": sorted(n.get("tags", [])),
                    "fields": {k: v["value"] for k, v in n.get("fields", {}).items()},
                })
        notes.sort(key=lambda x: x["noteId"])
        path = deck_path(name) + ".json"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"deck": name, "note_count": len(notes),
                       "exported": datetime.date.today().isoformat(),
                       "notes": notes}, f, ensure_ascii=False, indent=1)
        index.append((name, len(notes)))
        grand_total += len(notes)
        print(f"  {name}  ->  {len(notes)} notes")

    # index
    lines = ["# Anki collection export", "",
             f"Snapshot generated {datetime.date.today().isoformat()} from the local Anki",
             "collection via the AnkiMCP add-on. One JSON file per deck (media binaries not",
             "included). Regenerate with `python3 scripts/export_anki.py`.", "",
             f"**Total: {grand_total} notes across {sum(1 for _,c in index if c)} non-empty decks.**", "",
             "| Deck | Notes |", "|------|------:|"]
    for name, c in sorted(index):
        lines.append(f"| {name} | {c} |")
    with open(os.path.join(OUT, "INDEX.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\nDONE: {grand_total} notes in {time.time()-t0:.0f}s -> {OUT}/")

if __name__ == "__main__":
    main()
