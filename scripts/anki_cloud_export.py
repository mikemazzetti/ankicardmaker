#!/usr/bin/env python3
"""Cloud backup: download the collection from AnkiWeb using a stored hkey token,
then export every deck to anki-export/ as JSON (same format as export_anki.py).

Runs in GitHub Actions (headless). Uses SyncAuth(hkey) — never password login,
which CI blocks. Requires env: ANKIWEB_HKEY (and optionally ANKIWEB_ENDPOINT).
Media binaries are not exported. Read-only w.r.t. AnkiWeb: it only ever
downloads, never uploads.
"""
import os, json, re, tempfile, datetime, collections, sys

from anki.collection import Collection
from anki.sync import SyncAuth
from anki import sync_pb2

R = sync_pb2.SyncCollectionResponse
OUT = "anki-export"

def log(*a): print(*a, flush=True)

def sync_down(col, auth):
    """Perform a download-only sync; return the (possibly updated) auth."""
    for attempt in range(4):
        out = col.sync_collection(auth, False)  # sync_media=False
        if out.new_endpoint and out.new_endpoint != (auth.endpoint or ""):
            log("Server redirected to endpoint:", out.new_endpoint)
            auth = SyncAuth(hkey=auth.hkey, endpoint=out.new_endpoint)
            continue
        req = out.required
        if req in (R.NO_CHANGES, R.NORMAL_SYNC):
            log("Normal sync applied (required=%d)." % req)
            return auth
        if req in (R.FULL_SYNC, R.FULL_DOWNLOAD):
            log("Full download required — pulling collection from AnkiWeb…")
            col.full_upload_or_download(auth=auth, server_usn=out.server_media_usn,
                                        upload=False)
            return auth
        if req == R.FULL_UPLOAD:
            raise SystemExit("AnkiWeb asked for a FULL UPLOAD (local is newer). "
                             "Refusing — this job never uploads. Sync your desktop "
                             "Anki to AnkiWeb first.")
        raise SystemExit("Unexpected sync state: required=%d" % req)
    raise SystemExit("Too many endpoint redirects during sync.")

def sanitize(seg):
    return re.sub(r'[<>:"\\|?*]', "_", seg.replace("/", "-").strip())

def export(col):
    os.makedirs(OUT, exist_ok=True)
    nids = col.find_notes("")
    by_deck = collections.OrderedDict()
    for nid in nids:
        note = col.get_note(nid)
        cards = note.cards()
        did = cards[0].did if cards else 1
        deck = col.decks.name(did)
        by_deck.setdefault(deck, []).append({
            "noteId": nid,
            "modelName": note.note_type()["name"],
            "tags": sorted(note.tags),
            "fields": {k: v for k, v in note.items()},
        })
    index, grand = [], 0
    today = datetime.date.today().isoformat()
    for deck, notes in by_deck.items():
        notes.sort(key=lambda x: x["noteId"])
        path = os.path.join(OUT, *[sanitize(s) for s in deck.split("::")]) + ".json"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"deck": deck, "note_count": len(notes), "exported": today,
                       "notes": notes}, f, ensure_ascii=False, indent=1)
        index.append((deck, len(notes))); grand += len(notes)
        log("  %s -> %d notes" % (deck, len(notes)))
    lines = ["# Anki collection export", "",
             f"Snapshot generated {today} from AnkiWeb via GitHub Actions "
             "(scripts/anki_cloud_export.py). One JSON file per deck; media binaries "
             "not included.", "",
             f"**Total: {grand} notes across {len(index)} decks.**", "",
             "| Deck | Notes |", "|------|------:|"]
    for deck, c in sorted(index):
        lines.append(f"| {deck} | {c} |")
    with open(os.path.join(OUT, "INDEX.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    log("TOTAL:", grand, "notes")

def main():
    hkey = (os.environ.get("ANKIWEB_HKEY") or "").strip()
    if not hkey:
        raise SystemExit("ANKIWEB_HKEY env var not set (add it as a GitHub secret).")
    raw = os.environ.get("ANKIWEB_HKEY") or ""
    log("hkey: length=%d, had_surrounding_whitespace=%s, lines=%d"
        % (len(hkey), raw != raw.strip(), len(raw.splitlines())))
    # Leave the endpoint unset for AnkiWeb: the client then defaults to
    # https://sync.ankiweb.net/ and the server redirects us to the right shard
    # (handled in sync_down). Only honor a genuine self-hosted http(s) server.
    endpoint = (os.environ.get("ANKIWEB_ENDPOINT") or "").strip()
    if not endpoint.startswith(("http://", "https://")) or "ankiweb.net" in endpoint:
        endpoint = None
    auth = SyncAuth(hkey=hkey, endpoint=endpoint)

    path = os.path.join(tempfile.mkdtemp(), "collection.anki2")
    col = Collection(path)
    try:
        sync_down(col, auth)
    finally:
        col.close()  # flush downloaded data to disk

    col = Collection(path)  # reopen with the downloaded collection
    try:
        export(col)
    finally:
        col.close()

if __name__ == "__main__":
    main()
