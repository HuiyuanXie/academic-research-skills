---
name: paper-digest
description: Read and analyze AI research papers from a PDF or URL and produce a structured markdown digest grounded in the paper. Use when the user wants a paper summary, paper digest, benchmark or dataset breakdown, method breakdown, survey summary, position-paper analysis, experiment summary, or a structured reading note with faithful extraction of contributions, experiments, tables, and figures.
---

# Paper Digest

## Purpose

Read an AI research paper from a PDF or URL, identify the paper type, and produce a structured markdown digest grounded strictly in the paper.

## Workflow

1. Read the paper fully enough to identify its title, main contribution, paper type, structure, and evidence.
2. Classify the paper using [references/paper-types.md](references/paper-types.md).
3. Extract information using [references/extraction-rules.md](references/extraction-rules.md).
4. Build the digest using [references/output-schema.md](references/output-schema.md).
5. Preserve original contribution wording when the workflow asks for direct extraction.
6. Reproduce table contents in Markdown when they are readable from the source. If a figure cannot be reproduced faithfully as a table, describe it faithfully and specifically instead of inventing details.
7. Keep every summary, analysis, and interpretation strictly grounded in the paper.

## Output Rules

- Return Markdown only.
- Always include the common sections:
  - `Title`
  - `One-line summary`
  - `Paper type & keywords`
  - `Author-stated contributions`
- Add the appropriate paper-type-specific sections only after classifying the paper.
- Do not add personal opinions or outside evaluation unless the user explicitly asks for them.
- Do not invent missing statistics, dataset properties, model settings, citations, figure values, or claims.
- If a requested item is missing or unclear in the paper, say so explicitly.

## Input Handling

- Accept either:
  - a local PDF path
  - a paper URL
- When both PDF text and layout cues matter, prefer the paper itself over secondary metadata.
- If the input URL points to a metadata or abstract page, try to access the full paper text before producing a full digest.
- If only abstract-level or otherwise partial content is accessible, produce a limited digest and explicitly state which sections cannot be completed reliably.
- If the source is long or dense, extract the digest section by section rather than relying on a shallow skim.

## Paper-Type Routing

- For benchmark or dataset papers, emphasize dataset structure, construction, statistics, and experimental usage.
- For modelling papers, emphasize method logic, components, design choices, assumptions, and empirical results.
- For survey papers, emphasize organizational logic, section-wise takeaways, and influential cited work.
- For position papers, emphasize the core position, argument flow, alternative positions, and refutation structure.

## Fidelity Rules

- Preserve author-stated contributions as directly as possible when extracting them from the paper.
- Preserve original tables in Markdown when readable.
- Describe figures faithfully when direct tabular reconstruction is not realistic.
- Distinguish direct extraction from brief synthesis where needed, but keep both grounded in the paper text.
