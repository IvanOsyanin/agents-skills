# OTAR Diagram Visual Grammar

Specification updated on 2026-11-04 using notes and nine additional images from an official
source, as confirmed by the user: seven information-architecture slides and two explained
functional-model excerpts. These refine the earlier reconstruction from five images dated
2026-11-03. Source-system names and specific technologies are not requirements of this Skill.
Shapes and official explanations are described below; application rules are in the
[information](information.md) and [functional](functional.md) views. Evidence status and
limits are documented in [sources](sources.md).

## Shapes

| Element | Meaning and label | Visual rule |
| --- | --- | --- |
| Element | Meaning and label | Visual rule |
| --- | --- | --- |
| System/component | Executor and ownership boundary | Blue container; nesting is allowed. Place the full name at the top: `АС. Компонент. Подкомпонент`. Do not confuse it with an action or data. |
| Lane | One selected executor/component in a functional scenario | White vertical area with a heading. Separate lanes within one system are allowed for independent runtimes. |
| Information-view function | One functional capability | Separate yellow-orange, slightly rounded rectangle. Name it with a verb or verbal noun, e.g. «Отправить заявку» / «Отправка заявки». Use one block per function. |
| Functional-view action | Execution of a business function | In the new examples, use a separate light-blue rounded block. Its function name must exactly match the information model. |
| Component data | Usually one domain entity: application, consent, product | Green cylinder in either view. Use one entity per shape; wrapping a long name is fine, listing different entities is not. A cylinder does not prove a physical database or persistence. |
| Exchange data | Transmitted entity instance/value set | In the functional view, use a small green shape with a folded upper-right corner and a **visible inner fold**. It is not an action and does not prove a “file” format. |
| Actor | User/role | Show the actor shape and name; use a dashed participation link to an action or component labelled with the function invoked. The shape does not imply authorization. |
| Start/end | Boundaries of a specific scenario | New examples use a green circle for start and a pink circle with a thick black outline for end. Label the trigger/outcome nearby. Do not assign full BPMN semantics. |
| Interface | Service provision or data mastership | Small light-yellow numbered circle at the provider's boundary; it is not a process start, data direction, or separate system. |

The cylinder represents logical component data; the folded shape represents data in a
specific exchange. One entity may use both shapes with a shared ID; this does not make them
two entities. A cylinder beside «Предоставить данные» and its output object represent
different roles for the same data. See the [functional model](functional.md) for details.

### Styling Profiles

The primary profile follows the newly supplied annotated examples: yellow-orange functions
in the information view, blue actions in the functional view, a folded-corner data object,
and green/pink events. The editable teaching assets reproduce this profile. Older examples
use orange functional actions, a clipped-corner object without a fold, and circle markers
with triangles/squares. Treat that as an alternative profile for preserving an existing
diagram on request, not as a universal ban on folds or other colors. Do not mix profiles on
one sheet. For an exact copy, follow the selected source.

Practical palette: component `#9fc5f3`, information function `#efbb96`, functional action
`#bacbdd`, component data `#a9c574`, exchange data `#8faa50`, start `#92ce50`, end `#e5a5a5`,
interface `#fff2b2`, line `#41474b`. These are approximate chosen colors, not extracted
corporate RGB standards.

## Links and Conditions

- In the information view, arrows follow primary data flow, while the numbered circle
   sits by the service provider/master system regardless of direction. Do not infer data
   direction from the call initiator. A data-return arrow may point from provider to
   consumer even when the consumer called the provider.
- In the new examples, a filled triangle means synchronous interaction and an open triangle
  means asynchronous. Determine the mode from code or requirements, not line color. Record
  an unknown mode in the register/legend.
- A solid link between functional actions shows a call/transition; it does not replace a
  separate dashed data-flow link. Show material return flows here.
- A dashed data/action link shows input `data → action` or output `action → data`. Choose
  direction by meaning; it is not automatically bidirectional. A dashed actor link shows
  participation/triggering. Link type depends on both endpoints. Use an undirected
  association only with an explicit label when direction is unknown.
- Label information links as `Data(security category) [Service]`; add a category only when
  supported by evidence. Omit protocols, HTTP codes, and technical ACKs from overview sheets.
  Interface numbers are shared across both views and all OTAR sheets; they are not stage IDs.
- Label conditional behavior explicitly, e.g. “if enabled,” “on error,” or “retry when …”.
  A dashed line is not a universal marker for optional behavior.
- Show asynchronous publication, processing, state reads, and periodic maintenance as
  independent scenarios when the code supports them.

The new information-view legends define change statuses: red outline/flow means new,
purple means changed, dark means unchanged; a dashed information-view link means a
technical flow. These are separate attributes, not sync mode, security category, or the
functional view's dashed data link. Use them only when current and target states are known
and include a legend. A current-state diagram does not need status colors.

Do not transfer the meaning of special icons, the yellow pipeline block, or labels `(К)`,
`(КТ)`, `(БТ)`, `(ПДС)` without an applicable legend. The new examples confirm where a
security category appears in a label but do not define the full classifier. Function/entity
IDs do not replace interface numbers. Do not add BPMN gateways, diamonds, or architectural
types with unverified meaning.

## Granularity

Split a block such as “Принять запрос; сохранить копию; создать запись; отправить ответ”
into multiple actions. A block such as “Зарегистрировать операцию” may represent one atomic
transaction with multiple writes if its boundary is explicitly stated.

Do not create a block for every language-level function call. Show actions needed to
understand behavior, responsibility, and outcome. If success and retry follow different
paths, draw branches rather than hiding them in a block's prose.

Example: a blue component «АС. Хранилище» with separate functions «Записать файл»,
«Прочитать файл», and «Удалить файл», plus a separate entity «Копия файла». A green cylinder
called «Хранилище: сохранить и удалить копии» is wrong both semantically and in granularity.
