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

### Automatic daily backup (cloud, via GitHub Actions)

A scheduled GitHub Actions workflow downloads your collection **from AnkiWeb** and commits
the export daily — so it runs even when your Mac is off. Your cards must be synced to
AnkiWeb, and the job needs a one-time sync token (never your password).

**One-time setup:**

1. Make sure your desktop Anki syncs to AnkiWeb at least once.
2. On your Mac, get a sync token:
   ```bash
   python3 -m venv /tmp/ankienv && /tmp/ankienv/bin/pip install anki
   /tmp/ankienv/bin/python scripts/get_ankiweb_hkey.py
   ```
   It asks for your AnkiWeb email/password (typed locally, never stored) and prints an
   `ANKIWEB_HKEY` and `ANKIWEB_ENDPOINT`.
3. In GitHub: repo → **Settings → Secrets and variables → Actions → New repository secret**,
   and add both `ANKIWEB_HKEY` and `ANKIWEB_ENDPOINT`.
4. Done. The workflow ([`.github/workflows/anki-backup.yml`](.github/workflows/anki-backup.yml))
   runs daily (~08:17 UTC) and on demand (Actions tab → **Run workflow**). It only ever
   *downloads* from AnkiWeb — it never uploads or changes your collection.

The token stays valid until you change your AnkiWeb password or log out of all devices.

### Optional: local backup instead

If you'd rather back up straight from the desktop app (no AnkiWeb, no token), a macOS
`launchd` agent is included: [`scripts/daily_sync.sh`](scripts/daily_sync.sh) +
[`scripts/com.mikemazzetti.ankicardmaker-sync.plist`](scripts/com.mikemazzetti.ankicardmaker-sync.plist).
It runs the local exporter on a schedule but only works while your Mac is on with Anki
open. Install it with:

```bash
cp scripts/com.mikemazzetti.ankicardmaker-sync.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.mikemazzetti.ankicardmaker-sync.plist
```

(It is **not** installed by default — the cloud workflow above is the recommended path.)

## Layout

| Path | What it is |
|------|------------|
| [`CLAUDE.md`](CLAUDE.md) | Instructions Claude follows to turn a topic into good cards. |
| [`card-sets/`](card-sets/) | Version-controlled record of every card set generated. |
| [`card-sets/_TEMPLATE.md`](card-sets/_TEMPLATE.md) | The format each card set follows. |
| [`docs/SETUP.md`](docs/SETUP.md) | Full setup + troubleshooting. |
