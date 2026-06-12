# Paper Types

## Purpose

Use this reference to classify the paper before writing the digest.

Choose the dominant paper type based on the paper's central contribution, not on isolated sections.

## 1. Benchmark or Dataset Paper

Classify the paper as `benchmark/dataset` when its main contribution is one or more of the following:

- introducing a new dataset
- introducing a new benchmark or evaluation suite
- curating, annotating, or constructing data as the central contribution
- defining subtasks, splits, or evaluation settings around a dataset or benchmark

Common signals:

- the title foregrounds a dataset or benchmark name
- large parts of the paper focus on data collection, annotation, or statistics
- experiments are organized around benchmarking models on the new resource

Even if the paper includes baseline models, keep this label if the dataset or benchmark is the main contribution.

## 2. Modelling Paper

Classify the paper as `modelling` when its main contribution is one or more of the following:

- a new model, architecture, training method, inference method, or algorithm
- a new module or design pattern within a larger system
- a methodological improvement whose main evidence is empirical or theoretical performance

Common signals:

- the title foregrounds a model or method
- the paper contains a method section organized around components or steps
- the experiments are mainly used to validate a proposed method

If the paper introduces both a dataset and a method, choose `modelling` only if the method is clearly the primary contribution.

## 3. Survey Paper

Classify the paper as `survey` when its main contribution is synthesis rather than a new model or dataset.

Common signals:

- the paper organizes prior work into themes, taxonomies, or historical developments
- the paper compares research lines rather than proposing a new system
- the value of the paper lies in coverage, structure, critique, or synthesis

The digest should focus on how the survey is organized and what conclusions it draws across sections.

## 4. Position Paper

Classify the paper as `position` when its central goal is to argue for a viewpoint, framework, agenda, or normative stance.

Common signals:

- the paper argues what the field should do, avoid, redefine, or prioritize
- the contribution is a position, thesis, or conceptual framing rather than a new system
- the paper discusses alternatives and argues against them

The digest should emphasize argument structure and refutation, not present the paper as an empirical result paper.

## Classification Rules

- Pick one primary type for the digest.
- If the paper is mixed, choose the type that best matches the main contribution claimed by the authors.
- Mention notable secondary characteristics only when useful, but keep the output schema anchored to the primary type.
- If classification is uncertain, state the uncertainty briefly and choose the narrowest defensible label.
