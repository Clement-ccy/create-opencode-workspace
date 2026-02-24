# PROJECT KNOWLEDGE BASE

**Generated:** 2026-02-24
**Branch:** main

## OVERVIEW
CLI tool to scaffold pre-configured OpenCode workspaces natively. Built with Node.js ESM. Includes a Content Creator template supporting multi-platform bilingual creation using OpenCode native task architecture.

## STRUCTURE
```
.
├── bin/          # CLI entry point script
└── templates/    # Embedded OpenCode workspace templates
    └── content-creator/  # Primary multi-platform bilingual writing template
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| CLI Entry | `./bin/cli.js` | Uses ES modules and simple prompts. Single-file CLI. |
| Workspace Template | `./templates/content-creator/` | Self-contained OpenCode workspace. |
| Agent Orchestration | `./templates/content-creator/AGENTS.md` | Core rules for the template's Sisyphus orchestrator. |

## CONVENTIONS
- Pure Node.js ESM project (no build step for the CLI, `"type": "module"`).
- Uses `fs-extra` and `prompts`.
- Template files are copied directly.

## ANTI-PATTERNS (THIS PROJECT)
- Do not mix complex source code into `bin/cli.js` if it grows. Keep it a simple launcher.
- Do not commit `.venv` (currently ignored/present).

## COMMANDS
```bash
# Run CLI locally
npm start
# or
node ./bin/cli.js
```
