# ankicardmaker

Generate high-quality [Anki](https://apps.ankiweb.net/) flashcards from a topic, by
conversation. You tell Claude Code a topic; Claude drafts well-formed cards, saves a
version-controlled copy here, and pushes them straight into Anki via the
[AnkiMCP](https://github.com/ankimcp/anki-mcp-server-addon) server.

No AnkiConnect, no manual CSV import — Anki just needs to be open.

## How you use it

Open this folder in Claude Code and say something like:

> Make 15 cards on the Krebs cycle in `Biology::Biochemistry`.

Claude will:

1. Draft the cards to a Markdown file under [`card-sets/`](card-sets/) (your source of truth).
2. Create the deck if needed and push the cards into Anki via AnkiMCP.
3. Commit the new card set so you have a durable, reviewable record.

You review the cards in Anki like any others. Re-run any time to add more.

## One-time setup

See [docs/SETUP.md](docs/SETUP.md). In short:

1. **Install the AnkiMCP add-on** in Anki — Tools → Add-ons → Get Add-ons → code `124672614`, then restart Anki. It runs an MCP server at `http://127.0.0.1:3141/`.
2. **Register it with Claude Code** (from this folder):
   ```bash
   claude mcp add anki --transport http http://127.0.0.1:3141/
   ```
3. **Keep Anki running** whenever you want to generate cards — the server lives inside Anki.

## Layout

| Path | What it is |
|------|------------|
| [`CLAUDE.md`](CLAUDE.md) | Instructions Claude follows to turn a topic into good cards. |
| [`card-sets/`](card-sets/) | Version-controlled record of every card set generated. |
| [`card-sets/_TEMPLATE.md`](card-sets/_TEMPLATE.md) | The format each card set follows. |
| [`docs/SETUP.md`](docs/SETUP.md) | Full setup + troubleshooting. |
