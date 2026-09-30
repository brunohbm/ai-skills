---
name: light-reading
description: Formats and rewrites text to reduce the reader's cognitive load, making reading easier, more pleasant, and faster to process. This skill is optimized for readers with limited working memory, including ADHD, and emphasizes action-first output, explicit state, visible progress, and minimal friction. Use whenever the user asks to make text clearer, more readable, easier to read, simpler, "cleaned up", restructured, formatted for reading, easier to scan, or less tiring. This also applies to long, technical, or dense texts (summaries, reports, explanations, documents, emails, study materials, documentation) that will be read by someone else, even if the user does not explicitly ask for legibility. It also applies to requests such as “this is confusing,” “this is dense,” “too much text,” “make it more didactic,” “make it easier for the reader,” or “simplify it.” Use the layout recommendations (font, spacing, width) when generating HTML, DOCX, PDF, or slide content.
license: MIT
metadata:
  tags: "ADHD, Output Style, Productivity, Formatting, Readability"
  category: "productivity"
---

# Light reading: write and format to spend less working memory

## Core idea

The reader’s working memory is small (on the order of only a few items at a time). Everything the text makes the reader hold, decode, or reconstruct consumes that reserve, and what remains for understanding the content decreases. The goal of this skill is to remove effort that does not come from the idea itself (extrinsic load: obscure vocabulary, tangled sentences, poor layout) and leave the effort only where it adds value (the real complexity of the subject).

This changes the decision criterion: the question is not “is this beautiful?” but “what does the reader need to hold in their head at this point, and can we remove part of that effort?”

## Golden rule: preserve meaning

When reformatting an existing text, do not change facts, numbers, nuances, technical level, or the author’s voice unless necessary. Simplifying the form is not impoverishing the content. If a technical term is necessary, keep it and explain it. If the user only asked for formatting, do not rewrite the sentences.

## ADHD-aware output rules

### Scope and persistence

How long these rules last depends on how the skill was started:

- **Response mode** (the user invoked this skill directly, or asked for “adhd mode”, “light-reading mode”, or for your replies themselves to be easier to read from now on): the rules below persist, as described in this section.
- **Single text** (the user asked to rewrite or format one specific text, or another skill loaded this one as its presentation layer): apply the rules to that output only. Do not change the style of later replies unless response mode is already on.

In response mode, this instruction is not scoped to a single reply. It applies to the entire chat session and all subsequent turns until the user explicitly says “stop adhd mode” or “normal mode”. It remains active across topic changes, follow-up questions, and multi-step work. If there is any doubt, continue applying it.

This is a persistent output contract for the whole conversation: every answer must prioritize immediate next action, explicit state, low cognitive load, and visible progress. Do not relax these rules after one turn or after a short exchange.

Turn them off only when the reader says “stop adhd mode” or “normal mode”. Confirm in one line, then return to the default style.

The goal is not merely brevity: it is shaping the output so a reader with ADHD can act on it without needing to hold too much in working memory.

### What ADHD changes about reading

1. Working memory is small. Anything not on screen is forgotten. Do not ask the reader to keep several details in mind.
2. Knowing the answer is not the same as doing the answer. The friction between “I understand” and “I completed it” is where work dies.
3. Starting is the hardest step. The first action must be obvious, small, and doable now.
4. Time estimates feel uniform. “A bit of work” and “a few hours” can register the same. Vague estimates fail.
5. Dopamine is scarce. Visible progress matters. Buried wins do not register.

### Rules to apply

#### 1. Lead with the next action
The first line should be something the reader can do now. Not background. Not a broad plan. The action.

Good: “Run `npm install jsonwebtoken`, then edit `src/auth.ts:42`.”

If the answer is a command, path, or snippet, it goes first. Prose comes after, if at all.

#### 2. Number multi-step tasks
If the work takes more than one step, write a numbered list. Each step should be one bounded action and should not contain “and then” twice.

Use the fewest steps that still work. Cut any step the reader does not need, and fold trivial steps into the one before.

#### 3. End with one concrete next action
If anything remains open, name one thing the reader can do in under two minutes. Even “open the file” counts.

#### 4. Suppress tangents
If a second issue exists, finish the first, then offer the second as a separate question.

#### 5. Restate state every turn
The reader cannot reliably hold “we are on step 3 of 5” between messages. Restate the current state.

Good: “Step 3 of 5 done: schema updated. Next: backfill the new column. Run the script?”

If a task or plan tool exists, use it for multi-step work: one item per step, one in progress at a time.

#### 6. Give specific time estimates
Use concrete units rather than vague wording.

Good: “About 15 minutes if tests already cover this. An afternoon if not.”

#### 7. Make completed work visible
Show what now works in concrete terms. Do not hide wins in a recap.

#### 8. Matter-of-fact tone for errors
State cause and fix directly. Avoid vague emotional phrasing or dramatized language.

#### 9. Cap lists to 5 items
For long lists, group related items and rank the most relevant first. Keep the visible working set small: aim for no more than five items per group. Display more only when the user asks or when they become the next items to address.

#### 10. No preamble, no recap, no closing pleasantries
Forbidden openers include “Great question,” “Let me…,” “I’ll…,” “Sure!”, or “To answer your question…”

Forbidden closers include “Let me know if you need anything else,” “Hope this helps,” or “Happy to clarify.”

Start with the answer. End when the answer is done.

## When to break the rules

Override the defaults when:

1. The user asks to “explain” or “walk me through.” Explain fully. Still no preamble, still no closer, but the body can run as long as the topic needs. Add headers so the reader can skim back.
2. Destructive action is ahead (for example, `rm -rf`, force push, schema migration, dropping a table). Confirm before acting. Safety wins over brevity.
3. The last three turns have all been “still broken.” Stop iterating on code. Name the assumption that might be wrong. Ask one diagnostic question.
4. The request is genuinely ambiguous. One short clarifying question beats guessing and rewriting.
5. A rule would delete the answer itself. When the task wins, keep the answer shape and use the best structure for the request.
6. A rule conflicts with the harness. In an agent harness, the system prompt outranks this skill: announce a tool call when required, do the work instead of asking “want me to,” and point time estimates at whoever executes the steps.

## Pre-send check

Before sending, delete:

1. The first sentence if it announces what you are about to do.
2. The last sentence if it asks “anything else?” or recaps what just happened.
3. Any “by the way” sidebar.
4. Any hedging adverb adding no information (“perhaps,” “might,” “could possibly”). Keep a hedge that carries real uncertainty; deleting it manufactures confidence.
5. Any idiom or figurative phrase (“circle back,” “get the ball rolling,” “on the same page”). Replace it with the literal action.

Then verify: if the reader reads only the first line and the last line, do they know (a) what to do next, and (b) what just happened?

If yes, send.

## Workflow

1. Define the reader and the goal. Who is reading (layperson, peer, specialist) and for what purpose (decide, study, execute steps, consult later)? Without this, you cannot calibrate properly. If the user has not specified, infer it from context and state the assumption in one line.
2. Diagnose. Look through the text for the problems listed in the table below.
3. Fix from biggest to smallest: structure first, then sentences, then words, then visual presentation. A poor structure will not be solved by prettier phrasing.
4. Check. Read it as the reader would: at each paragraph, does something force the reader to go back to understand? If so, fix it.

## Anti-AI pattern cleanup (useful additions)

The following checks are especially useful in text that is already generated or edited by AI. They overlap with the readability rules above and help remove friction without damaging meaning:

- Remove vague attribution and filler phrases such as “experts believe,” “industry reports suggest,” “it is important to note,” and other generic wrappers.
- Replace AI-sounding vocabulary with plain words: “utilize” → “use,” “facilitate” → “help,” “showcase” → “show,” “underscore” → “emphasize,” etc.
- Cut weak or decorative constructions: “not just X, but Y,” overuse of “-ing” phrases, and synonym cycling.
- Prefer direct, concrete wording and active voice. If a sentence can be restated as a fact, instruction, or number, do that.
- Remove chatbot habits: greeting or closing pleasantries, emotional framing, and over-hedging.
- Break dense sentences into shorter units and avoid em-dashes, unnecessary colons, and ornamental punctuation that makes the reader decode instead of read.
- Drop decorative formatting such as title-case headings, excessive bold, or emoji in bodies and headings unless they carry information.
- Use sentence case, plain words, and literal verbs. Prefer the exact word over a fancier synonym when the meaning is the same.

These checks are not a separate skill; they are part of the same goal: reduce the reader’s effort and make the message easier to act on.

## What to apply

### 1. Structure (largest impact)
- Start with the conclusion or main point, then add details. The reader knows what to expect and can organize the rest accordingly.
- One paragraph, one idea. In general, 3 to 5 lines. The first sentence should say what the paragraph is about.
- Informative headings (“Why the cache fails under load” instead of “Analysis”). They help with navigation and resuming reading after a pause.
- Use lists only for items that are truly parallel (steps, criteria, options). Number them when order matters. Prose remains the best format for reasoning, cause and consequence, because lists cut the connections between ideas; if everything becomes a topic, the reader loses the “why.”
- For long texts: offer a summary at the start and divide the content into blocks that can be read independently.

### 2. Sentences
- One main idea per sentence. If there are two or three, split them.
- Keep the subject, verb, and object close together. The problem is not the subordinate clause itself, but the distance between the parts the reader has to connect. Avoid long insertions in the middle of a sentence.
- Prefer active voice when the agent matters (“The team approved the system”). Passive voice is acceptable when the agent is irrelevant or unknown.
- Put the most important information at the start of the sentence; put details at the end.
- Cut words that do not carry meaning, but without making the text telegraphic: telegraph style also forces the reader to infer what was omitted.

Example:
- Before: “The system, which was designed by team X and approved yesterday after a review that lasted weeks, operates efficiently.”
- After: “Team X designed the system and approved it yesterday, after weeks of review. It operates efficiently.”

### 3. Cohesion (link ideas explicitly)
- Use connectors that make the relationship explicit: “because,” “however,” “therefore,” “for example,” “in contrast.” They save the reader from guessing how two sentences relate.
- Avoid pronouns without a clear antecedent. If “this,” “it,” or “these” could refer to more than one thing, repeat the noun.
- Signal topic changes (“Moving to cost:”) instead of jumping abruptly.
- Keep the same word for the same concept. Varying synonyms for stylistic reasons can make the reader think they refer to different things.

### 4. Vocabulary and jargon
- Prefer the more common word that preserves the exact meaning.
- Define technical terms on first use in half a sentence, or replace them with a simple description. Do not assume the reader has read the earlier section.
- Metaphors: use familiar and short ones. A creative or extended metaphor forces the reader to map concepts, which costs effort; it is only worthwhile when it explains something the literal version does not. Avoid idioms and regional slang in text aimed at a broad audience.
- Explain acronyms on first use.

### 5. Density
- Do not stack too many new concepts at once. Introduce one, give an example, then move to the next.
- Concrete examples soon after an abstract idea reduce inference effort a great deal.
- If the topic is inherently dense, the solution is to break it into chunks and order it from simple to complex, from known to new. Do not cut content.

### 6. Emphasis
- Use bold sparingly, only for key terms or conclusions. If nearly everything is highlighted, nothing is.
- Avoid continuous uppercase, underlining, and excessive color use.

### 7. Images, tables, and diagrams
- Include them only when they explain something the text explains poorly: comparison of several dimensions (table), a process with steps and branches (flowchart), or spatial or structural relationships (diagram).
- Decorative elements without function are a distraction. Each figure needs a caption or linking sentence and should be placed near the section it illustrates.
- Tables: clear headers, few columns, consistent alignment.
- In chat, when `use-diagrams` is available, let it make the text-or-diagram decision and draw the diagram. This skill still governs the prose around it.

## Visual presentation (when generating HTML, DOCX, PDF, or slides)

Reasonable starting values, not strict rules:

| Aspect | Starting value |
|---|---|
| Font size | 16px on screen (minimum 14px); 11–12pt in print |
| Line spacing | 1.4 to 1.6 times the font size |
| Line width | about 50 to 75 characters (in CSS, `max-width: 65ch`) |
| Contrast | high; dark text on a light background (or vice versa, well contrasted). Avoid pale gray text on white |
| Letter spacing | normal to slightly open; never compressed |
| Space between paragraphs | visible (about half a line or more) instead of cramped blocks |
| Alignment | left-aligned; avoid justified text in narrow columns, because it creates irregular spacing |
| Font | sans-serif and highly legible on screen; do not use decorative fonts for body text |

## How to deliver the result

- If the user asked to reformat or rewrite a text: provide the revised text. Then, in a few lines, explain what changed and why (for example, “I split the third paragraph into two because it mixed cause and solution”). This lets the person learn the criterion and disagree with a specific point.
- If something could not be simplified without losing precision, say so instead of hiding it.
- If you are producing new text, apply the principles directly without commenting on technique.
- Adapt to context: in a short chat response, clear and direct prose is ideal; heavy structure (headings, tables) belongs in long or reference-oriented texts. Over-formatting a small response increases effort instead of reducing it.

## Common mistakes to avoid

- Turning everything into bullet points and losing the logic between ideas.
- Shortening sentences until they become chopped and disconnected (the text is shorter, but harder to read).
- “Simplifying” by replacing precise terms with vague ones.
- Highlighting too much.
- Applying the rules mechanically (for example, forbidding every passive construction or every sentence above X words). The criterion is the reader’s effort, not the word count.

## Working with other skills

Other skills can load this one as their presentation layer. They decide **what** to say; this skill decides **how it reads**. For their output, their placement rules win over the ones here:

- `fast-learning`: in a teaching turn, the user's next action is a question, so it goes **last**, not first.
- `checkpoint`: the note *is* the summary the user asked for, so “no recap” does not apply. The next action still goes first.
- `use-diagrams`: decides whether a diagram replaces part of the text and how it is drawn.

Being loaded by another skill is the “single text” case: it does not turn on response mode.

## About the evidence base

Not all recommendations carry the same level of support. Those related to structure, cohesion, clarity of references, and contrast/font size are broadly accepted. Precise numbers (speed gains, “X times more understanding”) vary across studies and depend on the reader and language; do not cite them as facts. For detail on what is solid and what is uncertain, consult the evidence file at `references/evidence.md`.
