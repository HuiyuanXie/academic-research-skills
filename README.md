# Academic Research Skills

A small Codex-ready research automation repo for monitoring arXiv, filtering papers against configurable research interests, and generating Markdown/CSV digests with model-written relevance judgments and summaries.

The current workflow is an **arXiv Research Paper Watcher**. It was originally focused on Legal AI / Legal NLP, but the latest version is topic-configurable through `config/topics.yaml`.

## What It Does

- Reads research topics, seed keywords, inclusion criteria, exclusion criteria, and arXiv categories from `config/topics.yaml`.
- Uses an OpenAI-compatible model to expand seed keywords into higher-recall arXiv search terms.
- Caches expanded keywords in `state/expanded_keywords.json` and regenerates them when the topic config changes.
- Queries arXiv for newly submitted papers after the last successful run.
- Filters papers for substantive relevance against the configured topics.
- Summarizes relevant papers in 3-5 concise sentences.
- Saves digest reports as both Markdown and CSV under `reports/`.
- Tracks processed papers in `state/seen_papers.json` to avoid reprocessing.

## Repository Layout

```text
.
├── .codex/
│   └── skills/
│       └── arxiv_paper_watcher_digest/
│           └── SKILL.md
├── config/
│   └── topics.yaml
├── reports/
│   └── arxiv_digest_*.md / *.csv
├── scripts/
│   └── arxiv_paper_watcher_digest.py
├── state/
│   ├── expanded_keywords.json
│   ├── last_run.json
│   └── seen_papers.json
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.11 or newer recommended
- An OpenAI API key available through `.env`
- Network access to:
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

## Configuration

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

- `id`: stable machine-readable identifier.
- `name`: display name used in reports.
- `description`: short description of the topic.
- `seed_keywords`: initial search terms.
- `include`: concepts that should count as relevant.
- `exclude`: false-positive patterns or adjacent areas to filter out.

`default_categories` controls which arXiv categories are searched.

## Running the Digest

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

## Codex Skill

This repository includes a local Codex skill at:

```text
.codex/skills/arxiv-paper-watcher-digest/SKILL.md
```

The skill describes the intended on-demand workflow:

1. Install dependencies if missing.
2. Confirm `OPENAI_API_KEY` is configured without printing it.
3. Read the last-run state.
4. Query arXiv.
5. Filter, summarize, and save a digest.
6. Update state after successful completion.

In Codex, you can ask:

```text
Run the arXiv Watcher and Digest skill.
```

## State and Generated Files

The script creates and updates:

- `state/last_run.json`: timestamp of the last successful run.
- `state/seen_papers.json`: arXiv IDs already processed.
- `state/expanded_keywords.json`: cached model-expanded keywords for the current topic config.
- `reports/*.md`: human-readable digest reports.
- `reports/*.csv`: tabular report exports.

If `config/topics.yaml` changes, the topic hash changes and expanded keywords are regenerated.

For a fresh run from scratch, remove or edit the files under `state/`. Be careful: deleting state may cause old papers to be processed again.

## Output Format

Markdown reports are grouped by matched topic and include:

- paper title
- authors
- publication timestamp
- arXiv ID and link
- arXiv categories
- matched topic names
- relevance score
- relevance reason
- abstract
- model-generated summary

CSV reports contain the same structured metadata for spreadsheet analysis.

## Model Behavior

The script currently uses:

```python
MODEL_NAME = "gpt-5.2"
client = OpenAI()
```

The model is used for three stages:

1. Expanding topic keywords.
2. Filtering papers against topic criteria.
3. Summarizing relevant papers.

To use a different OpenAI-compatible endpoint or model, update the OpenAI client initialization and `MODEL_NAME` in `scripts/arxiv_paper_watcher_digest.py`.
