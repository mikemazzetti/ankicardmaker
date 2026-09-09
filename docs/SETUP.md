# Setup

## 1. Install the AnkiMCP add-on

The [AnkiMCP add-on](https://github.com/ankimcp/anki-mcp-server-addon) runs an MCP server
*inside* Anki, so there's nothing separate to launch and no AnkiConnect required.

1. Open Anki → **Tools → Add-ons → Get Add-ons…**
2. Paste the add-on code: **`124672614`**
3. Click OK, then **restart Anki**.
4. Confirm it's running: **Tools → AnkiMCP Server Settings**. The server listens on
   `http://127.0.0.1:3141/`.

## 2. Register the server with Claude Code

From this project folder:

```bash
claude mcp add anki --transport http http://127.0.0.1:3141/
```

Verify it's connected:

```bash
claude mcp list
```

You should see `anki` listed. The tools only respond while Anki is open.

## 3. (Optional) Quick health check

With Anki open, this should return a version number:

```bash
curl -s http://127.0.0.1:3141/ -X POST \
  -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | head -c 400
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Claude says the anki tools aren't available | Make sure **Anki is open**. The server lives inside Anki. |
| `claude mcp list` doesn't show `anki` | Re-run the `claude mcp add` command above; restart Claude Code. |
| Connection refused on `:3141` | Open **Tools → AnkiMCP Server Settings** and confirm the server is enabled. |
| Cards added but wrong deck | Deck paths are hierarchical with `::`. Give the full path, e.g. `Work::SQL`. |

## Remote access (optional)

The add-on can expose a public HTTPS tunnel (Tools → AnkiMCP Server Settings → Connect
Tunnel) if you ever want to generate cards against an Anki running on another machine.
For local use you don't need it.
