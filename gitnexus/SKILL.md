---
name: gitnexus
description: "Use GitNexus for codebase exploration, debugging, planning, impact analysis, and review only when the active checkout is confirmed as indexed."
---

# GitNexus workflow

Use GitNexus for codebase exploration, cross-file debugging, planning changes, impact analysis, and review when it can add useful signal. Skip it for trivial, isolated tasks.

## Applicability and index gate

- Apply this skill's GitNexus workflow only after `list_repos` confirms an index for the active project's **full path**. An index for another checkout with the same repository name is not a match.
- Before using any other GitNexus tool or delegating a GitNexus-relevant task, call `list_repos` and match the active project by its full path.
- If the active checkout is not indexed, do not use other GitNexus tools. Explain that GitNexus is unavailable for this checkout and offer the user `gitnexus analyze --index-only`. This creates a local GitNexus index without injecting instructions into `AGENTS.md`/`CLAUDE.md` or installing project skills. Do not run the indexing command or start Planner while waiting for the user's choice; the user can run it from the repository root or decline.
- If the user declines, continue without GitNexus. If the user runs the command, recheck `list_repos` and confirm the full path before using GitNexus.
- Check reported freshness and coverage when available. If the index is stale or ambiguous, say so and continue with ordinary file search and source inspection; do not independently launch indexing or repeatedly prompt the user.

## Specialist agents

- Use GitNexus only for the active checkout's matching index. Pass Planner the matching repository path/name and the index timestamp/commit when available. Do not claim the index is fresh based on presence alone.
- Use `query` to discover relevant code/processes, `context` for symbol relationships, `impact` before changes, and `detect_changes` for a working diff. Use graph results as navigation and impact evidence, not as proof of behavior.
- Verify important conclusions against current source, tests, and the actual diff. Do not infer that a behavior or dependency is absent merely because the graph did not return it; respect index coverage, skipped files, and staleness.
- Executors may use `impact` before edits and `detect_changes` after edits. Reviewer must independently inspect the diff and source; GitNexus is supplemental and must not replace the review skill.
- The MCP server is configured read-only. Do not attempt to apply renames or use GitNexus to mutate project/index data. Indexing remains an explicit user decision.
