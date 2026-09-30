# Evidence behind the checkpoint note

Consult this file when the user asks why the note is shaped this way or whether something is proven, and before citing any number.

## Summary

Each component has its own support. The package does not. No trial was found that compares a full note (state, next action, pointer, open items, preservation, trigger) against a control condition, across varied jobs, after pauses that range from minutes to days. No study establishes an ideal note length, an optimal number of fields, or that writing a note always beats an automatic activity trail. Present the method as **a prudent routine derived from studied mechanisms**, not as a validated intervention.

## Components with direct experimental support

| Claim | Where it shows up in the skill | Sources |
|---|---|---|
| Interruptions delay resumption. Longer and more demanding interruptions cost more. | Why the note exists at all | [Monk, Trafton & Boehm-Davis, 2008](https://doi.org/10.1037/a0014402) |
| A brief ready-to-resume plan made before switching reduced attention residue and protected performance on the next task, especially under time pressure. | Next action; workflow step 2 | [Leroy & Glomb, 2018](https://doi.org/10.1287/orsc.2017.1184); [Leroy, 2009](https://doi.org/10.1016/j.obhdp.2009.04.002) |
| Planning the resume goal and having cues available on return sped up resumption. Changing the goal-related cues hurt it. | Next action + Pointers | [Trafton et al., 2003](https://doi.org/10.1016/S1071-5819(03)00023-5); [Altmann & Trafton, 2004](https://interruptions.net/literature/Altmann-CogSci04.pdf); [Hodgetts & Jones, 2006](https://doi.org/10.1037/0278-7393.32.5.1120) |
| Being forced to write during a very short window (6 s) *increased* resumption time. Visual cues helped. | Minimal format for urgent exits | [Clifford & Altmann, 2004](https://www.interruptions.net/literature/Clifford-CogSci04.pdf) |
| Unfinished goals can cause intrusive thoughts. A specific plan reduced that effect in lab studies. | Open + Next action | [Masicampo & Baumeister, 2011](https://doi.org/10.1016/j.jesp.2010.12.011) |
| With programmers, automatic chronological activity cues did better than free-form notes alone. | Pointers (prefer concrete locations over prose) | [Parnin & DeLine, 2010](https://doi.org/10.1145/1753326.1753342) |

## Structured handoffs (strongest field evidence, different domain)

In the **I-PASS** study, handoffs between medical residents were structured as: illness severity, patient summary, action list, situation awareness and contingency plans, and synthesis by the receiver. Across 10,740 admissions in nine pediatric residency programs, medical errors fell 23% (from 24.5 to 18.8 per 100 admissions). Preventable adverse events fell 30%. ([Starmer et al., 2014, NEJM](https://psnet.ahrq.gov/resources/resource/28485); [Intermountain summary](https://intermountainhealthcare.org/news/2014/12/multicenter-patientsafety-study-reduces-medical-error-injuries-by-30))

What the skill borrows:
- **Action list**: the "Next action" and "Then" fields.
- **Contingency plans**: the "If X, then Y" line, used only when a known branch exists.
- **Synthesis by receiver**: in the paste-into-new-chat line, the new chat restates the state before it acts.

Caveats: the intervention was a whole *bundle* (mnemonic, training, role-play, observation, and culture change), not the mnemonic alone. The setting was clinicians handing off to *other people*, not to their future selves. Do not transfer the percentages.

## Continuity for AI sessions (engineering practice, not controlled trials)

Anthropic describes how it keeps long-running agents on track across context resets:

- **Compaction** keeps architectural decisions, unresolved bugs, and implementation details, and discards redundant tool output. The advice is to tune for **recall first, then precision**. That is the order of workflow steps 2 and 3. ([Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))
- **Structured notes** are kept outside the context window, such as a progress file, and read back after a reset. A new session first gets its bearings from these notes and the history, then checks that the current state works before it starts new work. Failures they observed include declaring work finished too early, marking features complete without end-to-end testing, and leaving state that was buggy or undocumented. This is the reason for the honest status labels and the "Check on return" field. ([Effective harnesses for long-running agents](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents))
- Language models use information at the **start or end** of a long context better than information in the middle. This is one more reason to put the next action at the top and keep the note short. ([Liu et al., 2023, "Lost in the Middle"](https://arxiv.org/abs/2307.03172v3))

## Moderate or indirect support

- **Seeing what is left.** In the "Hemingway effect", motivation to go back to an unfinished task was higher when less remained. The effect appeared only when the task was structured enough for people to judge how much was left. That supports the "Left" field. The studies used undergraduates on copying and writing tasks, so the effect size in real work is unknown. ([Oyama, Manalo & Nakatani, 2018](https://researchmap.jp/read0151030/published_papers/22619952))
- **Writing it down beats trusting memory.** A meta-analysis found a robust *tendency to resume* unfinished tasks (the Ovsiankina effect). It found no reliable *memory advantage* for them (the Zeigarnik effect). The urge to come back survives; the details do not. ([Ghibellini & Meier, 2025](https://ideas.repec.org/a/pal/palcom/v12y2025i1d10.1057_s41599-025-05000-w.html))
- **"When X, I will do Y."** Implementation intentions have broad support in prospective memory research. That support is only indirect for resuming professional work. ([Gollwitzer & Brandstätter, 1997](https://pubmed.ncbi.nlm.nih.gov/11760131/))

## Design choices that are practical, not evidence-based

These choices follow the mechanisms above but were never tested directly:

- the two-minute test for the next action;
- the three sizes and when to use each;
- the honest status labels;
- the "Rejected" list, which prevents the same debate from starting again;
- the file path convention;
- the cap of five items per list, which comes from light-reading.

If the user wants to calibrate the routine, compare how they resume similar tasks with and without a note. Did they find the right spot? Did they start without rereading? Did the first action still make sense? This personal test does not prove causation, but it shows whether the note is worth its cost for them.
