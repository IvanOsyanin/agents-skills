# OTAR Notation: Evidence and Limits

Updated 2026-11-04. The user clarified the notation name as Gazprombank OTAR.
The user confirmed that the newly supplied notes and nine attachments are official.
Their explanations are primary rule sources, not hypotheses inferred from unrelated images.
This Skill covers the two diagram views shown in its examples. It does not define the full
OTAR document, approval procedure, or all corporate classifiers. Its output is a draft for
architect review.

## Public Primary Sources

1. **Gazprombank.Tech, 2025-08-29 — «Развитие внутренней венчурной студии Газпромбанка: новые возможности и результаты первого полугодия 2025 года».**
   [Publication](https://www.gazprombank.tech/blog/1359/).
   Confirms the expansion “organizational-technical architectural solution,” the diagrams'
   purpose in developing and approving solutions, and their coverage of roles, systems,
   functions, flows, artifacts, and technologies. It describes creating a machine-readable
   diagram, automatic visualization, and subsequent architect refinement.
   Application in this Skill: completeness of the evidence register and consistency of the
   editable model.
2. **Gazprombank.Tech, 2026-01-19 — “Business Analysis Day.”**
   [Publication](https://www.gazprombank.tech/blog/1445/).
   Describes a demonstration of OTAR and BPMN generation and emphasizes atomic, complete,
   consistent requirements. Application in this Skill: validating model completeness and
   consistency. The one-action-per-block rule is derived from user-provided examples.
   The article does not define block shapes or equate OTAR with BPMN.

These publications confirm purpose and scope, but are not a reference for shapes, colors,
line directions, or WebOTAR import formats. An initial search on 2026-11-03 for
“ОТАР Газпромбанк,” “ОТАР нотация,” “ОТАР информационная/функциональная схема,” and
“WebOTAR” did not find an accessible complete standard. This records the search result; it
does not claim that a standard was never published. Unrelated acronym expansions, job ads,
and generic UML/DFD articles are not used as Gazprombank rules.

## User-Supplied Official Materials — Updated 2026-11-04

Received notes on OTAR principles, seven information-architecture slides (pages 20–26),
and two functional-model excerpts (the second is page 12). The full document's author,
revision, and URL were not provided; the user confirmed the materials are official, but this
was not independently verified online. The material facts below are retained because the
user requested removal of the original notes and attachments. Filenames indicate provenance;
they are not links.

| Source material | Confirmed rule |
| --- | --- |
| General notes | The concept authors drew on TOGAF and viewpoints; information and functional views are perspectives on one solution. The usual order is information architecture first, then functional. This does not require a complete TOGAF model. |
| Component notes | An AS component encapsulates application capabilities in line with a modular, replaceable implementation structure. Use full names in the project's language; in Russian: `Родительская АС. Компонент. Подкомпонент`. |
| Function/entity notes | Prefer one function and one domain entity per shape; do not use comma-separated lists. This is the Skill's default for clear responsibility boundaries. Transit does not require an entity cylinder in an intermediate component. |
| informational architecture 1.png, p. 20 | Name an AS function with a verb or verbal noun; blue components contain separate yellow-orange functions and green entities. |
| informational architecture 2.png, p. 21 | An AS service is a function published for use by other ASs and is typically involved in interactions. This is not equivalent to “microservice.” |
| informational architecture 3.png, p. 22 | Function/service names are consistent across the information and functional views. |
| informational architecture 4.png, p. 23 | A link connects service provider and consumer; its direction follows data flow. The label contains the exchanged data object, information-security category, and called service. Include a category only when known. |
| informational architecture 5.png, p. 24 | Synchronous interaction uses a filled triangle; asynchronous uses an open triangle. Line color does not indicate mode. |
| informational architecture 6.png, p. 25 | Place the circle at the service-provider AS: the AS implementing the function or the master system for a key entity. The number is a global OTAR interaction number. |
| informational architecture 7.png, p. 26 | Interface numbering is global across the OTAR, including the functional model. Carry the link number across views; do not renumber it as an action number. |
| Information-slide legends | Red outline/flow means a new system/module or flow; purple means changed; dark means unchanged; dashed information flow means technical flow. These statuses require a comparison baseline and do not define the information-security category. |
| functional model 1.jpg | Lane headings identify ASs; a green circle marks process start; a separate person shape marks a participant role. Actions are blue, cylinders green, and the end is pink with a thick black outline. Independent launches include “Сохранить данные” and “Передать данные”. |
| functonal model 2.png, p. 12 (source filename contains a typo) | A blue block is an action/business function; a green object with a visible fold is data; a pink circle with a thick outline is process end. The result object has dashed links to its producer and consumer; a cylinder represents AS data. |

The notes further clarify that the overview information view omits protocols and service
response codes; its direction shows the primary exchange, not every technical message. The
functional view preserves function names and reveals execution order. On that view, entities
connect to actions with dashed links.

### Changes from the Previous Rules

- The requirement to show every request and return on the information sheet is removed:
  show primary data there; show material call/return order in the functional view and full
  contracts in the evidence register.
- Replace abstract exchange labels with a provider-side circle, a global interface number,
  and the same number in the functional scenario. The number is not algorithmic order.
- Red/purple/dark outline and flow statuses and sync/async arrowheads are confirmed.
- The primary functional profile is updated: blue actions, green start, pink end, and folded
  data object. Retain the previous profile as an alternative when updating existing diagrams
  on request.
- Cylinders are no longer containers for lists of entities. Full component names, data
  transit, and exact function-name matching are clarified.

## Earlier Visual Evidence — 2026-11-03

The initial comparison used five user-provided images, not the earlier generated description:

| Example | Material observation retained in the Skill |
| --- | --- |
| 1.jpg and 2.jpg | Overlapping parts of one information model: nested blue systems, separate orange functions, and green data groups. Repeated fragments do not imply a second service. |
| 4.jpg | ADM information view: ecosystem and nested service, adjacent ASs, an actor, functions, data groups, and labelled exchanges. An actor's dashed link may lead to a component. |
| 5.jpg | ADM functional view: the same executors become lanes; functions are separate; both data cylinders and clipped-corner objects without inner folds appear; inputs and outputs are directed. |
| 3.png | Open WebUI → LiteLLM → SOCHI.Router example with a returned response. It contains special unverified symbols listed below. |

The original images are not needed for normal use: observations are summarized in the
[visual grammar](notation.md), and shapes are reproduced in the assets. The
[paired example](../assets/example-pair.drawio) is a new teaching scenario that shows
coordinated views; it is not an official bank example.

## Remaining Unknowns

The meanings of `(К)`, `(КТ)`, `(БТ)`, `(ПДС)`, all special icons, the yellow pipeline block,
and the complete event/component-type catalogue remain unverified. The new materials do
confirm where the information-security category appears in a label and the line statuses;
they do not justify guessing category values. Corporate RGB values, exact dimensions, and
the WebOTAR exchange format are unknown. Do not guess confidentiality categories or
architectural types. Draw.io/XML is this Skill's editable output; WebOTAR import compatibility
is not claimed.

Code-detail rules, branching, local IDs, transaction boundaries, export formats, and checks
are working conventions of this Skill. Global interface numbers, function names, shape roles,
and primary directions are supported by official materials. Exact RGB/dimension choices and
simplified decorative icons approximate the examples. Do not present these conventions as
quotations from the bank's standard.

Official explanations in the newer materials take precedence over earlier reconstruction.
A new user-supplied legend or current standard supersedes these visual rules; the source
image takes precedence over generated summaries. If rules conflict or exact conformance to
an unknown type is requested, ask for the missing legend excerpt while continuing independent
parts of the task. For ordinary scenarios, use the retained rules without repeating the
standard search or reanalyzing old images.
