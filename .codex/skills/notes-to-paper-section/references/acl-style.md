# ACL Style Reference

## Purpose

Use this reference when drafting or revising paper prose in ACL style from research notes.

The goal is not to imitate surface polish alone. The goal is to produce prose that is clear, technically precise, evidence-aware, and structurally disciplined.

## Core style

- Write in clear, direct, technically precise prose.
- Prefer explicit claims over rhetorical flourish.
- Tie every strong claim to evidence, derivation, citation, or clearly stated reasoning.
- Use cautious modality when evidence is incomplete.
- Keep terminology and notation consistent across the section.
- Define key concepts before relying on them.
- Prefer concrete description over vague praise.
- Make the logical relation between sentences easy to follow.

## Tone

ACL-style prose is usually:

- restrained rather than promotional
- analytical rather than impressionistic
- explicit rather than allusive
- specific rather than generic
- careful about uncertainty

Prefer wording such as:

- "We study..."
- "We consider..."
- "We define..."
- "Our results suggest..."
- "These findings indicate..."
- "This is consistent with..."
- "One possible explanation is..."
- "A limitation of this analysis is..."

Avoid wording such as:

- "This clearly proves..."
- "This dramatically outperforms..."
- "This is groundbreaking..."
- "This perfectly solves..."
- "This undeniably shows..."

## Claim strength

Match the strength of the wording to the support in the notes.

Use strong wording only when the notes clearly support it.

- Use "shows" or "demonstrates" only when the evidence is strong and direct.
- Use "suggests" or "indicates" when the support is partial, indirect, or observational.
- Use "is consistent with" when multiple interpretations remain possible.
- Use "we hypothesize" or "we conjecture" when the idea is plausible but not established.

If the notes are incomplete, soften the claim instead of inventing support.

## Working from notes

When the source material is a raw note dump:

- preserve the underlying technical meaning even if the original wording is rough
- smooth local phrasing, but do not invent missing experimental details, results, citations, or theorem conditions
- keep important domain-specific terms in the original form when translation would blur meaning
- if several note fragments express the same idea, merge them into one coherent paragraph
- if the notes contain ambiguity, either mark it explicitly or choose the narrower defensible formulation
- distinguish content grounded in the notes from content introduced only to improve readability

A good draft should feel publication-ready while remaining faithful to the notes.

## Paragraph structure

A strong ACL-style paragraph usually does the following:

1. State the point.
2. Define the object, problem, or contrast.
3. Explain the method, reasoning, or evidence.
4. Ground the claim with evidence, derivation, or comparison.
5. State the implication, limitation, or transition.

Not every paragraph needs all five moves, but most strong paragraphs should have a clear internal logic.

## Section patterns

### Problem setup

Use this when the section introduces the task, setting, or motivating challenge.

A good problem-setup paragraph usually:

1. defines the object of study
2. explains why the problem is difficult or important
3. identifies the gap in existing approaches or understanding
4. states the narrower focus of the present section

Useful moves:

- define the task before evaluating it
- name the source of difficulty explicitly
- distinguish the general problem from the specific problem addressed here

### Method

A method section should help the reader reconstruct what was done and why.

A good method paragraph usually:

1. states the component or design choice
2. explains its role in the overall approach
3. gives enough detail to understand the mechanism
4. explains why the choice is appropriate

Useful moves:

- introduce notation before using it
- explain inputs, outputs, and transformations explicitly
- separate design motivation from implementation detail
- use one paragraph per conceptual component when possible

Method paragraph template:

- "We model X as Y."
- "Given A, the system computes B by ..."
- "This design allows ..."
- "In contrast to prior approaches, this component ..."

### Related work

A related-work section should organize prior work analytically, not just list papers.

A good related-work paragraph usually:

1. names a research line or comparison axis
2. groups prior work by shared approach, assumption, or objective
3. states what those works achieve
4. identifies the specific distinction relevant to the present paper

Useful moves:

- compare prior work along a clear dimension
- state the relation to the current paper explicitly
- avoid vague claims of novelty without a comparison basis

Related-work paragraph template:

- "Prior work on X has mainly followed two directions."
- "The first line focuses on ..., whereas the second emphasizes ..."
- "Our setting differs in that ..."
- "This distinction matters because ..."

### Analysis

An analysis section should interpret results, not merely repeat them.

A good analysis paragraph usually:

1. states the pattern or finding
2. explains why it matters
3. offers a technically plausible interpretation
4. notes uncertainty, scope, or an alternative explanation when needed

Useful moves:

- connect the interpretation to the method or task
- separate observation from explanation
- avoid causal language unless justified
- note when the interpretation is tentative

Analysis paragraph template:

- "We observe that ..."
- "One plausible explanation is ..."
- "This pattern is consistent with ..."
- "However, the evidence does not yet determine whether ..."

### Limitations

A limitations section should name real constraints, not ceremonial ones.

A good limitations paragraph usually:

1. identifies a concrete limitation
2. explains its source
3. states how it affects interpretation or generalization
4. suggests a bounded implication for future work

Useful moves:

- be specific about scope conditions
- distinguish data limitations, modeling limitations, and evaluation limitations
- explain what cannot be concluded

## Sentence-level guidance

Prefer:

- one technical point per sentence when the material is dense
- explicit connectors such as "because", "therefore", "however", "in contrast", "specifically"
- short clarifying appositives when introducing a term
- concrete nouns over vague abstractions

Be careful with:

- long sentences containing several unmarked logical transitions
- pronouns with unclear referents
- unexplained shorthand from notes
- overloaded notation
- compressed bullets pasted into prose without restructuring

## What to avoid

- novelty claims without a comparison basis
- vague phrases like "very effective" without evidence
- causal claims from correlational observations
- notation introduced after use
- unsupported universals such as "always", "in general", "all"
- inflated framing that exceeds the evidence
- paragraph openings that assume concepts not yet defined
- lists of observations with no analytical thread
- prose that sounds polished but hides missing technical content

## Final drafting rule

The draft should be smoother than the notes, but never more certain than the notes justify.