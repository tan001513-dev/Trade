---
name: smart-debug
description: Diagnose a specific bug using narrow searches, focused reproduction and minimal fixes. Use when a user reports a bug or failing test.
---
# Focused debugging
1. Get exact symptoms, command, error and expected behavior if missing.
2. Locate likely entry points using file names and symbol search; do not dump the repository.
3. Reproduce with the smallest feasible command and truncated relevant output.
4. Inspect only the affected functions and their immediate callers.
5. Fix root cause with a small patch, then run the focused regression test.
6. Summarize cause, fix and verification briefly. Escalate scope only with evidence.
