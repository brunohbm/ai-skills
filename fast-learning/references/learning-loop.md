# Learning loop

Use this cycle for each micro-lesson:

`explain → attempt → retrieve → correct → apply → verify`

## 1. Prepare

Present only the knowledge needed for the next task. When useful, begin with a prediction question. It should allow a plausible hypothesis, not create artificial difficulty.

## 2. Explain

Give the shortest explanation that enables the user to take the next action. Explain what it is, why it exists, how it works, when to use it, and how it connects to what has already been learned, as needed. Do not repeat material the diagnosis showed the user already knows.

## 3. Demonstrate

When the knowledge is procedural and the user does not yet have the necessary schemas, show a worked example and explain the important decisions. Avoid narrating every line when it does not help with the task.

## 4. Get the user to act

After the explanation, ask the user to do something: answer, explain, predict, complete, correct, implement, classify, compare, or solve. Reading the explanation without attempting anything does not provide enough evidence of learning.

## 5. Retrieve

Ask for an answer without consulting the material. Prefer free recall when possible. Examples:

- "Explain X in three sentences."
- "Why does X happen?"
- "How are X and Y different?"
- "Reconstruct the steps."
- "What would change if Y were different?"

## 6. Correct

Classify the answer as correct, partial, incorrect, or blocked. Confirm what is correct; identify exactly what is missing or wrong and explain the correction. Ask for another attempt if useful. If the user is blocked, give a hint and gradually increase support before providing the answer.

## 7. Reduce support

Fade scaffolding as competence increases:

`full explanation → partial explanation → hint → no assistance`

Do not keep support in place after it is no longer needed.

## 8. Vary practice

Once the basic procedure is established, vary the problem's surface features:

`same concept → same problem type → different context → combine with another concept → new case`

The user needs to recognize when and why to use the knowledge.

## 9. Transfer

When the goal requires application, include at least one task that is not copied from the material: a new example, edge case, different context, problem without a named technique, error diagnosis, or strategy comparison. Solving only the studied example does not demonstrate transfer.

## 10. Decide whether to move on

Move on when the essential concepts are understood and retrievable and there is no critical gap for the next concept. Do not require perfection on secondary details; track them for review when relevant.

## 11. Interleave

Interleave concepts after the user has a sufficient foundation in each. The goal is to make the user choose which knowledge to use, not to mix tasks after a fixed number of lessons.

## 12. Integrate concepts

After a group of related concepts, ask the user to explain from memory how they connect and apply that relationship to a case. This checks whether the concepts form an integrated structure.

## 13. Track session state

Keep a simple session state:

```text
SOURCE: ...
GOAL: ...
PROGRESS: ...
CURRENT: ...
MASTERED: ...
GAP: ...
NEXT: ...
```

Show only what is needed to guide the next action; do not display the entire state in every message if it adds cognitive load.
