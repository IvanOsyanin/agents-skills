# OTAR Information Diagram

Show the solution's composition and the meaning of interactions within the selected
scope. This is neither an ER model nor an execution sequence. The order of functions
inside a blue component does not define action order; it may be arranged for readability.
Maintain one information model/diagram per project covering confirmed in-scope scenarios.
Do not create competing architecture diagrams for separate scenarios. A diagram may use
multiple linked sheets for readability. For a paired view, agree on this composition first,
then elaborate it functionally.

If the user provides an existing architecture diagram, treat it as the source model:
identify roles, components, functions, data, exchanges, boundaries, and existing IDs/numbers;
compare them with code and requirements. Preserve confirmed decisions and numbering, and
refine or extend the diagram only when supported by evidence. Do not silently replace it with
another architecture or leave competing final versions. If the source is an image, use it as
context and create an editable final diagram.

## Composition

- Show participant roles and external systems that actually take part in the scenarios.
  A human role and an application component are different elements.
- Place application components inside systems/subsystems only when ownership is verified.
  Do not confuse deployment location, organizational ownership, and component composition;
  name the meaning of each outer container. Do not turn a source-code folder into a system
  without architectural evidence. An application-system component encapsulates application
  capabilities consistently with a modular, replaceable implementation; it is not an
  arbitrary collection of functions on a page.
- Use full component names in the project's language. In Russian, use the form
  `Родительская АС. Компонент. Подкомпонент`, e.g. `Заявки. API. Проверка`. This preserves
  ownership outside a container. Do not invent an unverified parent. IDs and technology
  stacks are not substitutes for architectural names.
- Show functions as separate yellow-orange blocks, named with a verb and object or a verbal
  noun and object. Do not combine distinct functions in a comma-separated list. Preserve
  executor and function IDs even when different systems use the same display name.
- An “AS service” is a function published for use by another AS and is typically involved
  in an interaction. It is not necessarily a microservice or separate runtime. The service
  named on a link must match the published function.
- Show domain entities as separate green cylinders. The Russian examples “Заявка” (Application)
  and “Решение” (Decision) are two shapes, not one cylinder labelled “Заявки, решения”. Do
  not split one entity merely to show its attributes/state or wrap a long name.
  A component may have no data of its own. Determine whether data is a temporary copy,
  in-memory, or persistent; a cylinder alone does not prove this.
- A component that only transmits an entity may omit its cylinder. Label inbound/outbound
  exchanges and mark “transit” in the evidence register.
- Distinguish logical data ownership, physical storage location, and copy recipient. For
  example, an application may own an application status, PostgreSQL may store a record, and
  a UI may display a copy. Entity placement does not replace this distinction.
- Do not overload the overview with stack, transport, or operational details. Keep verified
  stack information in the evidence register; add it to the diagram only when requested or
  clearly necessary. An “S3-compatible storage” contract does not prove AWS S3, and an
  OpenAI-compatible API does not prove a specific gateway or model provider.

## Exchanges

For every link, make the source/recipient of primary data, the data itself, the service
provider, and the called function clear. The call initiator and data source are separate
register fields. Do not draw a mandatory “request/response” arrow pair for every call:
technical status, ACK, and return codes are not independent business exchanges. Meaningful
data flows in both directions are valid; do not omit a significant result.

Label the link with the data and service, for example `Заявка [Принять заявку]` or
`Инвестиционные продукты клиента (known security category) [Предоставить продукты]`.
The exchanged data should semantically match the green entity. Keep names consistent, but
they need not repeat pluralization or filter details. Omit the security-category parentheses
when the category is unknown; do not infer a category from the domain. A long label may be
moved to an unambiguous legend, but keep the data name on the link.

### Interface, Direction, and Mode

- Place the yellow numbered circle **by the service provider**: the AS that implements the
  function or the master system for a key entity in the interaction. It is not necessarily
  at the start of the arrow.
- When submitting an application to a service, the arrow is `consumer → provider` and the
  circle is by the recipient. When retrieving a product list, the arrow is `provider → consumer`
  and the circle is by the sender, even though the consumer initiated the request. If the
  master system differs from the implementing service, record the selected role and evidence
  in the register; do not position the circle based on line geometry.
- Interface/interaction numbering is global across the entire OTAR and all sheets. Do not
  restart numbering in the functional view. Preserve existing numbers when updating. A number
  is a stable reference, not an algorithmic stage order. Repeated depictions of the same
  interface keep its number; distinct interfaces do not share one merely because their
  executors match.
- A filled triangle means synchronous interaction; an open triangle means asynchronous.
  Omit protocols from the overview. If the mode is unknown, do not present a chosen arrowhead
  as verified; mark the uncertainty explicitly.

An actor may have a dashed link to a component labelled with the function used, or directly
to the function. This appears in the supplied information example. Label conditional
participation explicitly, for example “if logging is enabled”.

## Relationship to the Functional Diagram

The same function has the same executor and **exact same name** in both views. A nested
component becomes a lane with its full `AS. Component` name. Adjacent lanes do not imply
server deployment.

In the register, map `component + function → scenario stages`. Multiple detailed stages may
map to one function if its parent function is identified explicitly. Do not replace the
function name with a synonym. If these are independent functions at the selected level, add
them to the information model first. Identical wording such as “Исполнить заявку” in two
systems does not make them one function. Mark the scope boundary if part of the composition
is not elaborated functionally.

Before export, verify that roles and external boundaries are visible; functions belong to
the correct components; entities are separate; transit is not shown as ownership; exchanges
are labelled with data and service; interface circles sit by providers; numbering is global;
data-flow direction and sync/async mode are correct; and target technology is not presented
as deployed technology.
