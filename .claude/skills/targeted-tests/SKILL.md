---
name: targeted-tests
description: Choose and run the smallest relevant test, typecheck or lint command after a code change. Use when verifying a specific change.
---
# Targeted verification
1. Identify test framework from existing project configuration, without scanning unrelated files.
2. Run directly related test file or case first.
3. Run a narrow lint/typecheck if supported.
4. Expand to full suite only for cross-cutting changes or when focused checks indicate risk.
5. Capture concise failure excerpts, not huge logs.
6. State precisely what passed, failed or was not run.
