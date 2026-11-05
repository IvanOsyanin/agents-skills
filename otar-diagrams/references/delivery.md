# Editable Output and Validation

Preserve the formats requested by the user. If no format is specified, a practical
set is an editable Draw.io file and an SVG preview; PNG is useful for embedding in
documents. Do not generate the diagram as an ImageGen raster: precise labels,
connections, and later shape editing matter here.

By default, deliver one final information diagram and one final functional diagram
for the project, consistent with each other and covering the confirmed scenarios
within the agreed scope. If the user requests only one view, deliver only that view.
Multiple sheets/pages are acceptable as parts of a single diagram; do not create
alternative files for each scenario, subsystem, or variant. Finish construction
and validation before the final response: do not stop at a draft unless the user
explicitly requested one or a blocking information gap cannot safely be marked unknown.

If the user supplies an existing architecture diagram, treat it as source context
and the basis for the final information diagram, not merely as a style reference.
Preserve confirmed components, boundaries, links, and IDs/numbers; verify and refine
them using available sources. Build the functional diagram from the refined model
without requiring the user to describe it again in text. Note non-blocking assumptions;
ask a question only when the scope or model meaning cannot be chosen correctly without
an answer. Do not destructively modify the user's source diagram.

[`notation.drawio`](../assets/notation.drawio) contains editable primitives, and
[`notation.svg`](../assets/notation.svg) shows their appearance. These are shape
examples, not a universal scenario layout. Copy suitable shapes; choose scale, lanes,
and sheet count based on content.
The coordinated teaching example is [`example-pair.drawio`](../assets/example-pair.drawio)
and [its SVG](../assets/example-pair.svg). It shows one successful scenario, exact
function names, two data-flow directions with provider markers, and shared interface
numbers across both views; it does not define the contents of a new project.
The assets use the primary profile from the new examples. To preserve an existing
style exactly, choose the alternative profile explicitly instead of mixing shapes.

If you use a generator, maintain one text/geometry model for all formats. Do not
fix only the PNG while leaving the Draw.io file different. For the primary data-object
profile, `shape=note` provides the visible fold used in the new examples. Only the
older no-fold profile needs another outline, such as an XML stencil; see the
[official Draw.io documentation](https://github.com/jgraph/drawio/wiki/Shapes-and-Stencils).

The teaching assets are generated from one text/geometry model with
`python scripts/build_assets.py` (Python 3, standard library only). It updates Draw.io/SVG
and removes stale PNG files when the SVG changes. Generate PNG with
`--browser <path-to-Chromium-or-Edge>`; this renders the SVG, not Draw.io.
Check example structure and consistency with `python scripts/build_assets.py --check`.
This script generates teaching assets; it is not a required generator for user diagrams.

Minimum validation:

- XML parses; IDs are unique; every source, target, and parent exists.
- Shapes and text fit within the page and parent containers.
- Arrows connect to the intended shape edges and do not cross unrelated shapes or labels.
- Conditions point to visible branches; returns and independent launches are preserved.
- IDs, full component names, exact function names, and interface numbers agree across
  the views; input data, results, and interaction modes agree with the evidence register.
- Text is readable at normal page scale; large diagrams use separate sheets.
- Each shape represents one function or entity; do not invent ownership for a transit component.
- Information-view arrows follow data flow and interface markers sit by providers;
  synchronization is not encoded by color. Technical ACKs and protocols do not clutter
  the overview sheet.
- Functional-view cylinders and folded-corner payloads are distinct and use dashed links;
  blue actions and green/pink events follow one selected visual profile.
- Visually inspect PNG/SVG in full and in detail. If an editor is available, inspect the
  Draw.io file there too; otherwise state the validation limitation honestly.

Geometry validation does not prove business correctness, and Draw.io syntax validation
does not prove that its actual rendering matches the SVG. Do not report hard-coded
counts of “checked” nodes; calculate them from the generated model.

Use portable paths relative to the Skill directory. `agents/openai.yaml` contains Codex
interface metadata; the instructions and resources do not require its API or any specific
generation tool. Follow this same `SKILL.md` in other environments. Do not claim that
Draw.io is a confirmed WebOTAR import format.
