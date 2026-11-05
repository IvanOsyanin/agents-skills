---
name: code-review
description: >-
  Perform structured code review for branches, diffs, pull requests, merge requests, commits, and uncommitted changes. Use when the user asks to review code, review a branch before merge, inspect a PR/MR, verify reviewer comments, find bugs, security/auth/RBAC risks, regressions, missing tests, API contract problems, migration issues, deployment risks, PII/data exposure, SOLID/DRY violations, or unclear implementation quality. Russian triggers: код ревью, ревью кода, сделай код ревью, проверь код, проверка кода, ревью ветки, проверь ветку, проверь PR, проверь diff, ревью перед мержем, проверь изменения, посмотри код.
---

# Code Review

Use this skill when reviewing code changes. Focus on real defects, risks, regressions, missing tests, and unclear assumptions. Do not summarize the diff instead of reviewing it.

Compatible with **Cursor** and **Codex** — use the citation format that matches the environment you are running in (see Code Citations).

## Output Language

Write findings in Russian by default.

Switch to English when any of these is true:

- The user writes the review request in English
- Repository docs (`README`, `AGENTS.md`, PR description) are clearly English-only
- The user explicitly asks for English output

Keep severity markers (`🔴 Высокий` / `🔴 High`, etc.) aligned with the chosen language.

## Review Target

Determine the review target from the user request:

- Current branch against a base branch
- Uncommitted changes
- A specific commit
- A pull request or merge request
- A reviewer comment that needs verification
- A pasted diff or file list without git context

If the base branch is not specified, inspect local git context and infer the likely base. State the assumption when inference is uncertain.

If git is unavailable or the user pasted a diff, review the provided material directly. Do not block the review waiting for checkout.

## Workflow

1. Inspect repository status and changed files.
2. Read project instructions such as `AGENTS.md`, `.cursor/rules`, `.ai`, or other repo agent docs before judging code.
3. Identify the base branch or review scope.
4. Read the relevant diff with enough context.
5. Open changed files around risky code paths.
6. Evaluate SOLID and DRY on changed modules (see Design Principles).
7. Check tests related to the changed behavior.
8. Run minimal useful verification when practical (see Verification).
9. Report findings first.

Prefer targeted commands such as:

```bash
git status --short --branch
git diff --name-status <base>...HEAD
git diff --stat <base>...HEAD
git diff --unified=80 <base>...HEAD -- <files>
git diff --check <base>...HEAD
```

## Scope for Large Diffs

When the change set is large:

1. Start with high-risk paths: auth, permissions, migrations, API handlers, transactions, background jobs, external integrations.
2. Skim `git diff --stat` and `git diff --name-status` before deep reading.
3. Deprioritize unless they hide real risk:
   - lockfiles (`uv.lock`, `package-lock.json`, etc.)
   - generated or vendored code
   - pure formatting or rename-only churn
4. State what was reviewed deeply and what was only spot-checked.

## Priorities

Prioritize findings in this order:

1. Security, auth, permissions, data leaks, PII
2. Data loss, migrations, schema/model mismatch
3. API contract regressions
4. Broken business logic or edge cases
5. Deployment/config/env risks
6. Async/background/transaction bugs
7. Missing or weak tests
8. SOLID and DRY violations when they create real maintenance, testability, or bug risk
9. Other maintainability issues only when they create real risk

Do not report style-only issues unless they can cause a bug or operational failure.

## Design Principles (SOLID, DRY)

Check changed code for concrete design problems in the diff. Do not give generic lectures; cite specific code.

**SOLID**

- **SRP**: one module/class/function mixes unrelated responsibilities or is hard to name without "and"
- **OCP**: new behavior requires editing the same large conditional instead of extending safely
- **LSP**: subtype or implementation breaks caller expectations or contracts
- **ISP**: interface forces unused, empty, or misleading implementations
- **DIP**: high-level logic is unnecessarily coupled to concrete infrastructure details

**DRY**

- Duplicated business rules, validation, mapping, or orchestration already present in the repo or introduced twice in the same change
- Copy-paste with drift risk: the same rule implemented in multiple places differently
- Acceptable duplication: boundary layers (DTO vs ORM), test fixtures, trivial one-liners without shared semantics

**Severity for design findings**

- Usually `🟡 Средний` when duplication or SRP violation likely causes bugs or makes change unsafe
- Usually `⚪ Низкий` for refactor opportunities without near-term risk
- Use `🔴 Высокий` only when a design flaw directly threatens production correctness or security

## Verification

Run checks only when they are likely to add signal and the environment allows it:

- Run targeted tests when behavior changed and a related test file exists.
- Run linters or type checks only for the touched area when the project already uses them.
- Do not run the full test suite by default on large changes.
- If verification cannot run, say what was skipped and why.

Examples:

```bash
uv run pytest -v tests/path/to/test_file.py
uv run ruff check app/path/to/changed_module.py
```

## Confidence Rules

Separate confirmed findings from open questions.

Use a confirmed finding only when the code proves the problem.

Use an open question when the risk depends on unknown deployment, product requirements, external configuration, reviewer intent, or data that is not present in the repository.

When a risk is plausible but not proven, phrase it as a question or verification request, not as a confirmed defect.

## Code Citations

Always include file path and line numbers. Do not cite code without a file and line reference.

Pick **one** format based on the environment you are running in. Never mix both formats in the same finding.

### Cursor

Use repository-relative paths. The opening fence must be on its own line (no list markers or text before it):

````markdown
```12:15:app/services/foo.py
def risky_call():
    ...
```
````

Do not use absolute filesystem paths unless the user explicitly needs them.

### Codex

Use a navigable markdown link plus a fenced code block. Prefer absolute paths when the workspace root is known:

````markdown
**Проблемный участок кода**

[file.py](/absolute/path/to/file.py:42):

```python
def risky_call():
    ...
```
````

Use repository-relative paths inside the code fence when absolute paths are unavailable. Also include `file.py:42` inline in prose when helpful.

## Finding Header Format

Every finding header must start with a severity marker, then the severity text, then a short title. Do not rely on color alone; the severity must be readable from the text as well.

Russian:

```markdown
**1. 🔴 Высокий - короткий заголовок**
**2. 🟡 Средний - короткий заголовок**
**3. ⚪ Низкий - короткий заголовок**
```

English:

```markdown
**1. 🔴 High - short title**
**2. 🟡 Medium - short title**
**3. ⚪ Low - short title**
```

Use these severity levels:

- High / Высокий — blocker before merge: confirmed serious security issue, data loss, broken deployment, migration breakage, major API regression, or high-confidence production failure.
- Medium / Средний — meaningful issue or important open question: likely bug, missing verification, risky deployment/config ambiguity, insufficient tests for risky behavior, or behavior that may block merge after confirmation.
- Low / Низкий — non-blocking observation: low-risk cleanup, small test improvement, or minor maintainability issue.

Prefer Medium / Средний for open questions that may affect merge, unless the code proves a High / Высокий failure.

Do not use green for finding severity. Reserve green check marks only for explicitly positive confirmations.

## Required Finding Structure

For each issue use this structure (adapt section titles to the output language). Use the code citation format from Code Citations that matches your environment.

**Cursor example:**

````markdown
**1. 🔴 Высокий - короткий заголовок**

**Проблемный участок кода**

```12:15:app/services/foo.py
...
```

**Что сделано не так**

Explain the issue plainly. Assume the reader may not know the project.

**К чему может привести**

Explain realistic impact and failure mode.

**Как сделать лучше**

Give concrete remediation or the exact question to ask if the issue depends on external context.
````

**Codex example:**

````markdown
**1. 🔴 Высокий - короткий заголовок**

**Проблемный участок кода**

[foo.py](/absolute/path/to/app/services/foo.py:12):

```python
...
```

**Что сделано не так**

Explain the issue plainly. Assume the reader may not know the project.

**К чему может привести**

Explain realistic impact and failure mode.

**Как сделать лучше**

Give concrete remediation or the exact question to ask if the issue depends on external context.
````

English equivalent section titles: **Problematic code**, **What is wrong**, **Likely impact**, **How to improve**.

## Final Response

Return findings first, sorted by severity (highest first). Then add:

- **Что сделано хорошо** / **What looks good** — 1–3 concrete positives when they exist; omit if nothing meaningful to praise
- Open questions, if any remain outside the findings
- Verification performed
- Tests not run or residual risk
- Scope note for large diffs (what was deep-reviewed vs spot-checked)

If there are no findings, say that clearly and mention remaining test gaps.

## Review Style

Be direct, evidence-backed, and specific. Include file and line references. Do not claim something is fixed unless live code proves it. Do not bury serious issues in a summary.
