# CLAUDE.md — how to make cards in this repo

This repo turns a **topic** into **Anki flashcards**. When the user gives you a topic,
follow this workflow. Optimize for cards the user will actually retain, not coverage.

## Workflow

1. **Confirm the target deck.** Use the deck the user names (e.g. `Languages::Spanish`).
   If they don't name one, propose a deck path and ask before creating it. Anki decks are
   hierarchical with `::` as the separator.
2. **Check the connection.** The AnkiMCP tools (server `anki`, `http://127.0.0.1:3141/`)
   only work while Anki is open. If the tools error or aren't available, tell the user to
   open Anki (and see `docs/SETUP.md`) rather than silently faking it.
3. **Avoid duplicates.** Before adding, use the find-notes tool to search the deck for
   cards on the same concept. Skip or update near-duplicates instead of re-adding.
4. **Draft the card set to a file first.** Write the cards to
   `card-sets/<Deck__Path>/<topic-slug>.md` following `card-sets/_TEMPLATE.md`. This is the
   version-controlled source of truth; write it before pushing so nothing is lost.
5. **Push to Anki** via AnkiMCP: create the deck if needed, then add the notes. Use the
   note type that fits (Basic, or Basic-and-reversed for facts worth testing both ways;
   Cloze for fill-in-the-blank). Tag every note with `ankicardmaker` plus a topic tag.
6. **Report** what was added: deck, count, note type, and the file path. Then commit the
   new/changed card-set file with a message like `cards: <topic> (<deck>)`.

## What makes a good card (follow these)

- **One fact per card.** If a card has "and" in the answer, it's probably two cards.
- **Minimum information principle.** Short question, short answer. Break big ideas apart.
- **Ask for retrieval, not recognition.** Prefer "What enzyme catalyzes X?" over
  "Is Y the enzyme for X? (T/F)".
- **Make the front unambiguous.** The question should have exactly one correct answer and
  enough context to know what's being asked.
- **Use cloze deletions** for definitions, sequences, and lists — e.g.
  `The {{c1::mitochondrion}} is the powerhouse of the cell.`
- **Prefer understanding over verbatim.** Test why/how, not just rote strings, unless the
  string itself is the point (vocabulary, dates, formulas).
- **Add examples and hints** in a separate field where they aid recall; keep them off the
  answer side.
- **No trivia the user won't use.** Tie cards to the user's actual goal for the topic.

## Note types & fields

- **Basic**: `Front`, `Back`. Default for Q→A facts.
- **Basic (and reversed card)**: for facts worth recalling in both directions (term↔definition, word↔translation).
- **Cloze**: `Text`, `Back Extra`. For fill-in-the-blank, lists, sequences.

If the user needs a custom note type, create it via the model tools, but prefer the
built-ins unless there's a clear reason.

## Conventions

- **Tags:** always `ankicardmaker`; add a lowercase topic tag (e.g. `spanish`, `krebs-cycle`).
- **Card-set filenames:** slugified topic under a folder named for the deck with `::`
  replaced by `__`, e.g. deck `Biology::Biochemistry` → `card-sets/Biology__Biochemistry/krebs-cycle.md`.
- **Count:** if the user doesn't say how many, aim for 10–20 focused cards and offer more.
- **Commit** after each successful push so the repo mirrors what's in Anki.
