# OTAR Functional Diagram

Create one coordinated functional diagram for the project, covering all confirmed
scenarios within the selected scope. Do not create separate alternative diagrams for
each scenario or component. Within the shared model, clearly separate scenarios by
initiator, actions, interactions, and outcomes. Use white vertical executor lanes and
separate blue actions from the primary [visual profile](notation.md). The functional view
elaborates the information view; it does not rename its functions or interfaces.

## Scenarios and Responsibilities

For each scenario, record its triggering event, input, and observable outcome. Before
export, compare scenarios with the evidence register: show a path from trigger to outcome
for every in-scope scenario, including material variants, errors, and independent background
launches. A successful happy path does not cover other scenarios. Do not add hypothetical
scenarios without evidence; mark unknown scope boundaries explicitly. For a large diagram,
use linked sheets within one model and label transitions rather than creating unrelated
final files. Distinguish a user request, message delivery, timer, and state read. An HTTP
response, job publication, and start of background processing are not one continuous flow
merely because they concern the same business object.

Each lane represents a component at the selected level. If the API, handler, and scheduler
run independently and their responsibilities matter to the scenario, separate them. Do not
create a lane for every class/package. Component placement in the information model and
action executor must agree by ID. Preserve full ownership in lane names, e.g. `AS. Component.
Subcomponent`. Show a human role separately, with a dashed participation link to the action;
an actor does not automatically become another AS.

## Actions and Data

One block represents one action at the selected level with a clear outcome. For example:
“Принять документ” → “Сохранить копию” → “Зарегистрировать заявку” → “Вернуть ID”. Do not
connect actions merely because they appear in that order inside an information container;
the code determines execution order. One atomic transaction with several writes may remain
one action if its boundary is stated. Do not combine independent operations this way.

Copy each function name **exactly** from the information diagram: do not rename
“Предоставление продуктов клиента” (“Provide client products”) as “Выдать продукты” (“Issue
products”). Repeated execution of one function may use multiple blocks with a shared function
ID and distinct stage IDs. For sub-stages, identify the parent function name/ID. Add
independent functions at the selected level to the information model as well; a shared ID
alone does not hide a name mismatch.

Place an application-performed validation in that application's lane, even when it checks
stored data. Write/read/delete operations belong to storage functions; the caller decides
when they run.

Solid links show meaningful calls/transitions between actions. Show a returned result and
the receiver's next action when they are part of the scenario. For an inter-system call,
use the same interface number as in the information view; scenario order, not increasing
interface numbers, determines action order.

### Choosing a Data Shape

| What is shown | Shape and link | What it does not imply |
| --- | --- | --- |
| Logical data held by a component: consent, product, application | Green cylinder in the owner/holder lane; dashed link to a reading action or from a writing action | A specific DBMS, disk, persistence, or mandatory separate database |
| Data instance/set produced by one function or consumed by the next: transferred consent, received product list | Green object with a folded top-right corner and visible inner fold; dashed `action → data → action` links | A disk file, paper document, or separate domain entity |

For example, the source AS logically owns “Признак согласия” (“Consent flag”; cylinder),
“Предоставить данные” (“Provide data”) creates an output object “Признак согласия” (folded
payload), and “Передать данные” (“Transfer data”) consumes it. Add a cylinder at the receiver
only when storage/ownership is confirmed; it is optional for transit. The cylinder and
exchange object may share one entity ID while representing different roles. Use separate
shapes for multiple entities; do not put a list inside one shape.

Label data objects with nouns; data links are always dashed and directed according to
reading/writing semantics. Solid action links and dashed data links are separate layers;
neither replaces the other. No green shape replaces a function, service, or success marker.
An older no-fold profile may be retained to preserve an existing diagram; the fold must not
be omitted from new examples.

## Branches and Completion

Branching rules below are working conventions for this Skill, not a complete OTAR standard.
The start/end shapes are confirmed by the supplied official materials.

- Label outgoing links for alternative outcomes, e.g. “данные корректны” (“data valid”),
  “ошибка проверки” (“validation error”), or “временная ошибка” (“temporary error”). Each
  branch must lead to a visible action, outcome, or labelled continuation on another sheet.
- Do not call a decision split a parallel launch. Show parallelism and result-wait conditions
  explicitly when verified; do not invent gateways.
- Route retries back to the retry point and label known conditions/limits. Polling is a
  repeated read, not repeated creation/processing.
- For asynchronous exchange, show publication, job acceptance, and a separate handler launch.
  When material, show commit/send/acknowledgement order. A transmitted ID is not the document
  contents.
- In the primary profile, use a green circle for start and a pink circle with a thick black
  outline for end; label the trigger and outcome, e.g. “ID выдан” (“ID issued”), “результат
  сохранён” (“result saved”), or “ошибка возвращена” (“error returned”). An HTTP request ending
  does not mean background work is complete. For a continuing loop, show a loop rather than
  inventing a final state.
- When splitting across sheets, preserve transition IDs and label links “продолжение: лист …”
  (“continuation: sheet …”); an accidental broken arrow is not a valid transition.

Show failures in enough detail to explain changed outcomes or responsibilities: input
validation, external-system failure, retry/final error, or compensation. Do not turn the
overview sheet into a list of every code exception. Hidden technical details must not change
the meaning of a successful outcome or transaction boundary.

Before export, trace each scenario from its start to every outcome; verify executors, data,
conditions, and return direction. Map stages to information-model functions by the component
ID and function ID pair.
