#!/usr/bin/env python3
"""Reorganize the LeetCode / NeetCode decks into NeetCode roadmap order.

Anki sorts decks alphabetically, so the roadmap sequence is encoded as a number
prefix on each topic subdeck ("01 Arrays & Hashing" ... "18 Bit Manipulation").
The order is the one neetcode.io uses for both NeetCode 150 and NeetCode 250.

Resulting layout (list-first: each list stays studiable on its own):

    Interview::LeetCode::NeetCode150::01 Arrays & Hashing ... 18 Bit Manipulation
    Interview::LeetCode::Extra::01 Arrays & Hashing       ... 18 Bit Manipulation
    Interview::LeetCode::Extra::99 Off-Roadmap::{SQL & Database, Concurrency & Shell, Unsorted}
    Interview::NeetCode 250::01 Arrays & Hashing          ... 18 Bit Manipulation

NeetCode150 and NeetCode 250 notes already sit in a correctly-named topic subdeck,
so they are only renumbered — nothing is reclassified. The ~2.5k problems sitting
loose in the flat LeetCode deck have no roadmap topic recorded anywhere, so they
are bucketed from their LeetCode topic tags (see classify()); measured against the
150 notes whose true bucket is known, that heuristic agrees ~79% of the time.
Every moved note also gets a `roadmap::NN-topic` tag so a wrong call is easy to
find and fix later.

Usage:
    python3 scripts/neetcode_roadmap.py --plan            # offline, from anki-export/
    python3 scripts/neetcode_roadmap.py --apply --dry-run # live read, no writes
    python3 scripts/neetcode_roadmap.py --apply           # live, moves + tags notes

--apply needs Anki open with the AnkiMCP add-on (http://127.0.0.1:3141/).
"""
import json, os, re, sys, csv, glob, urllib.request, urllib.error

URL = "http://127.0.0.1:3141/"
EXPORT = "anki-export"
PLAN = "docs/neetcode-roadmap-plan.csv"

# ---------------------------------------------------------------- roadmap order
# Confirmed from neetcode.io/practice on 2026-09-17; NC150 and NC250 share it.
ROADMAP = [
    "Arrays & Hashing", "Two Pointers", "Sliding Window", "Stack", "Binary Search",
    "Linked List", "Trees", "Heap - Priority Queue", "Backtracking", "Tries",
    "Graphs", "Advanced Graphs", "1-D Dynamic Programming", "2-D Dynamic Programming",
    "Greedy", "Intervals", "Math & Geometry", "Bit Manipulation",
]
NUM = {name: f"{i:02d} {name}" for i, name in enumerate(ROADMAP, 1)}
OFF_ROADMAP = ["SQL & Database", "Concurrency & Shell", "Unsorted"]

# Existing subdeck names in the collection that mean the same roadmap topic.
ALIASES = {
    "1-D DP": "1-D Dynamic Programming", "2-D DP": "2-D Dynamic Programming",
    "Heap / Priority Queue": "Heap - Priority Queue",
    "Heap - Priority Queue": "Heap - Priority Queue",
}

# ------------------------------------------------------------------ classifier
# First matching rule wins, ordered most-specific technique -> most generic.
RULES = [
    ("Tries",                   {"trie", "suffix-array"}),
    ("Advanced Graphs",         {"minimum-spanning-tree", "shortest-path",
                                 "strongly-connected-component", "eulerian-circuit",
                                 "biconnected-component"}),
    ("Graphs",                  {"graph"}),          # + special cases, see classify()
    ("Backtracking",            {"backtracking"}),
    ("2-D Dynamic Programming", None),               # special, see classify()
    ("1-D Dynamic Programming", {"dynamic-programming", "memoization", "bitmask",
                                 "game-theory"}),
    ("Trees",                   {"tree", "binary-tree", "binary-search-tree",
                                 "segment-tree", "binary-indexed-tree",
                                 "depth-first-search", "breadth-first-search"}),
    ("Heap - Priority Queue",   {"heap-priority-queue", "quickselect"}),
    ("Stack",                   {"monotonic-stack", "stack"}),
    ("Linked List",             {"linked-list", "doubly-linked-list"}),
    ("Sliding Window",          {"sliding-window", "monotonic-queue"}),
    ("Two Pointers",            {"two-pointers"}),
    ("Binary Search",           {"binary-search"}),
    ("Intervals",               {"line-sweep"}),
    ("Greedy",                  {"greedy"}),
    ("Bit Manipulation",        {"bit-manipulation"}),
    ("Math & Geometry",         {"geometry", "number-theory", "combinatorics",
                                 "probability-and-statistics", "randomized",
                                 "brainteaser", "rejection-sampling",
                                 "reservoir-sampling", "math", "matrix"}),
    ("Arrays & Hashing",        {"array", "hash-table", "string", "sorting",
                                 "prefix-sum", "counting", "hash-function",
                                 "ordered-set", "enumeration", "simulation",
                                 "divide-and-conquer", "recursion", "queue",
                                 "string-matching", "rolling-hash", "merge-sort",
                                 "bucket-sort", "counting-sort", "radix-sort",
                                 "data-stream", "iterator", "design"}),
]
OVERFLOW = [("SQL & Database", {"database"}),
            ("Concurrency & Shell", {"concurrency", "shell"})]

# Grid DP, or DP over two sequences (edit distance, LCS) -> 2-D. DP over one string stays 1-D.
TWO_SEQ_RE = re.compile(r"two |common|distinct|interleav|edit dist|matching", re.I)
# LeetCode has no "intervals" tag, so interval problems are recognised by title.
INTERVAL_RE = re.compile(r"\binterval|meeting room|my calendar|car pooling|\bmerge ranges", re.I)


def classify(tags, title=""):
    """Map a LeetCode problem's topic tags to one roadmap bucket."""
    t = {x for x in tags if not x.startswith("difficulty-")}
    for name, keys in OVERFLOW:
        if t & keys:
            return name
    if INTERVAL_RE.search(title or ""):
        return "Intervals"
    for name, keys in RULES:
        if name == "Graphs":
            # union-find and grid traversal are NeetCode "Graphs", and topological
            # sort is too (Course Schedule) — Advanced Graphs is Dijkstra/MST/Eulerian.
            if t & keys or t & {"union-find", "topological-sort"} or (
                    {"depth-first-search", "breadth-first-search"} & t and "matrix" in t):
                return name
            continue
        if name == "2-D Dynamic Programming":
            if "dynamic-programming" in t and (
                    "matrix" in t or ("string" in t and TWO_SEQ_RE.search(title or ""))):
                return name
            continue
        if t & keys:
            return name
    return "Unsorted"


def tag_for(bucket):
    """`roadmap::07-trees`, or `roadmap::99-off-roadmap` for the non-path buckets."""
    if bucket in NUM:
        slug = re.sub(r"[^a-z0-9]+", "-", bucket.lower()).strip("-")
        return f"roadmap::{ROADMAP.index(bucket) + 1:02d}-{slug}"
    return "roadmap::99-off-roadmap"


def target_subpath(bucket):
    """Deck path fragment under the list root, e.g. '07 Trees' or '99 Off-Roadmap::Unsorted'."""
    return NUM[bucket] if bucket in NUM else f"99 Off-Roadmap::{bucket}"


# ------------------------------------------------------------------- MCP client
# AnkiMCP groups operations under umbrella tools taking an "action":
#   card_management {params:{action:"change_deck", card_ids:[...], deck:"..."}}  <- CARD ids
#   tag_management  {params:{action:"add_tags",    note_ids:[...], tags:"a b"}}  <- NOTE ids
# The action args are nested under "params" (a discriminated union), and change_deck
# takes CARD ids while add_tags takes NOTE ids.
_id = [0]


def _post(method, params=None, notify=False):
    _id[0] += 1
    body = {"jsonrpc": "2.0", "method": method}
    if not notify:
        body["id"] = _id[0]
    if params is not None:
        body["params"] = params
    req = urllib.request.Request(
        URL, data=json.dumps(body).encode(),
        headers={"content-type": "application/json",
                 "accept": "application/json, text/event-stream"}, method="POST")
    with urllib.request.urlopen(req, timeout=180) as r:
        raw = r.read().decode()
    if notify:
        return None
    if "data:" in raw:
        for line in raw.splitlines():
            if line.startswith("data:"):
                raw = line[5:].strip()
    return json.loads(raw)


def call(name, arguments):
    r = _post("tools/call", {"name": name, "arguments": arguments})
    if "error" in r:
        raise SystemExit(f"TOOL ERROR {name}: {json.dumps(r['error'])}")
    res = r["result"]
    if res.get("isError"):
        raise SystemExit(f"TOOL ERROR {name}: {json.dumps(res)[:500]}")
    return res.get("structuredContent", res)


def connect():
    try:
        _post("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                             "clientInfo": {"name": "neetcode-roadmap", "version": "1"}})
    except (urllib.error.URLError, ConnectionError) as e:
        raise SystemExit(
            f"Cannot reach AnkiMCP at {URL} ({e}).\n"
            "Open Anki (with the AnkiMCP add-on) and re-run. See docs/SETUP.md.")
    _post("notifications/initialized", notify=True)
    tools = {t["name"] for t in _post("tools/list")["result"]["tools"]}
    missing = {"list_decks", "find_notes", "notes_info",
               "card_management", "tag_management"} - tools
    if missing:
        raise SystemExit(f"AnkiMCP is missing {sorted(missing)}. Available: {sorted(tools)}")


def find_note_ids(query):
    ids, offset = [], 0
    while True:
        r = call("find_notes", {"query": query, "limit": 500, "offset": offset})
        batch = r.get("noteIds", [])
        ids.extend(batch)
        if not r.get("hasMore") or not batch:
            break
        offset += len(batch)
    return ids


def chunked(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def notes_detail(note_ids):
    """Yield (noteId, cardIds, tags, title) for each note."""
    for batch in chunked(note_ids, 100):
        for n in call("notes_info", {"notes": batch})["notes"]:
            fields = n.get("fields") or {}
            title = fields.get("title") or fields.get("Front") or ""
            if isinstance(title, dict):
                title = title.get("value", "")
            yield n["noteId"], n.get("cards", []), n.get("tags", []), title


# ---------------------------------------------------------------------- --apply
def apply_live(dry_run):
    connect()
    decks = [d["name"] for d in call("list_decks", {})["decks"]]

    def root_for(leaf):
        hits = [d for d in decks if d == leaf or d.endswith("::" + leaf)]
        if not hits:
            raise SystemExit(f"No deck named or ending in '{leaf}'. Decks: {sorted(decks)}")
        return min(hits, key=len)

    lc_root = root_for("LeetCode")
    nc150_root = root_for("NeetCode150")
    nc250_root = root_for("NeetCode 250")
    print(f"roots: {lc_root!r} | {nc150_root!r} | {nc250_root!r}\n")

    moves = {}   # target deck -> [card ids]
    tags = {}    # tag -> [note ids]
    rows = []    # executed plan, written to PLAN so the move is reversible
    seen = 0

    def stage(deck, bucket, card_ids, note_ids):
        if card_ids:
            moves.setdefault(deck, []).extend(card_ids)
        if note_ids:
            tags.setdefault(tag_for(bucket), []).extend(note_ids)

    # 1. NeetCode150 + NeetCode 250 -- topic already known, renumber only.
    for root in (nc150_root, nc250_root):
        for sub in sorted(d for d in decks if d.startswith(root + "::")):
            leaf = sub[len(root) + 2:]
            if "::" in leaf or re.match(r"^\d\d ", leaf):
                continue                      # nested, or already renumbered
            topic = ALIASES.get(leaf, leaf)
            if topic not in NUM:
                print(f"  ! unrecognised subdeck, skipping: {sub!r}")
                continue
            note_ids = find_note_ids(f'deck:"{sub}" -deck:"{sub}::*"')
            cards, notes = [], []
            for nid, cids, _t, title in notes_detail(note_ids):
                cards.extend(cids)
                notes.append(nid)
                rows.append((nid, title[:80], sub, f"{root}::{NUM[topic]}", topic, "official"))
            seen += len(notes)
            stage(f"{root}::{NUM[topic]}", topic, cards, notes)
            print(f"  {len(notes):5} {leaf:26} -> {NUM[topic]}")

    # 2. The flat LeetCode deck -- bucket from LeetCode topic tags.
    loose = find_note_ids(f'deck:"{lc_root}" -deck:"{lc_root}::*"')
    print(f"\n  {len(loose)} notes loose in {lc_root!r}, classifying...")
    hist = {}
    for nid, cids, ntags, title in notes_detail(loose):
        bucket = classify(ntags, title)
        hist[bucket] = hist.get(bucket, 0) + 1
        seen += 1
        dest = f"{lc_root}::Extra::{target_subpath(bucket)}"
        rows.append((nid, title[:80], lc_root, dest, bucket, "heuristic"))
        stage(dest, bucket, cids, [nid])
    for b in ROADMAP + OFF_ROADMAP:
        if hist.get(b):
            print(f"  {hist[b]:5} {b}")

    total_cards = sum(len(v) for v in moves.values())
    print(f"\n{seen} notes / {total_cards} cards -> {len(moves)} decks")
    os.makedirs(os.path.dirname(PLAN), exist_ok=True)
    with open(PLAN, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["noteId", "title", "from_deck", "to_deck", "bucket", "source"])
        w.writerows(rows)
    print(f"executed plan -> {PLAN}")
    if dry_run:
        for deck in sorted(moves):
            print(f"  {len(moves[deck]):5}  {deck}")
        print("\n--dry-run: nothing written.")
        return

    for i, deck in enumerate(sorted(moves), 1):
        ids = moves[deck]
        for batch in chunked(ids, 200):
            call("card_management", {"params": {"action": "change_deck",
                                               "card_ids": batch, "deck": deck}})
        print(f"  [{i:2}/{len(moves)}] moved {len(ids):5} cards -> {deck}")
    for tag, ids in sorted(tags.items()):
        for batch in chunked(sorted(set(ids)), 200):
            call("tag_management", {"params": {"action": "add_tags",
                                              "note_ids": batch, "tags": tag}})
    print(f"\nDone. {total_cards} cards moved, {len(tags)} roadmap tags applied.")
    print("Old subdecks are now empty -- delete them from Anki's deck list when happy.")
    print("Then: python3 scripts/export_anki.py   to refresh the snapshot.")


if __name__ == "__main__":
    if "--plan" in sys.argv:
        plan_offline()
    elif "--apply" in sys.argv:
        apply_live("--dry-run" in sys.argv)
    else:
        print(__doc__)
        sys.exit(2)
