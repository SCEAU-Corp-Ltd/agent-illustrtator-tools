# Public Boundary

Use this repository for public notes about using Adobe Illustrator MCP server
tools with AI-assisted workflows.

## Safe To Commit

- Generic workflow notes.
- Public Adobe documentation links.
- Redacted examples.
- Small local test utilities that do not require private credentials.
- Screenshots from public documentation or fully redacted local demos.

## Keep Out

- Private project files.
- Client, collection, or internal workflow names.
- Local MCP keys, bearer tokens, auth files, and copied connection commands that
  include secrets.
- Private screenshots, document thumbnails, file paths, document titles, or
  visible local account details.
- Machine-specific setup notes, local profiles, sessions, logs, and caches.

## Working With Real Projects

Keep real project work in a separate private repository or local workspace. Use
this repo as a generic reference, then ask the AI tool you are using to adapt
the public workflow to the private project context without copying that context
back into this repository.

Before committing, check:

```powershell
git status --short
git diff --cached --name-only
```

Then search the staged content for tokens, keys, private paths, and project
names before pushing.
