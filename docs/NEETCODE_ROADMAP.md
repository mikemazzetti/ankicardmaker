# NeetCode roadmap ordering

Anki sorts decks alphabetically, which scrambles a curriculum. The LeetCode and
NeetCode decks are therefore numbered so that alphabetical order *is* the
recommended NeetCode path.

## The order

Confirmed from [neetcode.io/practice](https://neetcode.io/practice) on 2026-09-17.
NeetCode 150 and NeetCode 250 list their topics in the same sequence, so one
numbering serves both.

| # | Topic | Depends on |
|---|-------|------------|
| 01 | Arrays & Hashing | — |
| 02 | Two Pointers | Arrays & Hashing |
| 03 | Sliding Window | Two Pointers |
| 04 | Stack | Arrays & Hashing |
| 05 | Binary Search | Two Pointers |
| 06 | Linked List | Two Pointers |
| 07 | Trees | Binary Search, Linked List |
| 08 | Heap / Priority Queue | Trees |
| 09 | Backtracking | Trees |
| 10 | Tries | Trees |
| 11 | Graphs | Backtracking |
| 12 | Advanced Graphs | Graphs, Heap |
| 13 | 1-D Dynamic Programming | Backtracking |
| 14 | 2-D Dynamic Programming | 1-D DP, Graphs |
| 15 | Greedy | 1-D DP |
| 16 | Intervals | Greedy |
| 17 | Math & Geometry | Bit Manipulation |
| 18 | Bit Manipulation | 1-D DP |

`Heap / Priority Queue` is spelled `Heap - Priority Queue` in deck names — Anki
treats `/` as a path character in some contexts and the export script sanitizes it.

## Deck layout

List-first: each list stays studiable on its own, and the roadmap order shows up
inside it.

```
Interview::LeetCode
├── NeetCode150
│   ├── 01 Arrays & Hashing            9
│   ├── 02 Two Pointers                5
│   └── … 18 Bit Manipulation          7      (150 total)
└── Extra
    ├── 01 Arrays & Hashing          417
    ├── 02 Two Pointers              118
    ├── … 18 Bit Manipulation         64      (2,289 on-roadmap)
    └── 99 Off-Roadmap
        ├── SQL & Database           226
        ├── Concurrency & Shell       13
        └── Unsorted                  41

Interview::NeetCode 250
├── 01 Arrays & Hashing               22
└── … 18 Bit Manipulation             10      (250 total)
```

`Extra` is the ~2.5k imported LeetCode problems that are not part of NeetCode 150.
`99 Off-Roadmap` sorts last so it never interrupts the path.

## How topics are assigned

- **NeetCode 150 and NeetCode 250** already sit in a correctly named topic subdeck.
  They are only renumbered — nothing is reclassified, so these are exact.
- **The `Extra` problems** have no roadmap topic recorded anywhere, only LeetCode's
  own topic tags. `classify()` in `scripts/neetcode_roadmap.py` maps those tags to a
  bucket, first-match-wins from most specific technique to most generic container.

  Measured against the 150 notes whose true bucket is known, the heuristic agrees
  **~79%** of the time. It is weakest on 1-D vs 2-D DP and on problems NeetCode
  files by intended solution rather than by tag (Maximum Subarray is tagged
  `dynamic-programming` but NeetCode calls it Greedy).

  Every moved note gets a `roadmap::NN-topic` tag, so a misfiled card is easy to
  find (`tag:roadmap::13-1-d-dynamic-programming`) and re-file.

## Status

**Applied 2026-09-17**: 2,969 cards moved into 57 decks and tagged, verified against
the live collection (0 notes left loose in `Interview::LeetCode`, 2,969 carrying a
`roadmap::` tag), then synced to AnkiWeb.

## Running it

```bash
python3 scripts/neetcode_roadmap.py --plan             # offline, from anki-export/
python3 scripts/neetcode_roadmap.py --apply --dry-run  # live read, prints moves, writes nothing
python3 scripts/neetcode_roadmap.py --apply            # moves and tags the notes
```

`--apply` needs Anki open with the AnkiMCP add-on (see `SETUP.md`). It discovers the
current deck roots at run time rather than trusting `anki-export/`, and writes the
mapping it actually executed to `neetcode-roadmap-plan.csv`, so a move can be traced
or undone per note.

AnkiMCP nests umbrella-tool arguments under `params`, and `card_management.change_deck`
takes **card** ids while `tag_management.add_tags` takes **note** ids — `notes_info`
supplies both. It is re-runnable: already-numbered subdecks are skipped.

## Leftovers

The 36 old topic subdecks are still there, now empty. AnkiMCP has no delete-deck tool,
so remove them from Anki's Debug Console (`Cmd+Shift+;`, run with `Cmd+Return`):

```python
import re
gone = [d.id for d in mw.col.decks.all_names_and_ids()
        if re.match(r"^Interview::(LeetCode::NeetCode150|NeetCode 250)::", d.name)
        and not re.match(r"^\d\d ", d.name.split("::")[-1])
        and not mw.col.find_cards(f'deck:"{d.name}"')]
mw.col.decks.remove(gone); mw.reset(); len(gone)
```

Then sync, and re-run `scripts/export_anki.py` to refresh the snapshot (or let the
daily GitHub Action do it from AnkiWeb).
