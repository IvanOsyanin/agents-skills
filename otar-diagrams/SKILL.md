---
name: otar-diagrams
description: Create, validate, and update information and functional diagrams from code using Gazprombank OTAR notation and supplied official materials. Use for one diagram or a coordinated OTAR pair; do not substitute arbitrary UML, BPMN, C4, or ER diagrams.
---

# Gazprombank OTAR Information and Functional Diagrams

For each project, create one coordinated information (architecture) diagram and one
functional diagram. The information view shows roles, systems, components, functions, data,
and exchanges; the functional view shows actions performed by executors. These are two
coordinated perspectives on one solution, not independent models or alternatives. Each view
must cover all confirmed scenarios within the requested scope. Do not create one diagram per
scenario, subsystem, or run. For readability, use multiple linked sheets within one diagram
file. Do not stop after drafting one view: complete both, check their consistency, and deliver
the finished result. If the user requests only one view, honor that limit; do not present an
unfinished draft as a completed pair.
OTAR stands for “organizational-technical architectural solution.”
This Skill describes OTAR notation based on official materials supplied for Gazprombank; it
is not a complete internal standard. The user confirmed the official origin of the new
materials. Verified facts, rule provenance, and unresolved symbols are documented in
[sources and applicability limits](references/sources.md).

## Source Material

Preserve the scope and format requested by the user. For a diagram “from code,” show the
current state by default. If a target integration is already under discussion, keep that
scope and clearly distinguish implemented behavior from design.

Sources have distinct roles:

- Current code, connected entry points, and tests determine actual behavior.
- An approved plan defines target functions; a plan status does not make them implemented.
- This notation and its editable primitives define visual representation.
- A user-supplied existing diagram (image, SVG, Draw.io, or another format) is the project's
  source model. Use it as context and preserve confirmed elements, links, scope, and available
  IDs/numbers. Refine it using code and other specified sources; do not create a parallel
  alternative architecture. Build a coordinated functional view from it, even if only an
  architecture view was supplied. If the source is editable, update it; if it is raster,
  produce an editable result while leaving the original image untouched.
- New user-provided images/legends refine the notation and take precedence over earlier
  generated descriptions. Do not reanalyze old images without a new reason.

Read the [notation rules](references/notation.md). Before drawing, build a compact register
using the [code-evidence rules](references/code-evidence.md). Cover roles, internal and
external systems, functions, domain entities, and exchanges in the selected scenarios.
Keep technical detail in the register rather than overloading the overview sheet. Mark
unknowns; do not infer infrastructure from library names. Old images and web searches are
unnecessary for routine use. For a new legend or a request for strict compliance with a
standard, verify rule applicability using the cited sources.

## Construction

1. Inspect entry points, dependency composition, service operations, actual external calls,
   and result persistence. Compare with the UI if users appear in the diagram. Build a
   scenario register supported by code, tests, requirements, and any source diagram; define
   coverage boundaries. “All scenarios” means all confirmed scenarios within that scope,
   not hypothetical variants.
2. For the information view, follow the [composition and exchange rules](references/information.md).
   Name blue components `АС. Компонент. Подкомпонент`; show functions as separate yellow-orange
   blocks and entities as separate green cylinders. Transit does not require a cylinder in
   every intermediate component. Label links with data and the called service; direct arrows
   by primary data flow, and place the yellow numbered circle by the service provider/master
   system. Interface numbers are global to the OTAR, not execution-stage numbers.
3. For the functional view, follow the [scenario rules](references/functional.md). Preserve
   executors, exact function names, and interface numbers from the information model. Use
   one action per block. The primary profile from new examples uses blue actions, green start,
   and pink end with a thick outline. Show component data as cylinders and transmitted
   instances as folded-corner objects, with dashed data links. Do not mix this with the older
   shape profile unless explicitly requested.
4. In the functional view, show material calls, returns, conditions, and independent launches;
   do not turn the information view into an HTTP trace. Distinguish data movement from
   execution. Put complex scenarios on linked sheets with clear entry/exit points within the
   same functional diagram; do not compress multiple operations into prose to reduce block count.
5. Use the [shape examples](assets/notation.drawio) and
   [coordinated two-view example](assets/example-pair.drawio) as editable references.
   Preview them as [shapes](assets/notation.svg) and [the diagram pair](assets/example-pair.svg).
   These are teaching examples, not official
   bank templates. Export and validation details are in the [delivery rules](references/delivery.md).

This package does not prescribe technologies, system names, sheet count, a mandatory queue,
or background processes. Include them only when found in the project. Multiple sheets are
allowed for readability, but the deliverable is still one architecture diagram and one
functional diagram per project, not competing alternatives.

## Result Validation

Validate both diagrams against the scenario register: every confirmed in-scope scenario
must have a functional path from trigger to outcome, and all views must represent one
project model rather than unrelated alternatives. Every action needs an executor, every
exchange a source/receiver and data, and every store a verified owner. The service provider
is not necessarily the data source. Check marker placement, global numbering, full component
names, exact function-name matches, and the absence of lists of unrelated entities/actions
inside one shape. Verify branch conditions, commit/cleanup order, and independent background
work. Check action atomicity, scenario coverage, and consistency between views. Identical
names used by different executors do not make one function. Open the rendered output and
inspect readability, arrows, colors, and shapes.

Do not finish with a sketch unless a concrete blocker prevents completion. Before replying,
create and validate every requested final file. If information is missing, continue with
explicitly labelled unknowns wherever safe, and stop only for a decision the user must make.
Report what changed, where the result is stored, and remaining assumptions. Preserve the
evidence register in Draw.io shape properties or beside the diagrams in an allowed format
so later updates can rely on code and stable notation rules. Do not describe XML validation
as visual editor review or as proof of full compliance with the internal OTAR standard.
