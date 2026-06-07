from asyncio import tasks
import json
from datetime import datetime, timezone
from pathlib import Path

import arxiv
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

STATE_PATH = Path("state/last_run.json")
SEEN_PATH = Path("state/seen_papers.json")
REPORT_DIR = Path("reports")

REPORT_DIR.mkdir(exist_ok=True)
STATE_PATH.parent.mkdir(exist_ok=True)

# client = OpenAI()
client = OpenAI(
    base_url="https://yeysai.com/v1"
)
MODEL_NAME = "gpt-5.2"

KEYWORDS = [
    '"legal AI"',
    '"legal NLP"',
    '"AI and law"',
    '"computational law"',
    '"legal reasoning"',
    '"reinforcement learning" AND "legal"',
    '"legal information extraction"',
    '"legal text classification"',
    '"large language model" AND "legal"',
    '"LLM" AND "legal"',
    '"law" AND "language model"',
    '"legal agents"',
    '"legal" AND "dataset"',
    '"legal" AND "benchmark"',
    '"statutory reasoning"',
    '"court judgment"',
    '"case law"',
]

CATEGORIES = ["cs.CL", "cs.AI", "cs.IR", "cs.LG", "cs.CY", "cs.HC", "stat.ML"]


def load_last_run():
    if not STATE_PATH.exists():
        return "2026-01-01T00:00:00+00:00"

    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["last_run"]


def save_last_run(timestamp):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump({"last_run": timestamp}, f, indent=2)


def load_seen_papers():
    if not SEEN_PATH.exists():
        return set()

    with open(SEEN_PATH, "r", encoding="utf-8") as f:
        return set(json.load(f))


def save_seen_papers(seen_papers):
    with open(SEEN_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(seen_papers), f, indent=2, ensure_ascii=False)


def get_arxiv_id(paper):
    return paper.entry_id.split("/")[-1]


def build_query():
    keyword_part = " OR ".join(f"all:{kw}" for kw in KEYWORDS)
    category_part = " OR ".join(f"cat:{cat}" for cat in CATEGORIES)
    return f"({keyword_part}) AND ({category_part})"


def call_llm_json(prompt):
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    text = response.output_text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "is_relevant": False,
            "field": "parse_error",
            "reason": f"Could not parse model output: {text}",
        }


def relevance_filter(title, abstract):
    prompt = f"""
You are a research assistant specializing in Legal AI, Legal NLP, and AI & Law.

Determine whether the following arXiv paper is genuinely relevant to Legal AI, Legal NLP, or AI & Law.

Relevant papers include work on:
- legal reasoning
- reinforcement learning for legal tasks
- legal datasets or benchmarks
- legal information extraction
- legal agents or multi-agent systems for legal tasks
- court debate simulation
- legal argument mining
- similar case retrieval or precedent analysis
- issue analysis or dispute focus analysis
- computational law
- regulation, compliance, or governance using AI
- LLMs applied to legal tasks

Exclude papers where:
- "law" only means physical/scientific law
- the legal connection is superficial
- the paper is about general AI with no legal application

Return only valid JSON in this format:
{{
  "is_relevant": true,
  "field": "one of: legal reasoning, reinforcement learning, datasets/benchmarks, information extraction, document retrieval, judgment prediction, question answering, argument mining, case analysis, issue analysis, computational law, regulation/compliance/governance, LLM applications, or other specific legal AI area",
  "reason": "brief reason"
}}

Title:
{title}

Abstract:
{abstract}
"""

    return call_llm_json(prompt)


def summarize_paper(title, abstract):
    prompt = f"""
You are a research assistant for Legal AI / Legal NLP.

Summarize the following paper in 3-5 concise sentences.
Focus on:
1. the problem/task,
2. the method,
3. main findings or results,
4. summary of contributions.

Title:
{title}

Abstract:
{abstract}
"""

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    return response.output_text.strip()


def fetch_since(last_run_iso, seen_papers):
    last_run = datetime.fromisoformat(last_run_iso)

    search = arxiv.Search(
        query=build_query(),
        max_results=10,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    arxiv_client = arxiv.Client()
    rows = []
    newly_seen = set()

    for paper in arxiv_client.results(search):
        arxiv_id = get_arxiv_id(paper)
        published = paper.published.replace(tzinfo=timezone.utc)

        if arxiv_id in seen_papers:
            continue

        if published <= last_run:
            continue

        title = paper.title.strip().replace("\n", " ")
        abstract = paper.summary.strip().replace("\n", " ")

        relevance = relevance_filter(title, abstract)

        # Mark as seen even if not relevant, so it will not be checked again.
        newly_seen.add(arxiv_id)

        if not relevance.get("is_relevant", False):
            continue

        summary = summarize_paper(title, abstract)

        rows.append({
            "arxiv_id": arxiv_id,
            "published": published.isoformat(),
            "title": title,
            "authors": ", ".join(a.name for a in paper.authors),
            "link": paper.entry_id,
            "pdf": paper.pdf_url,
            "abstract": abstract,
            "relevance_field": relevance.get("field", ""),
            "relevance_reason": relevance.get("reason", ""),
            "codex_summary": summary,
            "categories": ", ".join(paper.categories),
        })

    return rows, newly_seen


def save_report(rows, start_time, end_time):
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_path = REPORT_DIR / f"arxiv_legal_ai_{date}.csv"
    md_path = REPORT_DIR / f"arxiv_legal_ai_{date}.md"

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# arXiv Legal AI / Legal NLP Digest\n\n")
        f.write(f"**Window:** {start_time} to {end_time}\n\n")
        f.write(f"**Relevant papers found:** {len(rows)}\n\n")

        for i, row in enumerate(rows, 1):
            f.write(f"## {i}. {row['title']}\n\n")
            f.write(f"**arXiv ID:** {row['arxiv_id']}\n\n")
            f.write(f"**Authors:** {row['authors']}\n\n")
            f.write(f"**Published:** {row['published']}\n\n")
            f.write(f"**Link:** {row['link']}\n\n")
            f.write(f"**PDF:** {row['pdf']}\n\n")
            f.write(f"**Categories:** {row['categories']}\n\n")
            f.write(f"**Relevance field:** {row['relevance_field']}\n\n")
            f.write(f"**Relevance reason:** {row['relevance_reason']}\n\n")
            f.write(f"**Abstract:** {row['abstract']}\n\n")
            f.write(f"**Codex summary:** {row['codex_summary']}\n\n")
            f.write("---\n\n")

    print(f"Saved CSV: {csv_path}")
    print(f"Saved Markdown: {md_path}")


def main():
    last_run = load_last_run()
    seen_papers = load_seen_papers()
    now = datetime.now(timezone.utc).isoformat()

    rows, newly_seen = fetch_since(last_run, seen_papers)

    save_report(rows, last_run, now)

    seen_papers.update(newly_seen)
    save_seen_papers(seen_papers)

    save_last_run(now)

    print(f"New relevant papers: {len(rows)}")
    print(f"Newly seen papers: {len(newly_seen)}")
    print(f"Total seen papers: {len(seen_papers)}")


if __name__ == "__main__":
    main()