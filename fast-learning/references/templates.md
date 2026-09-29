# Templates by knowledge type

Use these after classifying what the user wants to learn. Each section explains where to focus effort, how to adapt the lesson cycle, and which questions to ask.

## Contents

1. Learning from a source
2. Conceptual
3. Factual (vocabulary, terminology, dates)
4. Procedural (math, programming, techniques)
5. Languages
6. Exam, certification, or interview preparation
7. Ready-to-use prompts

## 1. Learning from a source

When the user provides a source:

1. Identify the learning goal.
2. Extract the relevant structure and dependencies.
3. Sort material into essential, important, secondary, and reference-only content.
4. Create observable objectives and order them by dependency.
5. Teach in micro-lessons with retrieval, feedback, and application.
6. Test transfer when the goal requires application, and track gaps.

Do not automatically turn the source into a summary. A summary is a reference artifact; learning is demonstrated by the user's performance. For the full workflow, see `source-learning.md`.

## 2. Conceptual

Focus: relationships, causes, and counterexamples.

- Start with a map using labeled arrows ("causes", "is an example of", "depends on").
- In each lesson, prioritize self-explanation ("Why does this happen?") and transfer questions ("What changes if X is different?").
- Retrieval prompts: "Explain it to a beginner," "How are A and B different?" or "Give an example that resembles this concept but is not one."
- Final test: ask the user to solve a new situation using the concept or identify the flaw in a plausible but intentionally incorrect explanation.

## 3. Factual

Focus: repeated, spaced retrieval; a few items at a time.

- Group by meaning, not alphabetically. Connect each item to something the user already knows (a personal example, image, or phrase).
- Introduce a small batch of new items at a time, and add more only when the user retrieves most of the current batch. There is no well-established ideal number; adjust it to how many items the user is actually retrieving.
- Use one question per flashcard. Ask the user to **create** their own examples; generating examples helps more than reading yours.
- Review missed items in the same session and again the next day; space items answered correctly farther apart.
- For large sets, suggest a spaced-repetition app such as Anki and offer to create the cards.

## 4. Procedural

Focus: worked examples with fading support, followed by varied practice.

For each technique:

1. Show a fully worked example and explain *why* each step is taken. Ask the user to explain one step you choose.
2. Give a problem with one or two steps left blank.
3. Give a complete problem to solve independently, offering graduated hints only if needed.
4. Give a variation using the same technique in a different context.
5. After 2 or 3 techniques, interleave problems without naming which technique each one requires.

For programming, ask the user to predict the output before running the code, explain it line by line, and debug an intentional error. Writing from scratch comes after reading and prediction. Do not provide the complete solution before the user tries.

For math and science, ask which principle applies and *why* before calculating. Track sign and unit errors as learning gaps.

## 5. Languages

- Treat comprehension and production separately: listening/reading and speaking/writing train different skills; practice what the goal requires.
- Prioritize vocabulary by frequency and relevance to the user's goal; learn words in sentences, not in isolation.
- For retrieval, ask the user to produce a sentence (for example, translate from their native language into the target language) before showing the answer.
- Simulate a conversation about a topic relevant to the user's goal. Correct the most frequent errors, not all of them at once.
- Pronunciation and listening require audio. State when pronunciation cannot be assessed from text.

## 6. Exam, certification, or interview preparation

- Start with the **exam format and topic weights**. Study in proportion to what is tested, not what is most interesting.
- Diagnose with exam-style questions before studying; use the errors to shape the plan.
- Start with topics that carry the most weight and have the largest gaps.
- Finish with a timed practice test and categorize errors (did not know, confused despite knowing, inattentive, or ran out of time).
- Check exam rules, current editions, and criteria against an official source; the information may have changed.
- For interviews, practice answers aloud and review them. Knowing an answer and articulating it are different skills.

## 7. Ready-to-use prompts

Calibration questions (choose only what is needed):

- "What will you be able to do once you have mastered this? Give a concrete example."
- "How much time do you have, and what is your deadline?"
- "Tell me what you already know, even if it is not much, or answer these three diagnostic questions."

Retrieval prompts:

- "Without looking, explain [concept] in three sentences."
- "How are [A] and [B] different, and when would you use each?"
- "What would happen if [condition] changed?"
- "Find the error in this explanation: ..."

Closing prompts:

- "Write down everything you remember about the topic without looking anything up."
- "From 0 to 100%, how confident are you that you can explain [X]? Now explain it."
