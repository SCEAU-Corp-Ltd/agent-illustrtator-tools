# AI Tool Connections

Adobe documents the Illustrator MCP server as a Beta feature for connecting
desktop AI tools to Illustrator (Beta).

The public workflow in this repository uses Illustrator tools from the Adobe MCP
server, with automation handled through Codex. Other tools can connect to the
same Adobe MCP server concept when they support the required MCP connection
shape.

## Tool Notes

| AI tool | Public note |
|---|---|
| Codex | Use the Adobe MCP server connection and ask Codex to adapt the workflow into Codex-compatible tool calls. |
| Illustrator Claw | Point an Illustrator Claw workspace at this repo, configure MCP servers privately, and keep tokens out of git. Start with `docs/illustrator-claw-public-setup.md`; Codex-compatible agents can use `skills/illustrator-claw/SKILL.md` as `$illustrator-claw`. |
| Claude Code | Adobe documents Claude Code as a supported desktop AI tool path. Ask Claude Code to adapt the workflow to its MCP command format. |
| Cursor | Adobe documents Cursor as a supported desktop AI tool path. Ask Cursor to adapt the workflow to its MCP settings format. |
| Other tools | Use the Adobe MCP server URL/key pattern only if the tool supports compatible MCP configuration. Ask the AI tool to adjust the workflow accordingly. |

## Public Safety

Do not paste real MCP keys or full connection commands into this repository.
Connection commands can include authentication material unique to an Illustrator
(Beta) installation.

For Illustrator Claw, keep workspace names, hostnames, bearer tokens, API keys, local
paths, and agent logs in private Illustrator Claw state. Public docs should explain what
needs to exist and how to verify it, without copying the private values.

## Official References

- [About using desktop AI tools with Adobe Illustrator (Beta)](https://helpx.adobe.com/au/illustrator/desktop/connect-with-other-apps-and-tools/about-using-ai-tools-with-illustrator.html)
- [Connect Adobe Illustrator (Beta) to AI tools](https://helpx.adobe.com/illustrator/desktop/connect-with-other-apps-and-tools/connect-illustrator-to-ai-tools.html)
- [Work with Adobe Illustrator (Beta) documents from AI tools](https://helpx.adobe.com/illustrator/desktop/connect-with-other-apps-and-tools/work-with-illustrator-documents-from-ai-tools.html)
