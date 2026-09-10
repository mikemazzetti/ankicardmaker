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

# Mint AND verify the token, then emit it base64-encoded on a single line so no
# whitespace/newline in the token can corrupt it. Password passed via env only.
OUT="$(ANKI_EMAIL="$ANKI_EMAIL" ANKI_PASS="$ANKI_PASS" "$VENV/bin/python" - <<'PY'
import os, sys, base64, tempfile
try:
    from anki.collection import Collection
    from anki.sync import SyncAuth
except Exception as e:
    sys.exit("Could not import anki: %s" % e)
col = Collection(os.path.join(tempfile.mkdtemp(), "c.anki2"))
try:
    a = col.sync_login(username=os.environ["ANKI_EMAIL"],
                       password=os.environ["ANKI_PASS"], endpoint=None)
    col.sync_status(SyncAuth(hkey=a.hkey))          # confirms the token authenticates
except Exception as e:
    sys.exit("AnkiWeb login/verify failed: %s" % e)
finally:
    col.close()
print("HKEY_B64:" + base64.b64encode(a.hkey.encode()).decode())
PY
)"
unset ANKI_PASS

B64="$(printf '%s\n' "$OUT" | sed -n 's/^HKEY_B64://p')"
[ -n "$B64" ] || { echo "Did not receive a valid token — aborting."; echo "$OUT"; exit 1; }
HKEY="$(printf '%s' "$B64" | base64 --decode)"
[ -n "$HKEY" ] || { echo "Token decode failed — aborting."; exit 1; }

printf '%s' "$HKEY" | gh secret set ANKIWEB_HKEY --repo "$REPO"
unset OUT B64 HKEY
echo "✓ Token verified and secret ANKIWEB_HKEY set on $REPO."

echo "Kicking off a test run…"
gh workflow run "anki-backup.yml" --repo "$REPO" && \
  echo "✓ Started. Watch it with:  gh run watch --repo $REPO" || \
  echo "Could not auto-start; run it from the repo's Actions tab (Run workflow)."
