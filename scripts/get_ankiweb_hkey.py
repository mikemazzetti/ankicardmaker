#!/usr/bin/env python3
"""ONE-TIME, run on your own Mac (not in CI).

Logs in to AnkiWeb once and prints a long-lived sync token (hkey) plus the
sync endpoint. You copy those two values into GitHub repo secrets so the cloud
backup can sync WITHOUT your password. Your password is typed here, stays on
your machine, and is never stored or sent anywhere except AnkiWeb's login.

Why this exists: current Anki blocks password login from headless/CI
environments, but a pre-obtained hkey works fine there. So we get the hkey on
your Mac (which has a display) once, and CI reuses it.

Setup:
    python3 -m venv /tmp/ankienv && /tmp/ankienv/bin/pip install anki
    /tmp/ankienv/bin/python scripts/get_ankiweb_hkey.py

Then in GitHub: repo → Settings → Secrets and variables → Actions → New
repository secret, adding:
    ANKIWEB_HKEY      = (the HKEY printed below)
    ANKIWEB_ENDPOINT  = (the ENDPOINT printed below)

The token stays valid until you change your AnkiWeb password or log out of all
devices. Anki must have synced this collection to AnkiWeb at least once.
"""
import getpass, os, tempfile

try:
    from anki.collection import Collection
except ImportError:
    raise SystemExit("Install first:  python3 -m venv /tmp/ankienv && "
                     "/tmp/ankienv/bin/pip install anki  (then run with that python)")

email = input("AnkiWeb email: ").strip()
password = getpass.getpass("AnkiWeb password (hidden): ")

path = os.path.join(tempfile.mkdtemp(), "collection.anki2")
col = Collection(path)
try:
    auth = col.sync_login(username=email, password=password, endpoint=None)
finally:
    col.close()

print("\n--- copy these into GitHub repo secrets ---")
print("ANKIWEB_HKEY     =", auth.hkey)
print("ANKIWEB_ENDPOINT =", auth.endpoint or "https://sync.ankiweb.net/")
print("-------------------------------------------")
print("Keep the HKEY private — it grants sync access to your collection.")
