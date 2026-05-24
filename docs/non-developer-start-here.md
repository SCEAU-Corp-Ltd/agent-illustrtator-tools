# Non-Developer Start Here

This page is for designers, operators, and project stakeholders who want to use this repository without needing engineering experience.

## In One Sentence

This repository is a practical guide for using AI assistants with Adobe Illustrator (Beta) in a safe, repeatable way.

## What You Can Do With It

- Recolor artwork with AI-guided workflows
- Follow setup checklists for AI tools that support Adobe MCP
- Run optional visual quality checks on exported PNG files
- Share the same documented process across teams

## What You Do Not Need To Do

- You do not need to write code to use the main workflows
- You do not need to install Node packages or Python dependencies for the docs
- You do not need to edit any YAML files unless you are publishing integrations

## First 3 Steps

1. Read Adobe's "connect Illustrator to AI tools" instructions:
   - https://helpx.adobe.com/illustrator/desktop/connect-with-other-apps-and-tools/connect-illustrator-to-ai-tools.html
2. Open `docs/ai-tool-connections.md` and pick your AI tool path.
3. Run `workflows/illustrator-recolor.md` as your first hands-on workflow.

## If You Only Read Two Files

- `docs/ai-tool-connections.md`
- `workflows/illustrator-recolor.md`

## Keep Private Information Out Of This Repo

Never store these in this repository:

- API keys, bearer tokens, and secrets
- Client files, private screenshots, and internal project names
- Local machine paths and logs

Read `docs/public-boundary.md` before sharing or committing changes.

## Common Questions

### "Is this an app I install?"

No. It is a documentation and workflow repository.

### "Will this modify Illustrator directly?"

The workflows are designed around Adobe Illustrator (Beta) MCP-enabled operations. Your AI assistant orchestrates the actions.

### "Where do I start if I get stuck?"

Return to:

- `docs/ai-tool-connections.md` for setup issues
- `workflows/illustrator-recolor.md` for workflow issues
- Adobe official guides linked above for Illustrator MCP connection steps
