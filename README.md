# Academic Research Skills

A small Codex-ready repository of academic research skills.

At the moment, the repo contains three local Codex skills:

- `arxiv-paper-watcher-digest`: monitors arXiv for configurable research topics and generates Markdown/CSV digests
- `notes-to-paper-section`: reads large research notes, critiques their technical and logical quality, and drafts an ACL-style paper section
- `paper-digest`: reads AI papers from a PDF or URL and produces structured Markdown digests tailored to benchmark, modelling, survey, or position papers

The repo is meant to be practical rather than framework-heavy: each skill lives under `.codex/skills/`, and supporting scripts or configuration live alongside it in the repository.

## Skills Included

### 1. arXiv Paper Watcher and Digest

Skill file:

```text
.codex/skills/arxiv-paper-watcher-digest/SKILL.md
```

Supporting script:

```text
scripts/arxiv_paper_watcher_digest.py
```

What it does:

- reads research topics from `config/topics.yaml`
- expands seed keywords with an OpenAI-compatible model
- queries arXiv for newly submitted papers
- filters papers for substantive relevance against configured topics
- summarizes relevant papers
- writes Markdown and CSV reports under `reports/`
- tracks state under `state/`

Typical Codex prompt:

```text
Run the arXiv Watcher and Digest skill.
```

### 2. Notes to Paper Section

Skill files:

```text
.codex/skills/notes-to-paper-section/SKILL.md
.codex/skills/notes-to-paper-section/references/acl-style.md
.codex/skills/notes-to-paper-section/references/critique-checklist.md
```

What it does:

- reads large research notes, including multilingual notes
- builds an internal map of claims, assumptions, evidence, and open gaps
- critiques technical correctness and logical soundness
- identifies mistakes, unsupported claims, and missing information
- suggests improvements before drafting
- writes an ACL-style academic paper section grounded in the notes

Typical Codex prompt:

```text
Use the notes-to-paper-section skill on /absolute/path/to/notes.md. First critique the notes, then draft an ACL-style Method section.
```

### 3. Paper Digest

Skill files:

```text
.codex/skills/paper-digest/SKILL.md
.codex/skills/paper-digest/references/paper-types.md
.codex/skills/paper-digest/references/extraction-rules.md
.codex/skills/paper-digest/references/output-schema.md
```

What it does:

- reads AI papers from either a local PDF path or a paper URL
- identifies the paper type before drafting the digest
- produces structured Markdown digests grounded in the paper text
- adapts output for benchmark/dataset, modelling, survey, and position papers
- extracts author-stated contributions directly when possible
- reproduces readable tables in Markdown and otherwise describes figures faithfully

Typical Codex prompt:

```text
Use the paper-digest skill on /absolute/path/to/paper.pdf and produce a structured digest.
```

## Repository Layout

```text
.
├── .codex/
│   └── skills/
│       ├── arxiv-paper-watcher-digest/
│       │   └── SKILL.md
│       ├── notes-to-paper-section/
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── acl-style.md
│       │       └── critique-checklist.md
│       └── paper-digest/
│           ├── SKILL.md
│           ├── agents/
│           │   └── openai.yaml
│           └── references/
│               ├── extraction-rules.md
│               ├── output-schema.md
│               └── paper-types.md
├── config/
│   └── topics.yaml
├── reports/
├── scripts/
│   └── arxiv_paper_watcher_digest.py
├── state/
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

For the repository as it exists today:

- Python 3.11 or newer recommended
- an OpenAI API key available through `.env`
- network access to:
  - arXiv API
  - OpenAI Responses API

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Create a local `.env` file:

```bash
OPENAI_API_KEY=your_api_key_here
```

`.env` is ignored by Git and should not be committed.

## arXiv Watcher Setup

The arXiv watcher is the only current skill in this repo that requires a Python runtime and external APIs.

Research interests live in `config/topics.yaml`.

Example topic:

```yaml
profile_name: "Research Paper Watcher"

default_categories:
  - cs.CL
  - cs.AI
  - cs.IR
  - cs.LG
  - cs.CY
  - stat.ML

topics:
  - id: legal_ai
    name: "Legal AI and Legal NLP"
    description: >
      Papers about applying AI, NLP, LLMs, retrieval, reasoning, or agents to legal tasks.
    seed_keywords:
      - legal AI
      - legal NLP
      - AI and law
      - computational law
      - legal reasoning
      - legal datasets and benchmarks
    include:
      - legal reasoning
      - legal datasets or benchmarks
      - legal information extraction
      - precedent analysis
      - regulation, compliance, or governance using AI
      - LLMs applied to legal tasks
    exclude:
      - physical law
      - scientific laws
      - generic AI papers without legal application
```

Each topic supports:

- `id`: stable machine-readable identifier
- `name`: display name used in reports
- `description`: short description of the topic
- `seed_keywords`: initial search terms
- `include`: concepts that should count as relevant
- `exclude`: false-positive patterns or adjacent areas to filter out

`default_categories` controls which arXiv categories are searched.

## Running the arXiv Watcher Script

Run:

```bash
python3 scripts/arxiv_paper_watcher_digest.py
```

Successful output looks like:

```text
Done.
Relevant papers found: 8
New papers processed: 10
Total tracked papers: 10
CSV report: reports/arxiv_digest_YYYY-MM-DD_HH-MM-SS.csv
Markdown report: reports/arxiv_digest_YYYY-MM-DD_HH-MM-SS.md
Expanded keywords: state/expanded_keywords.json
```

The script updates `state/last_run.json` only after the workflow completes.

## State and Generated Files

The arXiv watcher creates and updates:

- `state/last_run.json`: timestamp of the last successful run
- `state/seen_papers.json`: arXiv IDs already processed
- `state/expanded_keywords.json`: cached model-expanded keywords for the current topic config
- `reports/*.md`: human-readable digest reports
- `reports/*.csv`: tabular report exports

If `config/topics.yaml` changes, the topic hash changes and expanded keywords are regenerated.

For a fresh run from scratch, remove or edit the files under `state/`. Be careful: deleting state may cause old papers to be processed again.

## Notes-to-Paper Workflow

The `notes-to-paper-section` skill is prompt-and-reference driven. It does not currently depend on a dedicated Python script in this repo.

Its workflow is:

1. read the notes fully
2. build an internal map of claims, assumptions, evidence, definitions, and open gaps
3. critique technical correctness and logical soundness
4. report mistakes, ambiguities, and missing information
5. draft an ACL-style section using the bundled references

The main skill file explicitly routes Codex to:

- `references/critique-checklist.md` before critique
- `references/acl-style.md` before drafting

This separation keeps the critique pass and the writing pass distinct, which is important for note-to-paper conversion.

## Paper-Digest Workflow

The `paper-digest` skill is also prompt-and-reference driven. It is designed for paper reading rather than note rewriting.

Its workflow is:

1. read the paper from a PDF path or URL
2. identify the paper title, structure, main contribution, and evidence
3. classify the paper as benchmark/dataset, modelling, survey, or position
4. extract paper-grounded content using the bundled extraction rules
5. produce a structured Markdown digest using the paper-type-specific schema

The main skill file explicitly routes Codex to:

- `references/paper-types.md` for classification
- `references/extraction-rules.md` for grounded extraction
- `references/output-schema.md` for final digest structure

This keeps paper-type routing, extraction behavior, and output formatting separate and easier to maintain.

## Model Usage

The arXiv watcher currently uses:

```python
MODEL_NAME = "gpt-5.2"
client = OpenAI()
```

It uses the model for:

1. keyword expansion
2. topic-aware relevance filtering
3. paper summarization

To use a different OpenAI-compatible endpoint or model, update the OpenAI client initialization and `MODEL_NAME` in scripts/arxiv_paper_watcher_digest.py.

The `notes-to-paper-section` and `paper-digest` skills are prompt-and-reference based. They do not currently rely on a dedicated Python runtime in this repo, but they may still depend on Codex being able to read local files or access a paper URL when invoked.
