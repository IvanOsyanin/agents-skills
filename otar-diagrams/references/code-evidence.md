# Extracting the Model from Code

Work from the current working tree. Documentation can help locate code but does not prove
that a route is connected, an integration exists, or operations actually occur in a given order.

Build a compact evidence register alongside the result:

| ID | Type | Name | Executor/owner | Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| F1 | function | Принять документ | API | path, symbol/lines | implemented |
| D1 | data | Копия документа | object storage | write adapter | implemented |
| E1 | exchange | Содержимое файла | API → storage | service call | implemented |
| F2 | function | Проверить версию формы | external system | integration-plan item | target |

Add only fields that matter to the task:

- **Component:** ID, parent system/components, full name such as `АС. Компонент`, modular responsibility, internal/external boundary, verified stack/deployment, and evidence. Distinguish an interface contract from a specific product.
- **Function:** component ID + function ID, one canonical name shared by both views, input, observable result, published service or internal function, related stages/substages, and sheets. Function names are not unique keys.
- **Data:** ID, meaning/content, logical owner, physical location if known, lifecycle (persistent, temporary, in-memory, transit), producer, and consumer.
- **Exchange:** exchange ID and global interface number (separate fields), service provider/master system, call initiator, source-data component/function, receiver, request/event data, response data if any, sync/async mode, and verified condition/protocol. Show response flow in the reverse direction. Record a security category or change status only with explicit evidence. Technical responses and transport details need not appear on the information view.
- **Scenario:** ID/name, initiator, input, stages, conditions, outcomes, and function links; evidence/source and coverage status in the final information and functional views.

“Unknown” and “out of scope” are valid values when explained. Do not turn this list into
mandatory empty tables or fill gaps with guesses. Record evidence and status for disputed
details, not only for the component as a whole. Cite the plan item for target requirements;
do not mark a plan item implemented just because a class has a similar name.

Function symbols are more stable than line numbers; record both when possible. Do not invent
evidence from a filename alone. To establish that a significant function is absent, inspect
composition roots and connected routes/jobs.

When relevant to the scenario, verify:

- Who initiates work: a user, HTTP request, message, or timer.
- What actually arrives as input: bytes, multipart data, URL, ID, or form fields.
- Who calls an external system and who validates its result. An application hash check is not a business function of object storage.
- Which data is persisted, held in memory, or passed through in transit.
- Where transactions end and how commit, publication, and acknowledgement relate.
- What starts independently of the client response; where retries, errors, and final outcomes occur.
- How the client receives and applies results; whether a stale response can change state.
- Which dependencies are optional; whether a third-party service is an installed product or only an OpenAI-compatible contract/planned deployment.

Choose the level of detail for the task. A business-scenario diagram need not show
heartbeats or connection pools. However, it must not turn a retry into a successful
completion or several independent operations into one transaction.

Compare both views by ID **and exact names**. Use the scenario register as a completeness
checklist: represent every confirmed in-scope scenario in both views where appropriate.
Several atomic functional steps may elaborate one application function; preserve the parent
function name/ID. Give each entity a distinct ID; its cylinder and exchanged instance may
share that ID but have different roles. Check the global interface number and provider
independently of data-flow direction. Do not confuse transit with entity ownership. A shared
container must not hide an incorrect dependency between independent processes.
Store the evidence register in Draw.io shape properties or in a separate agreed file. If the
user asks for “diagrams only,” prefer shape properties and do not create unrequested sidecar
documentation.
