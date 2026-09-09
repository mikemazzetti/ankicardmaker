# card-sets

The version-controlled record of every card set generated in this repo. Each file mirrors
a batch of notes pushed into Anki, so you can review, diff, re-import, and avoid
regenerating the same material.

## Structure

```
card-sets/
  _TEMPLATE.md                     # the format every card set follows
  <Deck__Path>/<topic-slug>.md     # one file per topic
```

The folder name is the Anki deck path with `::` replaced by `__`. For example, deck
`Biology::Biochemistry`, topic "Krebs cycle" →
`card-sets/Biology__Biochemistry/krebs-cycle.md`.

## Workflow reminder

Claude writes the card-set file **before** pushing to Anki, then commits it after a
successful push — so this folder stays a faithful mirror of your Anki collection. See
[`../CLAUDE.md`](../CLAUDE.md) for the full card-quality rules.
