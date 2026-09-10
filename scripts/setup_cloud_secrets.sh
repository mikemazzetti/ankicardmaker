#!/bin/bash
# One-time setup for the cloud daily backup. Run this ONCE on your Mac:
#
#     bash scripts/setup_cloud_secrets.sh
#
# It logs in to AnkiWeb locally (you type your password at the prompt — it is
# never stored, printed, or sent anywhere but AnkiWeb), turns that into a
# long-lived sync token, and saves the token + endpoint as GitHub repo secrets
# via the `gh` CLI. The token never appears on screen. After this, the daily
# GitHub Actions backup just works.
#
# Requirements: gh (authenticated), python3. Anki must have synced to AnkiWeb
# at least once.
set -euo pipefail

command -v gh >/dev/null || { echo "GitHub CLI (gh) not found. Install with: brew install gh"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Run 'gh auth login' first."; exit 1; }

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
[ -n "$REPO" ] || REPO="mikemazzetti/ankicardmaker"
echo "Target repo: $REPO"

VENV="${TMPDIR:-/tmp}/ankienv"
if [ ! -x "$VENV/bin/python" ]; then
  echo "Setting up a temporary Python env with the Anki library…"
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q --upgrade pip
  "$VENV/bin/pip" install -q --upgrade anki
fi

read -r -p "AnkiWeb email: " ANKI_EMAIL
read -r -s -p "AnkiWeb password (hidden): " ANKI_PASS; echo

# Mint the token in a subshell; password is passed via env, never argv/stdout.
CREDS="$(ANKI_EMAIL="$ANKI_EMAIL" ANKI_PASS="$ANKI_PASS" "$VENV/bin/python" - <<'PY'
import os, sys, tempfile
try:
    from anki.collection import Collection
except Exception as e:
    sys.exit("Could not import anki: %s" % e)
col = Collection(os.path.join(tempfile.mkdtemp(), "c.anki2"))
try:
    a = col.sync_login(username=os.environ["ANKI_EMAIL"],
                       password=os.environ["ANKI_PASS"], endpoint=None)
except Exception as e:
    sys.exit("AnkiWeb login failed: %s" % e)
finally:
    col.close()
print(a.hkey)
print(a.endpoint or "https://sync.ankiweb.net/")
PY
)"
unset ANKI_PASS

HKEY="$(printf '%s\n' "$CREDS" | sed -n 1p)"
ENDPOINT="$(printf '%s\n' "$CREDS" | sed -n 2p)"
if [ -z "$HKEY" ]; then echo "Did not receive a token — aborting."; exit 1; fi

printf '%s' "$HKEY"     | gh secret set ANKIWEB_HKEY     --repo "$REPO"
printf '%s' "$ENDPOINT" | gh secret set ANKIWEB_ENDPOINT --repo "$REPO"
unset CREDS HKEY ENDPOINT
echo "✓ Secrets ANKIWEB_HKEY and ANKIWEB_ENDPOINT set on $REPO."

echo "Kicking off a test run…"
gh workflow run "anki-backup.yml" --repo "$REPO" && \
  echo "✓ Started. Watch it with:  gh run watch --repo $REPO" || \
  echo "Could not auto-start; run it from the repo's Actions tab (Run workflow)."
