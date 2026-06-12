---
name: notes-to-paper-section
description: Read large research notes, including multilingual notes, analyze their logic and technical content, critique mistakes or gaps, and draft an ACL-style academic paper section. Use when the user wants to turn notes into a paper section, critique research notes before writing, convert multilingual notes into academic prose, draft an ACL-style method or related-work section, or identify missing information and logical problems before paper writing.
---

# Notes to Paper Section

## Purpose

Read raw research notes, understand the technical content, identify logical or technical problems, and draft a polished ACL-style section.

## Workflow

1. Read the notes fully before drafting.
2. Build an internal map of claims, assumptions, evidence, definitions, and open gaps.
3. Before writing, read [references/critique-checklist.md](references/critique-checklist.md) and use it to test technical correctness and logical soundness.
4. Report technical concerns, logical gaps, and missing information to the user.
5. When drafting the final prose, read [references/acl-style.md](references/acl-style.md) and follow its guidance for tone, paragraph structure, and claim discipline.
6. Distinguish clearly between content grounded in the notes and content inferred for readability.
7. Never invent results, citations, datasets, or theorem conditions not supported by the notes.

## Output format

Return:
1. Understanding of the notes
2. Technical and logical critique
3. Missing information
4. Suggested improvements
5. ACL-style draft section
6. Assumptions and uncertainties
