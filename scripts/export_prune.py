#!/usr/bin/env python3
"""Delete snapshot files for decks that no longer exist.

Both exporters write one JSON per current deck and never remove anything, so
`anki-export/` accumulates files for decks that were renamed or deleted — at one
point it held two full generations of the collection side by side. `prune()` is
called at the end of an export with the set of files that export just wrote;
everything else under the output directory goes.

It refuses to run on an empty `kept` set, so a failed or partial export can never
wipe the snapshot.
"""
import os

KEEP_NAMES = {"INDEX.md"}


def prune(out_dir, kept, log=print):
    """Remove *.json under out_dir that are not in `kept`, then drop empty dirs.

    kept: iterable of paths just written by the exporter (any form os.path can
          normalise). Returns the list of removed paths.
    """
    kept = {os.path.normpath(os.path.abspath(p)) for p in kept}
    if not kept:
        log("prune: refusing to run — the export wrote no files "
            "(failed or partial run?); snapshot left untouched.")
        return []

    stale = []
    for root, _dirs, files in os.walk(out_dir):
        for fn in files:
            if fn in KEEP_NAMES or not fn.endswith(".json"):
                continue
            p = os.path.normpath(os.path.abspath(os.path.join(root, fn)))
            if p not in kept:
                stale.append(p)

    for p in sorted(stale):
        os.remove(p)
        log("  pruned %s" % os.path.relpath(p, out_dir))

    # drop directories left empty, deepest first
    for root, dirs, _files in os.walk(out_dir, topdown=False):
        for d in dirs:
            p = os.path.join(root, d)
            if not os.listdir(p):
                os.rmdir(p)
                log("  pruned empty dir %s/" % os.path.relpath(p, out_dir))

    log("prune: removed %d stale file(s); %d kept." % (len(stale), len(kept)))
    return stale
