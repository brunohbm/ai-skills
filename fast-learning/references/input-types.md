# Input types

The source determines part of the method. Do not use the same process for a research paper, API documentation, a programming video, and a vocabulary list.

## Article or research paper

Prioritize the problem, hypothesis or objective, necessary concepts, method, results, interpretation, limitations, and implications. Distinguish what the author claims from what the results actually demonstrate. Do not treat the author's conclusion as independent evidence.

## PDF

First identify the document structure. Tables, charts, diagrams, equations, screenshots, and figures may be learning units. Do not ignore relevant visual information just because it is missing from extracted text. If a figure is necessary, describe its role and ask the user to interpret it.

## Documentation

Prioritize `concept → prerequisite → setup → example → behavior → error → application`. Teach the path needed for the goal, not the entire documentation. For an API, this might mean the mental model, authentication, a minimal request, the response, an error, and a real use case.

## Code or repository

Prioritize architecture, flow, responsibilities, dependencies, important decisions, examples, extension points, and common errors. For code, progress through `predict → explain → run → modify → debug → create`. Do not start by asking the user to write everything from scratch if they do not yet have the necessary mental model.

## Video or lesson

Use a transcript as a textual source when available, and preserve important visual demonstrations. Turn the content into learning objectives, not a sequence of minutes watched. The user does not need to rewatch every segment to demonstrate learning.

## Slides

Slides may be conceptually dense and provide little context. Reconstruct the concepts, relationships, necessary context, and missing examples. Do not treat every slide as a required unit.

## Book or chapter

Start with the chapter's goal, concepts, arguments, examples, and applications. Split by conceptual dependencies, not necessarily by page.

## Short technical text

Do not force a complex map for a short text. Use `central idea → explanation → retrieval → application`.

## Images and diagrams

Use visual information when spatial or visual features matter. Do not add images just for decoration. Ask the user to interpret a figure when that is part of the goal.

## Multiple sources

Establish a primary source and use the others as supplements. Flag contradictions, do not merge different positions as if they were one, and preserve the origin of claims when it matters.

## Inaccessible or incomplete source

Do not invent missing content. State which parts could not be analyzed and proceed only with the available material. If the missing section is essential, ask for the source or the relevant excerpt.
