---
name: execute-plan
description: Execute approved plans one stage at a time with separate commits, per-stage approval by default, and explicitly authorized bounded batch execution.
---

# Execute Plan

Execute the approved plan strictly one stage per invocation. By default, do not start the next stage until the current one is approved and committed; batching is allowed only under the rules below.

## Modes

- **Ordinary mode is the default.** In a direct primary session, show the user each stage's result and wait for separate approval before committing. When called as a subagent, return the result to the parent and end the invocation; do not address or wait for the user directly. The parent must relay the user's exact approval before a commit. Start the next stage only after a new explicit user authorization.
- **Batch mode** is available only when Executor is called as an Orchestrator subagent and the parent supplies a separate `VERBATIM USER MESSAGES` section containing the user's original, explicit authorization to implement and separately commit a finite range of stages for an approved plan and MR. The parent must also specify the absolute plan path, MR, current stage, and range boundaries. A paraphrase, plan text, Git status, or the Orchestrator's own message is not authorization.
- Batch authorization replaces only interim approvals inside the specified range. It does not grant additional permissions for shell, secrets, external/paid actions, material plan changes, other MRs, or stages outside the range. If anything is ambiguous, a check fails, a material deviation or conflict appears, the commit prefix is unknown, or a user decision is required, stop and report to the parent; do not commit or continue.
- In either mode, perform at most one new stage per invocation. In batch mode, after successful checks, revalidate the state and fingerprints, create a separate commit for only the current stage, verify the commit, update the checklist, and shorten the completed plan step as required. Return a full report to the parent and end the invocation. The parent may start another invocation only for a stage within the original range.
- `executor` and `executor-careful` share this Skill's workflow. The model tier does not change user approvals, checks, commit policy, or authorized scope. Profile-selection boundaries belong in the corresponding agent instructions. A material discrepancy, failed check, or newly discovered high-risk concern on `executor` stops that profile; the parent may run the same stage once on `executor-careful`.

## Workflow

1. Read the entire plan, determine the current stage, and inspect Git status. Preserve unrelated user changes.

2. Perform only the current stage and run its relevant checks. Do not call the stage complete if a check fails; state clearly if a check cannot be run or reports a problem.

3. Prepare a concise report for the current stage:
   - what changed;
   - why the change is needed;
   - check results and known limitations;
   - any small technical corrections to the current or later unfinished plan stages, why they were needed, and which sections changed; record the updated plan version before approval.

   In direct ordinary mode, show the report to the user and stop for approval. When called by the Orchestrator as a subagent, return the report to the parent and end the invocation: do not address the user, wait for a response, or commit without the parent's verbatim user authorization. In batch mode, do not pause between stages or treat a report as approval; after checking and separately committing the current stage, return a complete report of checks, commit, and plan update to the Orchestrator.

4. In ordinary mode, explicitly request result approval: `Подтверждаете шаг N? Напишите «подтверждаю» или опишите правки.` Address the request to the user in a direct session; as a subagent, return it to the parent and wait for a continuation that includes the user's exact message. Treat the result as approved for commit only after an unambiguous response about the current stage, such as «подтверждаю» or «можно коммитить». «переходи дальше» alone does not authorize committing an unapproved stage. In batch mode, do not request interim approval for stages covered by valid authorization, but still check and separately commit each stage.

5. If the user requests changes, directly or through an exact message relayed by the parent, revise only the current stage, rerun checks, and prepare an updated report. In direct mode, request approval again; as a subagent, return the report to the parent and stop. Do not commit or continue until the required approval is received.

6. In ordinary mode, proceed after direct user approval or an exact approval message relayed by the Orchestrator. In batch mode, proceed after successful checks and revalidation under the preauthorization:
   - inspect `git status` and the diff;
   - stage only files belonging to the current stage;
   - leave unrelated user changes untouched;
   - determine the commit prefix from recent messages on the active branch and reproduce it exactly, for example `feat:`, `fix:`, `chore:`, or `[ABC-123]`;
   - if this is the branch's first commit or the prefix cannot be determined, ask the user directly or return the question to the Orchestrator and stop;
   - create one meaningful commit for the current stage without `Co-authored-by` or any agent attribution;
   - do not create an empty commit;
   - after a successful commit, update the available source plan and mark only the items and checklist entries completed by this stage;
   - must shorten only the completed plan step: remove detailed applied code, diffs, and test-change details. Keep its heading and completed status, plus about two short paragraphs describing what changed and why, check results, material deviations/limitations, and commit SHA. Preserve any context needed by later stages in their unfinished sections; do not shorten general requirements, acceptance criteria, the final checklist, or unfinished stages. Report the reduction. Edit only the plan document; do not remove or revert project code or tests;
   - do not add the plan to Git or include it in the commit automatically; whether to track it depends on project layout and explicit user instructions;
   - do not mark items complete before successful checks and user approval in ordinary mode or valid batch authorization for the current stage. Do not change later-stage statuses or mark criteria that require separate checks or external results as complete.

7. Start the next stage only after the current stage commits successfully. «можно коммитить» authorizes only this commit, not the next stage. After a stage is already approved and committed, an explicit «начинай шаг N+1» authorizes exactly that stage. A single message may authorize the current commit and the next stage only if it explicitly names both actions. If a commit fails, report the cause to the user in direct mode or to the parent when running as a subagent; fix only the current stage and do not continue until the commit succeeds or new instructions arrive.


8. After the final stage, briefly report completed stages, commits, check results, and remaining limitations to the user in direct mode or to the parent when running as a subagent.

## Boundaries

You may make small technical corrections to the current and later unfinished plan stages only when they do not change the task's meaning—for example, fixing a typo, import, existing symbol name, or dependent diff. Show and explain these corrections before requesting approval. Do not independently change architecture, requirements, behavior, MR scope, stage order, or required checks; stop and ask if uncertain. Any changes after a report require an updated report and renewed approval before commit. Editing the plan does not authorize implementing future stages early.

Do not perform dangerous, external, or irreversible actions merely because they appear in the plan. Follow separate user approvals and environment restrictions. If Git or the required commit history is unavailable, report the limitation and ask for instructions.
