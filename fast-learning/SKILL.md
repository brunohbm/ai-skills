---
name: fast-learning
description: An adaptive system for learning new material from articles, PDFs, documentation, books, videos, lessons, and other sources. Turns sources or goals into micro-lessons with active retrieval, practice, feedback, and application tests until the user demonstrates sufficient mastery for their goal. Use when the user wants to learn, study, understand, or master something; asks to be taught; wants a study plan; prepares for an exam, interview, or certification; or wants to learn from a source.
---

# Fast learning

## Goal

Maximize demonstrable learning per unit of time. Progress is not pages read or content explained; it is what the user can retrieve, explain, apply, and, when needed, transfer without relying on the source or the AI.

## When a source is provided

When the user provides or points to an article, PDF, documentation, chapter, book, video, lesson, or other material:

1. Identify the learning goal; ask only if it is ambiguous.
2. Inspect the source structure and identify relevant core concepts, dependencies, examples, evidence, and limitations.
3. Sort the material into essential, important, secondary, and reference-only content.
4. Create observable learning objectives and order them by dependency.
5. Teach in micro-lessons with retrieval and application, and track gaps.
6. Test mastery according to the goal and the required level of evidence.

See `references/source-learning.md` to turn a source into a learning sequence and `references/input-types.md` to adapt the process to its format. Treat the source as the authority for source-specific claims: do not invent missing content, and check the material for important details.

## When no source is provided

Build the map from the goal and available knowledge. Follow `goal → diagnosis → map → micro-lessons → retrieval → practice → transfer → review`, adjusting the scope to the available time and prior knowledge. Do not ask again for information that is already clear.

## Teaching principles

### Teach interactively

Present only what is needed for the next task. After a short explanation, ask the user to retrieve, explain, decide, or apply. The AI's explanation alone does not demonstrate learning.

### Adapt the support

Diagnose prior knowledge and adjust the level of support:

- **Beginner**: pre-train essential components, demonstrate examples, and provide scaffolding.
- **Intermediate**: prioritize retrieval, varied practice, comparison, and partially open-ended problems.
- **Advanced**: start with problems, edge cases, diagnosis, and transfer.

Reduce assistance as competence grows. Do not repeat explanations for material the diagnosis shows the user already knows.

### Use functional micro-lessons

A micro-lesson teaches one unit that can be explained, retrieved, applied, or connected to another concept. There is no fixed duration. Split it when too many new concepts appear, the goal changes, or a dependency should be taught separately.

Default structure: `brief context → minimal explanation → example, if needed → user action → retrieval → feedback`.

For procedures, use `worked example → partial practice → independent attempt → variation → transfer`, gradually removing support. See `references/learning-loop.md` to guide each cycle.

### Advance based on evidence

Move on when the essential concepts are understood and retrievable, with no critical gaps for the next objective. Do not require perfection on secondary details. When the goal requires application, include at least one case that differs from the examples studied.

### Choose the mastery level

Choose the criterion based on the goal: retrieval may be enough for peripheral facts; important concepts require explanation and connections; procedures require independent application; practical skills should include transfer when possible. Do not declare mastery based only on recognition, rereading, or repeating an example. See `references/mastery.md`.

### Track progress without adding clutter

Track the goal, source, learning objectives, progress, mastered material, gaps, and next lesson. Show only what helps the user understand where they are and what to do. When ending a session that will continue later, offer a compact state card.

## Presentation and readability

When `light-reading` is available, use it as the presentation layer. This skill decides what to teach, in what order, and when to test, move on, or review. `light-reading` decides how to structure and present the response to reduce extraneous load and make the next action clear. Do not duplicate its presentation rules here.

## Review and limited time

Use spaced retrieval when knowledge needs to remain available for weeks or months. If the goal is immediate use, focus on application and transfer. Review should begin with an attempt to retrieve, not with rereading. Formal schedules are optional.

When time is limited, reduce the scope, not the quality of the learning cycle: prioritize the highest-impact goal, one retrieval attempt, one application, and one test. State what was left out.

## References

- `references/source-learning.md`: turn sources into objectives and micro-lessons, preserve traceability, and prioritize content.
- `references/learning-loop.md`: guide explanation, practice, retrieval, feedback, and transfer.
- `references/mastery.md`: assess mastery and decide when an objective has been met.
- `references/input-types.md`: adapt the process to articles, PDFs, documentation, code, videos, slides, and multiple sources.
- `references/templates.md`: adapt practice to knowledge types and find ready-to-use prompts.
- `references/techniques-and-evidence.md`: evidence, limitations, and strength of support. Consult it when the user asks about the method or techniques need comparison.
