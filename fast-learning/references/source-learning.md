# Learning from a source

Use this workflow when the user provides or points to an article, PDF, documentation, chapter, book, video, lesson, presentation, or other material and wants to learn its content.

The goal is not to produce a summary. Turn the source into a learning sequence that helps the user demonstrate enough mastery for their goal.

## Core principle

`source → structure → objectives → micro-lessons → practice → mastery`

The source is the reference material. Do not reduce the process to `source → summary → passive reading`.

## 1. Identify the goal

Determine what "learning" means in this context. The user may want to understand the main ideas, explain an article, implement a technique, reproduce an experiment, apply concepts at work, study for an exam, discuss the material critically, or memorize specific facts.

If the goal is clear, do not ask again. If it is ambiguous, ask only one question.

## 2. Inspect the source

Identify the structure, core concepts and dependencies, examples, procedures, arguments, evidence, tables, charts, diagrams, conclusions, limitations, and terms that require pre-training.

Do not treat every page or section as equally important. See `input-types.md` to adapt the inspection to the format.

## 3. Prioritize the content

Classify what you find:

- **Essential**: without it, the user cannot understand or apply the core idea.
- **Important**: deepens understanding or improves application, but does not block the goal.
- **Secondary**: useful for later exploration.
- **Reference-only**: a detail that can be looked up in the source when needed and does not need to be memorized now.

Learning quickly also means deciding what not to learn yet.

## 4. Build the learning map

Show the minimum structure needed to understand the material and its relevant dependencies. For example:

```text
Problem
  ↓
Concept A → Concept B
  ↓
Method → Result → Limitations → Application
```

Do not turn the map into an exhaustive copy of the table of contents. One figure may deserve its own objective; several pages may support a single idea.

## 5. Define observable objectives

Each objective should answer: "What should the user be able to do after this lesson?"

Prefer objectives such as explaining, distinguishing, predicting, applying, identifying when to use something, identifying a limitation, or reconstructing a procedure. Avoid objectives defined by page or section, such as "read page 15."

## 6. Order by dependency

Teach A before B when A is needed to understand B. Teach independent concepts in parallel when appropriate. To distinguish similar concepts, teach them and then compare them. For procedural material, move from the concept to an example, guided practice, independent practice, and transfer.

## 7. Create micro-lessons

Each lesson should teach one unit that can be explained, retrieved, applied, or connected to another concept. There is no fixed duration.

Split the lesson when too many new concepts appear, the explanation becomes long, the user must hold too much in mind, the goal changes, or a dependency can be taught separately. Organize instruction around the cognitive structure, not the amount of text.

## 8. Teach without dumping the source

Do not reproduce large passages. Explain the necessary idea in your own words and use examples when they reduce difficulty.

For difficult concepts, use `term → meaning → example → connection → retrieval`. For procedures, start with a worked example when the user does not yet have the necessary schemas.

## 9. Retrieve before continuing

After each important unit, ask the user to explain, reconstruct, predict, compare, apply, or solve without consulting the source. The AI's explanation is not evidence of learning.

## 10. Verify claims against the source

The source is authoritative for the material being studied. For numbers, specific claims, definitions, charts, methods, results, quotations, or experimental details, check the material before answering confidently.

Do not fill gaps in the source with invented content. If external knowledge differs from what the source says, make the distinction explicit.

## 11. Integrate groups of concepts

After roughly 2 to 4 related micro-lessons, when appropriate, ask for closed-book retrieval, mix the concepts, ask the user to explain a connection, and apply that connection to a new case. Adjust the number to the material; do not make it a rigid rule.

## 12. Finish according to the goal

Consider the material studied when the user can, as appropriate for the goal, reconstruct its structure, explain essential concepts, connect ideas, apply the knowledge, answer important questions, and handle at least one new case when transfer is required.

Only then produce a final summary, if useful. The summary records what was learned; it does not replace learning.

## 13. Interpret "learn everything"

Interpret this as learning all ideas relevant to understanding the source and achieving the goal, not memorizing every sentence, example, number, reference, or peripheral detail. Prioritize details accordingly. If the user needs to memorize specific facts, treat them as factual content and use spaced retrieval.
