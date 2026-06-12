# Extraction Rules

## Purpose

Use these rules when extracting information from the paper.

The goal is faithful, paper-grounded extraction rather than generic summarization.

## Grounding Rules

- Base all content on the paper itself.
- Prefer the abstract, introduction, method, experiments, discussion, appendix, tables, and figure captions over guesswork.
- Do not invent missing values, claims, settings, or interpretations.
- If a requested item is not clearly present, say `Not clearly specified in the paper` or equivalent.

## Title

- Use the exact paper title as written.

## One-line Summary

- Write one sentence capturing the main contribution.
- Keep it grounded in the paper's central claim.
- Do not inflate the claim beyond what the paper supports.

## Keywords

- Use concise technical keywords based on the paper's actual content.
- Prefer task names, method families, dataset names, benchmark names, domains, or problem settings.

## Author-Stated Contributions

- If the paper gives an explicit contribution list, extract it directly.
- If the paper states contributions only in prose, quote or closely preserve the most direct contribution-claim sentences and label them as direct contribution statements from the introduction.
- If no clear author-stated contribution passage exists, say `No explicit contribution list found in the paper` and provide the closest direct claim passage separately.
- Do not synthesize a polished contribution list and present it as direct author wording.

## Tables

- Reproduce original table contents in Markdown when readable from the source.
- Keep row labels, column labels, and key values.
- If the table is too large, reproduce the most relevant part and say that the paper contains additional rows or columns.
- Do not silently normalize or alter values.

## Figures

- If a figure cannot be faithfully converted into Markdown structure, describe it specifically.
- Mention what the axes, comparison groups, or trends show when they are legible.
- Do not fabricate numerical values that are not readable.

## Experimental Design

When summarizing experiments, extract:

- datasets or tasks used
- model or system setup if given
- baselines or comparators
- evaluation metrics
- ablations or analyses if present

Do not infer experiment details that are only typical in the field but absent from the paper.

## Sample Examples

- Include representative examples only if the paper provides them or describes them concretely enough.
- Preserve the paper's framing of the examples.

## Construction Process

For dataset or benchmark papers, identify whether construction is:

- fully synthetic or automatic
- fully human-annotated
- a mixed pipeline

If the process is mixed, state the roles of automation and human annotation as clearly as the paper allows.

## Influential References in Surveys

- Extract papers that the survey itself treats as classic, foundational, highly cited, or central.
- Prefer references discussed repeatedly or used to define major sections or paradigms.
- Include links only when the paper explicitly provides them or when they are clearly available in the source material being read.

## Analysis and Discussion

- Summarize the paper's own analysis, discussion, and interpretation.
- Do not add your own critique unless the user explicitly asks for it.
- Keep the distinction between paper content and outside judgment clear.
