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

## Back up / sync your whole collection

Snapshot every deck in your Anki account into the repo as version-controlled JSON
(one file per deck, full note fidelity — media binaries excluded):

```bash
python3 scripts/export_anki.py
```

Output lands in [`anki-export/`](anki-export/) with an [`INDEX.md`](anki-export/INDEX.md)
listing every deck and its note count. Re-run any time and commit the diff to track how
your collection changes. Anki must be open with the AnkiMCP add-on for it to work.

### Automatic daily backup

A macOS `launchd` agent runs the export every day at **20:00** and commits + pushes only
when something changed. It skips quietly (logging) if Anki isn't open at that time.

- Job script: [`scripts/daily_sync.sh`](scripts/daily_sync.sh)
- Agent definition: [`scripts/com.mikemazzetti.ankicardmaker-sync.plist`](scripts/com.mikemazzetti.ankicardmaker-sync.plist)
  (installed copy lives at `~/Library/LaunchAgents/`)
- Log: `~/Library/Logs/ankicardmaker-sync.log`

**Change the time:** edit the `Hour`/`Minute` in the installed plist, then reload:

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.mikemazzetti.ankicardmaker-sync.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.mikemazzetti.ankicardmaker-sync.plist
```

**Run it now / disable it:**

```bash
launchctl kickstart -k gui/$(id -u)/com.mikemazzetti.ankicardmaker-sync   # run immediately
launchctl bootout   gui/$(id -u) ~/Library/LaunchAgents/com.mikemazzetti.ankicardmaker-sync.plist  # disable
```

## Layout

| Path | What it is |
|------|------------|
| [`CLAUDE.md`](CLAUDE.md) | Instructions Claude follows to turn a topic into good cards. |
| [`card-sets/`](card-sets/) | Version-controlled record of every card set generated. |
| [`card-sets/_TEMPLATE.md`](card-sets/_TEMPLATE.md) | The format each card set follows. |
| [`docs/SETUP.md`](docs/SETUP.md) | Full setup + troubleshooting. |
