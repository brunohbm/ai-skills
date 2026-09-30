---
name: checkpoint
description: Pauses a chat, task, or specific topic by writing a short, self-contained checkpoint note that lets the user pick it up later without rereading or reconstructing anything. The note leads with the next concrete action and records the current state, open questions, decisions already made, what is left, and where to look. It is formatted with light-reading so it is easy to scan when coming back cold. Use whenever the user wants to pause, stop for now, park a topic, save where they left off, "continue tomorrow", has to leave or switch tasks, or asks for a summary "to pick up later", a checkpoint, or a note to their future self, even if they do not say "checkpoint". Also use when the user asks to pause only one specific subject inside a longer conversation. Portuguese triggers include "pausar", "vou parar aqui", "continuo depois", "salvar onde parei", "resumo para retomar", "tenho que sair", and "checkpoint".
license: MIT
metadata:
  tags: "Productivity, Task switching, Handoff, ADHD, Notes"
  category: "productivity"
---

# Checkpoint: pause now, resume without reconstructing

## Goal

Hand the work off to the user's future self. That reader comes back cold: hours or days later, maybe tired, maybe in a new chat with no history. The note succeeds if that reader can **start the next action within about two minutes, without rereading the conversation**. It fails if it only looks like a good summary.

Two ideas drive every choice below:

1. **The next action matters most.** Resuming is hard mainly because the suspended goal is gone from memory. A specific first action and a pointer to where it happens do most of the work.
2. **Record state, not history.** The reader needs to know what is true now, what is still open, and what is decided. They do not need the story of how the conversation got there.

## Workflow

### 1. Define the scope

- "Pause" with no subject means the active thread of the conversation.
- "Pause [subject]" means only that subject. Leave the other threads out.
- A pasted text or task description means that material, plus whatever the conversation adds to it.

If the conversation has several threads and it is unclear which one to pause, pick the most recent active one. Name it in the note's title so the user can correct it. Ask a question only when two threads are equally active. Pausing should cost as little as possible.

### 2. Extract (recall first)

Scan the scoped material and collect every candidate item before cutting anything:

- **Goal**: the outcome this work is aiming for.
- **State**: what is done. Mark each item honestly as *done and checked*, *done but not checked*, or *not started*. The most common handoff failure is calling something finished that was never verified.
- **Decisions**: what has been decided, with a short reason. Also list options that were rejected for a reason, so the same debate does not start again.
- **Open**: questions, doubts, hypotheses, blockers, and dependencies on other people.
- **Next action**: one verb plus one observable object plus where it happens. "Compare the April estimate against March in the 'Costs' tab" works. "Continue the analysis" does not.
- **What is left**: the remaining steps, counted if possible, with a time estimate only when there is a basis for one. Seeing clearly how much remains makes it easier to come back.
- **Pointers**: files, sections, links, messages, versions, or commands where the work lives.
- **What may change**: anything outside the user's control that could change during the pause, such as data, prices, other people's replies, open PRs, or deadlines.
- **Contingency**, only if a known branch exists: "If X, then Y."

### 3. Compress (then precision)

Cut whatever does not help the reader restart:

- the chronological narrative ("first we tried…, then…");
- tool output, long quotes, and code the reader can reopen from a pointer;
- repeated explanations, courtesies, and meta comments;
- detail that is safe to rebuild from the pointer.

Keep any detail whose absence would force real reconstruction, such as an exact value, a command that finally worked, or a reason behind a decision. When in doubt about one item, keep it as a single line.

### 4. Choose the size

| Situation | Format |
|---|---|
| The user must leave now ("I have to go", "quick pause") | **Minimal**: 2–3 lines |
| A simple topic, a short pause, a single thread | **Compact** (default) |
| Many decisions or dependencies, work that is hard to rebuild, a pause of days, or a note that will be pasted into a new chat | **Detailed** |

The user can override this with words like "short note" or "full note". Do not spend the user's exit time on a long note. If the pause is urgent, capture the next action and its pointer first. A note that is too short but correct beats a complete one that never gets written.

### 5. Write it with light-reading

See **Presentation** below. Write in the conversation's language. Use absolute dates ("2026-09-30"), not relative ones like "tomorrow".

### 6. Check before sending

Read the note as the future reader would, with no access to this chat:

- Does it lead with the next action, and can that action start in about two minutes?
- Does every reference stand on its own? Remove "as discussed above", "that approach", or any pronoun that points into the chat. Name the thing instead.
- Is the status of each item honest? Nothing unverified should be marked "done".
- Could any line be cut without forcing reconstruction later? If so, cut it.

### 7. Deliver

- Send the note as the whole reply, with no preamble or closing lines.
- **Save a file** when the user asks for one, or when you are working inside a project with filesystem access (for example, Claude Code in a repository). Follow the project's existing notes convention if there is one. Otherwise save to `checkpoints/YYYY-MM-DD-topic-slug.md` at the project root. Add one line after the note with the path.
- Without filesystem access, the note in chat is the deliverable.

## Templates

Labels follow the conversation's language. Drop any field that would be empty. Never write "N/A".

### Minimal (urgent exit)

```markdown
**Checkpoint: [topic] ([date])**
Next: [verb + object] in [where].
Open: [the one doubt or blocker].
```

### Compact (default)

```markdown
## Checkpoint: [topic] ([date])

**Next action:** [verb + object + where]

**Where I stopped:** [current state in 1–2 sentences; what is done and checked vs. not]

**Open:**
- [question / blocker / dependency]

**Left:** [N steps, ~time if known]: [the steps, briefly]

**Pointers:** [file, link, section, message]
```

### Detailed

```markdown
## Checkpoint: [topic] ([date])

**Next action:** [verb + object + where]
**Then:** [2nd and 3rd actions, in priority order]

**Goal:** [the outcome this work is aiming for]

**State**
- Done and checked: …
- Done, not checked: …
- Not started: …

**Decided (do not reopen)**
- [decision]: [short reason]
- Rejected: [option]: [why]

**Open**
- [question / hypothesis / blocker / who it depends on]

**Left:** [N steps, ~time if known]
**If [condition], then [alternative].**   ← only if a known branch exists

**Pointers:** [files, versions, links, commands, messages]

**Check on return:** [what may have changed during the pause, and how to confirm it]

> To resume in a new chat, paste this note and say: "Resume this checkpoint. Restate the state in 1–2 lines, flag anything that may be outdated, then start with the next action."
```

The last line of the detailed template matters when the reader is a fresh AI chat. It makes the receiver restate the handoff before acting, which catches misunderstandings early. This practice comes from structured clinical handoffs. It also makes the new chat check for stale state instead of trusting an old note.

### Example (compact, Portuguese conversation)

```markdown
## Checkpoint: orçamento da viagem (2026-09-30)

**Próxima ação:** comparar a cotação de hospedagem da Booking com a do Airbnb na aba "Hospedagem" da planilha `viagem-2026.xlsx`.

**Onde parei:** transporte fechado e conferido (R$ 1.840, voos já emitidos). Hospedagem com 2 cotações, ainda não comparadas.

**Em aberto:**
- A cotação do Airbnb inclui taxa de limpeza? O anúncio não deixa claro.

**Falta:** 3 passos, cerca de 40 min: hospedagem, alimentação e somar o total.

**Pistas:** planilha `viagem-2026.xlsx`, aba "Hospedagem"; link do anúncio na célula B4.
```

## Pausing a study session

If the paused thread is a `fast-learning` session, the next action on return is retrieval, not new material. Map the session state onto the note like this:

| Session state | Note field |
|---|---|
| REVIEW items, then CURRENT | **Next action**: "Answer from memory: [review items by name]", then NEXT |
| MASTERED, still provisional | State: *done, not checked* |
| MASTERED, confirmed after a delay | State: *done and checked* |
| GAP | **Open** |
| Remaining objectives | **Left** |
| SOURCE, with page, section, or timestamp | **Pointers** |

List review items **by name only**, never with their answers or explanations. A note that holds the answers turns retrieval into rereading, which is what `fast-learning` avoids.

In the detailed template, replace the resume line with: "Resume this study checkpoint. Quiz me on the review items before showing any content, then continue with the next lesson."

## Presentation: light-reading

This skill decides **what** goes into the note. `light-reading` decides **how it reads**. If it is available, load it and apply it to the note: use the skill tool if it is listed there, or read `../light-reading/SKILL.md` if the file exists. Give it this reader profile: the user themselves, coming back cold, maybe tired, maybe pasting the note into a chat with no history. The note's purpose is to execute the next step.

Scope and conflicts:

- Apply light-reading **to the note only**. Do not turn on its session-wide persistence unless the user has already done so or asks for it.
- Its "no recap" rule does not apply, because the note *is* the summary the user asked for. Its "lead with the next action" rule does apply, and it is why every template starts with the next action.
- Its list cap applies to the "Open" and "Left" fields. If there are more than five items, group them and rank them, and put the most important first.
- Keep the note plain text. Do not add diagrams, even when `use-diagrams` is available: the note must survive being pasted into a new chat or a text file.

If light-reading is not available, apply this minimum:

- Put the next action first. Short sentences, one idea each.
- Use plain, literal words. Write out an abbreviation the first time it appears in the note.
- Keep the same name for the same thing throughout the note.
- Bold only the field labels.
- Use lists only for parallel items. Use a sentence where a reason or a cause-and-effect link matters.

## Evidence and limits

The workflow combines findings that are each supported on their own. These include preparing to resume and leaving cues, planning for unfinished goals, structured handoffs, and compacting AI context. **The combination itself has not been tested as a package.** Do not present it as a validated method, and do not cite productivity gains. For sources, strength of support, and what was left out, see `references/evidence.md`. Consult it when the user asks why the note looks the way it does, or asks whether something is proven.
