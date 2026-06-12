# Output Schema

## Purpose

Use this schema to structure the digest after classifying the paper.

Return Markdown with clear headings and subheadings.

## Common Sections

Include these sections for all paper types:

### Title

- exact paper title

### One-line Summary

- one sentence capturing the paper's main contribution

### Paper Type & Keywords

- primary paper type
- relevant technical keywords

### Author-Stated Contributions

- direct extraction from the paper when possible

## Benchmark or Dataset Paper

If the paper is classified as `benchmark/dataset`, include:

### Dataset Name

### Dataset Highlights

- key novelties
- distinguishing properties

### Sub-tasks / Data Subsets

### Sample Examples

### Data Statistics

- examples
- classes
- splits
- scale
- other key statistics given in the paper

### Original Data Sources

### Construction Process

- synthetic, automatic, human-annotated, or mixed

### Experimental Design & Results Summary

- datasets or tasks used in experiments
- baselines or comparison systems
- evaluation metrics
- experimental setup
- headline quantitative results
- original results tables or figures, reproduced or described faithfully

### Analysis / Discussion

- the paper's own insights and discussion points

## Modelling Paper

If the paper is classified as `modelling`, include:

### Methodology One-line Summary

### Method Highlights

- novel aspects
- major design contributions

### Modules / Steps

- break the method into modules or sequential steps
- give a brief summary of each

### Decision Points & Assumptions

- important design choices
- assumptions
- constraints

### Experimental Design & Results Summary

- datasets or tasks used
- baselines or comparison systems
- evaluation metrics
- training or inference setup when central to the paper
- headline quantitative results
- original results tables or figures, reproduced or described faithfully

### Analysis / Discussion

- analysis
- ablations
- discussion

## Survey Paper

If the paper is classified as `survey`, include:

### Survey Logic & Structure

### Section-wise Summary

- summarize each major section

### Highly Influential References

For each highlighted reference, include:

- title
- one-line summary
- link, if available from the source

## Position Paper

If the paper is classified as `position`, include:

### Core Position

### Argumentation Flow

### Contrasting Positions

### Refutation

- explain why the authors reject or dismiss alternative positions

### Analysis

- strictly grounded in the paper's own content

## Completeness Rule

- If a requested section cannot be filled reliably from the paper, keep the heading and state briefly that the information is not clearly specified or not accessible from the available source.
- Do not omit the section silently when the schema expects it.

## Formatting Rules

- keep headings explicit
- use concise bullets when extraction is list-shaped
- preserve tables in Markdown when readable
- otherwise describe figures faithfully and specifically
- keep all summaries grounded in the paper
