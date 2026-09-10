#!/bin/bash
# Daily Anki -> GitHub backup. Run by the launchd agent
# com.mikemazzetti.ankicardmaker-sync. Exports the collection, and commits +
# pushes only if something changed. Skips quietly if Anki (the MCP server on
# :3141) isn't open. Safe to run by hand any time.
set -uo pipefail
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
REPO="/Users/mikemazzetti/ankicardmaker"
LOG="$HOME/Library/Logs/ankicardmaker-sync.log"
mkdir -p "$(dirname "$LOG")"
ts() { date '+%Y-%m-%d %H:%M:%S'; }

cd "$REPO" || { echo "$(ts) ERROR: repo $REPO not found" >>"$LOG"; exit 1; }

# Is the AnkiMCP server reachable? (connection succeeds even if it returns 406)
if ! curl -s -m 5 -o /dev/null http://127.0.0.1:3141/; then
  echo "$(ts) SKIP: AnkiMCP not reachable — is Anki open?" >>"$LOG"
  exit 0
fi

echo "$(ts) START export" >>"$LOG"
if ! python3 scripts/export_anki.py >>"$LOG" 2>&1; then
  echo "$(ts) ERROR: export failed" >>"$LOG"; exit 1
fi

if [ -n "$(git status --porcelain anki-export)" ]; then
  git add anki-export
  git commit -q -m "backup: daily Anki sync $(date +%F)

Automated snapshot via scripts/daily_sync.sh.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>" >>"$LOG" 2>&1
  if git push -q origin main >>"$LOG" 2>&1; then
    echo "$(ts) OK: pushed changes" >>"$LOG"
  else
    echo "$(ts) ERROR: git push failed" >>"$LOG"; exit 1
  fi
else
  echo "$(ts) OK: no changes to back up" >>"$LOG"
fi
