# Critique Checklist

## Purpose

Use this checklist before drafting.

The goal is to identify technical errors, logical gaps, unsupported claims, ambiguous wording, and missing information in the notes before converting them into polished academic prose.

This checklist is for critique-first drafting. Do not move directly from notes to publication-style prose without using it.

## Step 1: Understand the notes first

Before judging correctness, build a working map of the notes.

Identify:

- the main claim or thesis
- the supporting claims
- the problem being addressed
- the method, mechanism, or line of reasoning
- the evidence available in the notes
- the assumptions that the notes appear to rely on
- the unresolved ambiguities
- the missing pieces that prevent confident drafting

If the notes are fragmented, infer the likely structure conservatively. Do not invent a stronger argument than the notes support.

## Step 2: Separate content types

Classify each important statement in the notes as one of the following:

- background fact
- definition
- empirical claim
- theoretical claim
- interpretation
- speculation
- future direction
- writing instruction or reminder

This prevents the draft from accidentally presenting tentative thoughts as established results.

## Step 3: Check claims

For each major claim, ask:

- What exactly is being claimed?
- What evidence in the notes supports it?
- Is the claim stronger than the evidence?
- Does the wording imply causality, generality, novelty, or robustness that is not justified?
- Is the claim actually central, or is it just a side observation in the notes?
- Would a skeptical reviewer ask for proof, data, citation, or qualification?

Flag claims that are:

- too broad
- underspecified
- unsupported
- rhetorically inflated
- dependent on hidden assumptions

## Step 4: Check logic

Ask:

- Are there missing intermediate reasoning steps?
- Are definitions, assumptions, or scope conditions missing?
- Do the conclusions actually follow from the premises?
- Are there contradictions across different parts of the notes?
- Is the argument mixing observation, explanation, and conclusion without marking the transitions?
- Is there a leap from correlation to causation?
- Is there a leap from a single case to a general claim?

When a reasoning chain is incomplete, identify the exact missing link.

## Step 5: Check technical soundness

Ask:

- Are methods described accurately?
- Are metrics, objectives, losses, or algorithms used correctly?
- Are formal terms used in the right sense?
- Is notation internally consistent?
- Are equations, proof ideas, or derivations missing assumptions?
- Are there likely misunderstandings or oversimplifications of prior work?
- Are comparisons technically fair?

Look for common technical failures such as:

- confusing task formulation with evaluation metric
- describing a heuristic as if it were a guarantee
- claiming theoretical implications from empirical observations alone
- using terms like "bias", "robustness", "generalization", or "interpretability" loosely
- attributing novelty where the notes only describe implementation detail

## Step 6: Check prior-work reasoning

Ask:

- Does the note attribute a capability, limitation, or novelty claim to prior work without enough support?
- Is the comparison to prior work dimension-specific, or just rhetorical?
- Does the note clearly state what differs from prior work?
- Is a citation needed for a background statement, standard method, or historical claim?
- Is a "first" or "novel" claim actually supported by the notes?

Be especially cautious when the notes compare against unnamed "existing methods" or "previous work" without specifying the basis of comparison.

## Step 7: Check empirical adequacy

If the notes concern experiments or evaluation, ask:

- Is the dataset or task clearly identified?
- Is the evaluation setting defined?
- Are baselines or comparators specified?
- Is the comparison fair?
- Are important implementation details missing?
- Are error bars, variance, or uncertainty relevant but absent?
- Is there enough information to support the interpretation of the results?
- Are failure cases or limitations missing?

Common missing pieces:

- task definition
- data source
- train/dev/test split assumptions
- baseline choice
- ablation or control
- evaluation metric definition
- significance or robustness caveat

## Step 8: Check theoretical adequacy

If the notes contain proofs, formal claims, or derivations, ask:

- Are all variables and objects defined?
- Are the assumptions explicit?
- Is any theorem stated more strongly than the derivation supports?
- Are proof sketches missing crucial cases or constraints?
- Are there hidden regularity conditions, independence assumptions, or optimization assumptions?
- Is an empirical intuition being presented as a formal result?

If the notes only contain an intuition, the draft should present it as intuition, not as theorem-like fact.

## Step 9: Check multilingual and terminology risks

When the notes are not entirely in English, or mix languages, ask:

- Is any technical term being translated too loosely?
- Does the original wording carry a narrower or broader meaning than the English paraphrase?
- Are there shorthand phrases that depend on local lab context?
- Are there citation names, task names, or formal concepts that should remain in the original or standardized form?
- Is a phrase ambiguous enough that the draft should preserve it cautiously or ask for clarification?

Preserve technical meaning over stylistic fluency.

Do not over-normalize multilingual notes if doing so changes the scientific content.

## Step 10: Check paper readiness

Ask:

- Is there enough support to write this as polished paper prose?
- Which parts can be stated confidently?
- Which parts must be softened?
- Which parts should be marked as assumptions, hypotheses, or open issues?
- Which missing pieces are important enough to surface to the user before drafting?

A strong draft may still be possible even when the notes are incomplete, but only if the uncertainty is handled honestly.

## Step 11: Decide the repair strategy

For each problem found, choose the most appropriate repair:

- clarify a vague statement
- add a missing definition
- soften an overstrong claim
- add a limitation or scope condition
- restructure the argument
- request missing evidence or detail from the user
- preserve the issue explicitly as an unresolved uncertainty

Do not repair every issue by rewriting it more elegantly. Some issues need to be surfaced, not hidden.

## Step 12: Drafting rule

When the notes are uncertain or incomplete:

- flag the uncertainty explicitly
- prefer a narrower defensible claim
- avoid silently inventing missing support
- separate source-grounded content from inferred content

The final draft should be cleaner than the notes, but the critique should remain visible in the workflow.