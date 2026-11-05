---
name: task-planning
description: "Prepare detailed implementation plans for one or more MRs, including project analysis, complete step code, tests, and checks. Use for implementation planning or when explicitly requested."
---

# Task Planning

## Purpose and Scope

Prepare an implementation plan for an existing project that the user can review and approve. Respond in Russian unless the user requests another language. Do not implement the plan, launch executor agents, or create project files other than plan documents. Separate verified facts from assumptions. If requirements, dependencies, or project state do not provide enough information to produce reliable code, ask for clarification; never present guesses as implementation-ready code.

In a direct primary session, ask the user any clarifying questions. When called as a subagent, return questions and blockers to the parent; do not call `question` or address the user directly. Continue only after the parent relays the user's exact answer.

## Project Research

1. Clarify the goal, expected behavior, constraints, and task boundaries. Inspect actual entry points, affected calls and types, implementations and API consumers, configuration, dependencies, existing tests, and documentation. Determine how the project normally runs tests and checks.
2. Read every applicable `AGENTS.md` from the project root through affected directories, including nested files. Do not apply instructions for neighboring areas. Also consider other applicable project instructions and link important constraints to their sources. If conflicting instructions or requirements prevent a reliable plan, state the conflict and ask the user to resolve it.
3. Check current project documentation such as `README.md`, `docs/`, API descriptions, and operational guides. If the change affects documented behavior, configuration, or interfaces, include a specific documentation update in the relevant stage. If no documentation change is needed, briefly explain why.
4. Determine the project root: the Git repository root or the active OpenCode location root. Ask the user if it cannot be determined. If an existing plan was specified, read it first. Inspect Git read-only and only after shell permission; prefix commands with `git --no-pager --no-optional-locks -c core.fsmonitor=false -c core.untrackedCache=false`. Check actual status and refs; do not assume the base branch name. First inspect changed-file names or statistics. For substantive diffs, use safe options and the secret-path exclusions in `~/.config/opencode/agents/reviewer.md`; if a safe diff cannot be formed, ask the user for a sanitized diff. Do not fetch, checkout, or run commands that modify the repository. Never put secrets in a plan.

## One or More MRs

- Split work into multiple MRs when doing so improves independent understanding, review, safe rollout, or risk management. Do not artificially split a small cohesive task. Consider compatibility, rollout order, migrations, and dependencies; every MR must have clear value and a verifiable outcome.
- If one MR is sufficient, save the complete plan in `<project-root>/.ai/plans/<name>.md`.
- If several related MRs are needed, create `<project-root>/.ai/plans/<name>/` with a `README.md` and a complete plan file for each MR, such as `01-<name>.md` and `02-<name>.md`. In the `README.md`, clearly describe the shared goal, current and target behavior, boundaries, order and dependencies, each MR's contribution, and relative Markdown links to every subplan. State which earlier MR results are prerequisites for later ones and how compatibility at the boundaries will be checked.
- At the start of each subplan, identify its MR, link the shared `README.md`, and state its prerequisites and place in the sequence. Each subplan must be self-contained for its scope; do not replace its stages with a link to the shared document.
- Never overwrite existing plans or directories containing materials: choose a new name or ask the user. Create required directories under `.ai/plans/`. Do not save project plans in the global OpenCode configuration directory.

## Contents of Each MR Plan

Before listing stages, explicitly state:

1. **Goal and scope** — the problem, expected outcome, and what is out of scope for this MR.
2. **Current behavior** — verified facts with paths and relevant symbol names and, when useful, links to applicable instructions.
3. **Target behavior** — observable changes, acceptance criteria, and impact on users and interfaces. Add a text or Mermaid diagram when helpful; a diagram supplements, not replaces, the description.
4. **Decisions and constraints** — relevant alternatives and tradeoffs, compatibility, migrations, risks, and prerequisites. Clearly distinguish assumptions from facts.

### Stages

Split implementation into sequential numbered stages. Each stage must be logically cohesive and fit one non-empty commit; state dependencies between stages. Use a separate level-four Markdown heading for each stage, immediately followed by a separate status line. For a Russian plan, use `#### Шаг N: <понятное название>` and `- [ ] Выполнено`; if the user requests another language, localize both. Do not replace the heading with a checklist item. Mark a stage complete only after checks, approval, and a successful commit under the Executor workflow.

Explain changes in plain language: first state what changes, why, and the resulting benefit. Avoid internal jargon, unexplained abbreviations, and names understandable only to project insiders; briefly explain necessary technical terms on first use. Each stage's purpose should be clear without deep project knowledge. Preserve exact paths, symbol names, and technical details the implementer needs.

For every stage provide:

- The stage goal and exact files/symbols to create, change, or delete, including required documentation. Explain the purpose of each change.
- **Complete, fully worked code for every non-test change**, ready to implement against the actual project state and prior stages. For new files, provide the full contents; for modifications, provide an exact applicable diff or full contents of the affected files; for deletions, name exact paths and describe required updates to all affected callers. Include imports, signatures, error handling, configuration, and call sites where relevant. Do not use vague descriptions, contextless fragments, pseudocode, `...`, TODOs, or invented APIs. If a stage has no non-test code, state this explicitly and describe the other changes concretely.
- **Tests:** test code is optional, but identify existing or new test files/suites, scenarios, preconditions, and expected behavior/assertions, including relevant negative and edge cases. Include tests that must be changed or removed.
- Stage checks and completion criteria, using actual project commands where possible. Do not claim proposed code was tested unless checks were actually run.

Every diff must start from the state after prior stages/MRs, avoid conflicts, and include enough context to apply. Check proposed code carefully against actual dependency versions, types, and constraints; implementation-ready does not mean compiled or tested. If required code cannot be specified reliably, mark the blocking gap, gather missing information, or ask the user; do not call the plan ready to execute. Clearly identify destructive or external actions and required approvals.

After approval, Executor may make small technical updates to the current and later unfinished stages without changing their meaning, and report those updates before requesting approval. After a successful commit, Executor updates the plan document: replace the completed stage's detailed applied code, diffs, and test-change details with its heading, completed status, and about two short paragraphs describing the outcome, checks, material deviations, and commit. Do not shorten general requirements, acceptance criteria, the final checklist, or unfinished stages; preserve any context they need in the corresponding sections. This reduction applies only to the plan document, never to project source files or tests.

## Design Method

- Apply DRY, KISS, and SOLID where they genuinely help the task; do not add abstractions or refactoring merely to satisfy a principle. If formal SOLID compliance adds complexity without meaningful benefit, prefer KISS while preserving correctness and supportability.
- Use patterns such as Strategy, Repository, Ports and Adapters, Unit of Work, or Dispatcher only when they provide a concrete benefit. Briefly state where and why each selected pattern is used, what problem it solves, and its tradeoffs. If a term is ambiguous, state the definition used. Cite a reliable source and a reasonable alternative when useful; do not invent links or make a pattern mandatory.

## Final Checks for Every Plan

After each MR's stages, plan the project's full standard test suite and applicable required build, lint, type, and documentation checks. Find actual project commands; if a command cannot be determined, state this and ask rather than inventing one. For monorepos, define the scope of the full suite and check project-wide requirements.

Also identify long-running end-to-end and integration scenarios, especially those involving LLM calls, external services, paid resources, or data changes. Decide whether to run each one based on change scope and risk; record its command and prerequisites or a reasoned exclusion. If uncertain, ask the user before plan approval. Do not exclude checks required by project instructions without approval to change that constraint. State any extra permissions, secrets, services, or costs that may be needed; do not run them during planning. Do not call a suite “full” if checks were excluded unless scope and exclusions are explicit.

Run final checks after the last stage's changes and before that stage is approved and committed; additional verification of the final post-commit state is allowed. If the integrated MR sequence needs further checks, specify them in the last MR and the shared `README.md`.

End every plan with an **Executor-required-checks checklist**, using separate `- [ ]` items for behavior and compatibility criteria, planned tests and commands, documentation, decisions about long-running/E2E checks, and other task risks. Leave statuses unchecked; never mark a check complete unless it was run. Clearly label checks dependent on external conditions. Plan checks so Executor can report their results before the final stage is approved.

## Completion

Provide the absolute path to the single plan, or to the shared `README.md` and every MR subplan. In a direct primary session, ask the user to approve the plan; for a multi-MR plan, identify the first executable subplan for `/implement` and provide the shared README for context. When called as a subagent, return the same paths, blockers, and required user decisions to the parent; do not request approval directly or treat the subagent call as approval. Plan approval alone does not authorize implementation, commits, or later stages. Before implementation, Executor must compare the proposed code with the actual project and stop on material discrepancies.
