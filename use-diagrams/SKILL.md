---
name: use-diagrams
description: Decides whether content is best understood as text or as a diagram and, when it is a diagram, draws it inline in the chat itself with the Visualizer (show_widget), never as an artifact or file. Use when an answer or pasted material has structure the reader would otherwise have to picture (a process with branches or 4+ steps, a system or mechanism, a hierarchy, a cycle, a timeline, relationships among 3+ entities, a trade-off on two axes, or numbers with a pattern), even if the user doesn't ask for a diagram. Also use when the user asks to see, draw, or visualize something. Portuguese triggers include "desenha", "mostra num diagrama", "visualizar", and "faz um esquema".
license: MIT
metadata:
  tags: "Diagrams, Visualization, Data viz, Explanation"
  category: "visualization"
---

# Use diagrams: decide, then draw inline

This skill has a single job: decide **text or diagram** for the content at hand and, if diagram, draw it **inline in the chat**, following the interface's native visual style.

- If the decision is **text**: answer normally. Don't mention the skill, the decision, or "I chose not to draw".
- If the decision is **diagram**: pick the family based on the relationship the content needs to show, render with `show_widget`, and keep the text explanation around it.

This applies both to the content of your own answer and to material the user pasted or attached.

---

## Step 1 — Text or diagram?

### The principle

Larkin & Simon (1987, *Why a diagram is (sometimes) worth ten thousand words*): text is sequential; a diagram indexes information by **position on the plane**. The diagram wins when it makes explicit relationships that, in text, the reader would have to reconstruct mentally, and when it puts side by side what needs to be compared, reducing search. When the information is already linear, singular, or depends on verbal nuance, the diagram only adds cost.

**Test question:** to follow this, would the reader need to build a mental image (where it is, what leads to what, what contains what, how it compares, what shape the numbers have)? Yes → diagram. No → text.

### Diagram signals (one is enough, if central to the answer)

- 3+ entities with non-linear relationships (network, dependency, mutual influence)
- process with 4+ steps, or with decisions, branches, or parallelism
- hierarchy, containment (A inside B inside C), parts of a whole
- cycle or feedback loop
- physical or abstract mechanism understood by *seeing* it ("how X actually works")
- numbers with a pattern: trend, distribution, compared magnitudes, composition, deviation from a reference
- timeline with 5+ events, durations, or overlaps
- trade-off on two axes (2×2 quadrant) or position on a continuum

### Text signals

- fact, definition, yes/no, short answer
- argumentation, opinion, ethical nuance, personal or emotional conversation
- linear sequence of up to 3 steps
- code, commands, text to copy
- exact values for lookup, or few items with many textual attributes → **markdown table** (still text)
- the visual metaphor would be arbitrary (drawing "the cloud" as a cloud teaches nothing)
- the user asked for brevity or said they don't want visuals

**When in doubt, text.** An unnecessary diagram violates Mayer's coherence principle: extra material competes for attention and hurts comprehension.

---

## Step 2 — Which relationship? → which family

The diagram's name decides nothing; the **relationship** does. Before drawing, answer: *what will an arrow, a position, an area, or a color mean here?* If it doesn't fit in a few words, the form is wrong.

| The content's question is… | Family | How to render |
|---|---|---|
| How does it work inside? | Illustrative: cutaway, exploded view, spatial metaphor | SVG; HTML + SVG if the real system has a control |
| What comes next, under which condition? | Flowchart, decision tree | SVG (flowchart) |
| What is inside what? | Structural (containment) | SVG (structural) |
| Which steps repeat? | Cycle | HTML stepper (never a ring) |
| What state is it in and what changes it? | State machine | SVG |
| Who does what? | Swimlane | SVG |
| How do the concepts relate? | Concept map (links labeled with verbs) | SVG |
| What belongs to which category? | Tree / taxonomy | SVG |
| What causes the problem? | Ishikawa (hypotheses) or causal loop map (feedback) | SVG |
| Why accept the conclusion? | Argument map | SVG |
| Where does it sit between two extremes? | Spectrum / continuum | SVG |
| How do options spread across 2 criteria? | 2×2 quadrant | SVG |
| When did it happen, how long did it last? | Timeline, Gantt | SVG or Chart.js (floating bars) |
| Who connects to whom? | Node network | SVG (few nodes) |
| What data exists and how does it relate? | ERD, class diagram | HTML + mermaid.js |
| How much flows from where to where? | Sankey | HTML + d3/d3-sankey |
| Which is bigger? | Bars, dot plot | Chart.js |
| How does it change over time? | Line | Chart.js |
| How is it distributed? | Histogram, boxplot, strip | Chart.js |
| Are two measures associated? | Scatter | Chart.js |
| How does the whole break down? | Stacked bar, waffle | Chart.js / HTML |
| Above or below the reference? | Diverging bars | Chart.js |
| Before → after per item? | Dumbbell / slope | Chart.js |
| One number matters (± trend)? | Stat tile / KPI | HTML |
| What is the estimate and the uncertainty? | Point + interval | Chart.js |
| Where is the geographic pattern? | Choropleth (rates), proportional symbols (totals) | HTML + d3 with real topology |

The detailed catalog (ideal data, best moment, caveats) is at the end of this file.

**Double question = two diagrams.** If the content calls for intuition *and* reference (e.g., "how it works" + "what the components are"), draw the illustrative one first, then the structural one, with prose between them. More than 5 nodes: overview first, then one diagram per sub-flow.

---

## Step 3 — Render inline

1. **Tool:** the Visualizer's `show_widget`. **Never** an Artifact, never a file, never a Mermaid/ASCII code block as a substitute for the drawing. The one exception: the user explicitly asks for a file, an artifact, or diagram code. Their request wins.
2. **Before the first `show_widget` in the conversation**, call the Visualizer's `read_me` with the right modules (`diagram`, `chart`, `interactive`, `mockup`, `art`). That guide is the authoritative source for classes, variables, sizes, and constraints; this skill doesn't replace it and, on any technical conflict, it wins. Do this silently: no "I'll load the module".
3. **Answer structure:** one or two sentences saying what the diagram shows → diagram → text explanation. Titles, long captions, and paragraphs stay **outside** the widget (contiguity principle: text nearby, but prose in the chat).
4. **Multiple diagrams:** always with prose between them; never two `show_widget` calls in a row. Promise only what you'll deliver.
5. **No Visualizer in the environment:** answer in text (markdown table if it helps) and say in one line that inline rendering isn't available here. Don't create an artifact as an alternative.
6. **Clickable nodes:** use `sendPrompt('…')` on nodes so the user can ask for details on a part. This keeps the diagram lean and turns deeper dives into conversation.

---

## Step 4 — Style

### Borders, corners, and surfaces (native style)

- Thin outlines: `0.5px`, with `var(--border)` (or `--border-strong` for emphasis). In SVG, `stroke-width="0.5"`.
- Corners: `var(--radius)` (8px) on controls, `12px` on cards; in SVG `rx="4"` (max `rx="8"`).
- Flat: no gradient, shadow, glow, or blur. Transparent background (the host provides the card).
- Typography: always sentence case; only weights 400 and 500; SVG at 14px (labels) and 12px (subtitles); nothing below 11px.
- No emoji; icons only Tabler outline, and never inside diagram boxes.

### Color — evidence-based rules

1. **Color encodes meaning, never order.** Same category = same color. Don't make a rainbow by step.
2. **2 to 3 ramps per diagram**, with gray for neutral/structural. More colors = more noise.
3. **Emphasis = one highlight + gray.** If the message is "this one", color only it (pre-attentive attribute); the rest stays gray.
4. **Never color alone.** Every distinction needs a second channel: direct label, shape, dashing, or hatching. About 1 in 12 men can't reliably tell red from green, so never separate information by red × green alone. Mental test: does it still work in grayscale?
5. **Contrast:** graphical parts required for understanding at least 3:1 against the background (WCAG 1.4.11); text with text contrast. On colored fills, text in the 800/900 shade of the **same** ramp (title 800, subtitle 600 in light mode).
6. **Scale type follows data type:**
   - categorical: fixed palette order, at most 8; beyond that, group into "Other" or use small multiples
   - sequential (magnitude): one hue, light → dark
   - diverging (above/below a reference): two hues with neutral gray in the middle, never a hue in the middle
7. **Reserved semantics:** blue, green, amber, and red carry UI meaning (info, success, warning, error). For general categories, prefer purple, teal, coral, and pink.
8. **Dark mode is mandatory.** In SVG/HTML, use the ramp classes (`c-purple`, `c-teal`…) and CSS variables, which adapt on their own. Fixed hex only on canvas (Chart.js), using the categorical palette from the Visualizer guide, which starts with the colorblind-safe blue/orange pair.

Why not use Okabe-Ito or Paul Tol directly: they are the reference palettes for color blindness, but they have fixed hex values that don't adapt to dark theme and clash with the native look. The native ramps, together with rules 3 to 5, achieve the same goal. Use Okabe-Ito only if you need fixed colors outside the renderer.

### Legibility (Mayer, data visualization)

- **Direct label > legend.** Name next to the line, bar, or node; legend only when direct labels would collide (around 5+ close series).
- **Coherence:** cut everything that doesn't serve the message (heavy gridlines, decorative borders, 3D, ornamental icons).
- **Signaling:** arrows and highlights only on the essential path.
- **Segmenting:** long content becomes several diagrams or a stepper, not one dense diagram.
- Boxes: subtitle of at most 5 words; up to 4 boxes per row; up to 5 nodes per flow. Trees, networks, and ERDs can hold more, but past about 5 nodes show an overview and let clickable nodes open the detail.
- Data: a single y-axis; recessive axes and gridlines; numbers always rounded; unit, denominator, and source explicit.
- Animation only if it shows real behavior (flow, rotation), and always respecting `prefers-reduced-motion`. Animation isn't automatically better than a static image.

---

## Step 5 — Checklist before sending

- [ ] Can I say in a few words what each arrow, line, area, and color means?
- [ ] Does the diagram answer **one** question?
- [ ] No overlapping labels; text fits in boxes; nothing outside the viewBox.
- [ ] Does it work in grayscale and in dark mode?
- [ ] No invented data. If numbers are illustrative or estimated, the text says so.
- [ ] Temporal order isn't presented as cause; correlation doesn't appear as causation.
- [ ] The main message is written in the text, not just implied in the drawing.

---

## Working with other skills

- **`light-reading`**: governs the prose around the diagram (sentence before, explanation after). If its response mode is on, keep the diagram lean and still end the message with the next action.
- **`fast-learning`**: in a teaching turn, the question comes last, after the diagram and its explanation. The diagram must not contain the answer to that question. A map shown once can become a later exercise: the user rebuilds it from memory.
- **`checkpoint`**: pause notes stay plain text. Do not draw inside them.

---

## Reference catalog

Organized by the relationship represented. "Caveat" indicates what the form omits or may distort.

### Mechanisms and objects (intuition)

| Type | When to use | Caveat |
|---|---|---|
| Cutaway / cross-section | Show the inside of something physical (engine, cell, heater) | Schematic, not portrait: simple silhouette, color by physical property (hot/cold) |
| Exploded view | Show how parts fit into a whole | Good overview, poor for detail of a single part; label each part |
| Annotated diagram | Name parts of a shape with callout lines | Labels all on the same side, outside the drawing |
| Spatial metaphor | Give shape to something abstract (attention, hash, call stack) | The metaphor must reveal the mechanism; if arbitrary, use text |
| Interactive with control | The real system has a knob, parameter, or input | Minimal control; the result changes visibly |

### Ideas, concepts, and arguments

| Type | When to use | Caveat |
|---|---|---|
| Mind map | Initial associations around a topic | Branches don't say what kind of relationship exists |
| Concept map | Relationships between concepts as propositions | Links need verbs; without them it becomes a list |
| Tree / taxonomy | Classes, subclasses, parts | Can't represent cycles or many-to-many relationships |
| Venn / Euler | Overlap, inclusion, exclusion between sets | Up to 3 sets; areas aren't proportional |
| Ishikawa | Organize possible causes of an effect | Hypotheses, not proof of causation |
| Causal loop map | Influences with feedback | Qualitative; indicate the sign (+/−) of influences |
| Argument map | Claim, evidence, objections | The link means support or rebuttal |
| Spectrum / continuum | Position items between two poles | Only works if there really is a single dimension |
| 2×2 quadrant | Classify options by two criteria | Axes must be independent and named |
| Layer stack | Levels that support each other (OSI networking, architectures) | Implies bottom-up dependency |
| Pyramid | Only if there's a real base → top (quantity or prerequisite) | Suggests hierarchy even when none exists |
| Before / after | Contrast between two states | Same scale and layout on both sides |

### Sequences, processes, and systems

| Type | When to use | Caveat |
|---|---|---|
| Flowchart | Steps and decisions toward an outcome | Flow in one direction; too many branches → split |
| Decision tree | Choices and their outcomes | Without probabilities, it's logic, not risk |
| Swimlane | Responsibilities and handoffs between roles | Few lanes; exception details in the text |
| Sequence diagram | Messages between participants in a scenario | One scenario per diagram |
| State machine | Discrete states and what changes between them | Only for truly discrete states |
| Cycle | Steps that repeat | HTML stepper with "next" looping back to start; a ring causes collisions |
| Timeline | Order and dates of events | Chronology ≠ causation; clear time scale |
| Gantt | Tasks, durations, and overlap | Dependencies may call for a complementary network |
| Journey | Stages of an experience and what happens in each | One persona and one scenario at a time |
| Structural | Containment and where each process happens | At most 2 to 3 nesting levels |
| Leveled architecture (C4 style) | System seen at increasing zoom | One level per diagram |
| Node network | Connections between entities | Layout may suggest nonexistent meaning; dense networks become tangles |
| ERD / classes | Entities, attributes, and cardinality | Use mermaid.js, not hand-made SVG |
| DFD | Origin, transformation, and destination of data | Doesn't show temporal order |
| Sankey | Quantity flowing between stages | Many crossings hide flows |

### Numeric data

| Type | When to use | Caveat |
|---|---|---|
| Stat tile / KPI | One number (and maybe the change) | Don't use a single-bar chart |
| Gauge | A ratio against a limit | Don't use a 2-slice pie |
| Bars / dot plot | Compare magnitudes, rank | Common zero baseline; sort by value if there's no natural order |
| Diverging bars | Deviation from a reference (target, mean, zero) | Explicit reference |
| Dumbbell / slope | Change between two moments per item | Few items |
| Line | Evolution over time | Never two y-axes; don't connect unordered categories |
| Area | One series over time emphasizing volume | Stacked only if the total matters |
| Histogram / boxplot / strip | Shape and spread of values | Bin width changes the reading; boxplot hides multimodality |
| Scatter | Association between two measures | Correlation isn't causation |
| Heatmap | Many values crossing two dimensions | Single-hue sequential scale; order rows with purpose |
| Stacked bar / 100% | Composition of a whole | Middle segments are hard to compare |
| Waffle / units | Concrete proportion ("3 in 10") | Only for few categories |
| Waterfall | How you get from a starting total to the final one | Only with a cumulative sequence |
| Small multiples | Many series on the same scale | Same axes in every panel |
| Point + interval | Estimate with uncertainty | Say what the interval is (confidence, prediction…) |
| Choropleth | Rate or proportion by region | Raw counts mislead; real topology, never invented coordinates |

---

## Decision examples

- "What is an API?" → **text** (definition).
- "How does TCP work?" → **illustrative diagram**: two endpoints, numbered packets in transit, ACK coming back.
- "What are the steps to deploy?" (6 steps, 1 decision) → **flowchart**.
- "Should I accept the job offer?" → **text** (personal decision, nuance). If the user lists options × criteria, a markdown table.
- "Explain the Krebs cycle" → **HTML stepper**, one panel per step.
- "How did price X evolve from 2015 to 2025?" with data → **line** (Chart.js). Without reliable data → text, no invented numbers.
- "Compare REST, GraphQL, and gRPC" → **markdown table** (textual attributes); an optional 2×2 only if there are two dominant criteria.
- User pastes a long text about a company's structure → **tree** (org chart) + text summary.
