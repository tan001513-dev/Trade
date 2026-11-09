---
name: token-audit
description: Audit Claude Code context overhead and suggest low-risk reductions to instructions, skills, MCP tools and workflow. Use when explicitly asked to optimize token usage.
disable-model-invocation: true
---
# Token audit
1. Ask user to inspect /usage and /context; do not invent measurements.
2. Identify overly long always-loaded CLAUDE.md files and repeated instructions.
3. Check unnecessary enabled MCP servers and plugins; propose disabling unused ones.
4. Suggest moving procedures into on-demand skills and narrowing file/tool outputs.
5. Prioritize changes by expected impact, implementation effort and risk.
6. Never remove user configuration or disable integrations without consent.
