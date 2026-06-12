import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import arxiv
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import yaml

SCRIPT_PATH = Path(__file__).resolve()


def find_repo_root() -> Path:
    for parent in SCRIPT_PATH.parents:
        if (parent / ".codex").exists() and (parent / "config").exists():
            return parent
    raise RuntimeError("Could not locate repository root from script path.")


REPO_ROOT = find_repo_root()
load_dotenv(REPO_ROOT / ".env")

REPORT_DIR = REPO_ROOT / "reports"
CONFIG_DIR = REPO_ROOT / "config"
STATE_DIR = REPO_ROOT / "state"
TOPICS_PATH = CONFIG_DIR / "topics.yaml"
EXPANDED_KEYWORDS_PATH = STATE_DIR / "expanded_keywords.json"
LAST_RUN_PATH = STATE_DIR / "last_run.json"
SEEN_PATH = STATE_DIR / "seen_papers.json"

for path in [CONFIG_DIR, STATE_DIR, REPORT_DIR]:
    path.mkdir(exist_ok=True)

client = OpenAI()
MODEL_NAME = "gpt-5.2"


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing config file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
    

def stable_hash(obj: Any) -> str:
    serialized = json.dumps(obj, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def load_last_run():
    if not LAST_RUN_PATH.exists():
        return "2026-01-01T00:00:00+00:00"
    with open(LAST_RUN_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["last_run"]


def save_last_run(timestamp):
    with open(LAST_RUN_PATH, "w", encoding="utf-8") as f:
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


def call_llm_text(prompt: str) -> str:
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )
    return response.output_text.strip()


def call_llm_json(prompt):
    text = call_llm_text(prompt)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "parse_error": True,
            "raw_output": text,
        }


def expand_keywords_for_topic(topic: dict[str, Any]) -> dict[str, Any]:
    prompt = f"""
You are helping build an arXiv paper watcher.

Given a research topic, expand the user's seed keywords and include criteria into high-recall arXiv search keywords.

Use BOTH:
1. seed_keywords: the user's initial search terms;
2. include: concepts that should count as relevant and should be reflected in the search keywords.

Rules:
- Return only valid JSON.
- Generate high-recall search keywords likely to appear in arXiv titles or abstracts.
- Prefer short phrases, not full sentences.
- Include synonyms, common variants, and adjacent terminology.
- Do not include Boolean operators such as AND/OR.
- Do not include overly broad standalone terms such as "AI", "NLP", "LLM", "machine learning", or "reasoning" unless qualified by the topic.
- Keep around 10-25 keywords.
- Preserve important domain-specific phrases from seed_keywords and include terms.
- Avoid keywords that are mainly described by the exclude list.

Return format:
{{
  "topic_id": "{topic["id"]}",
  "expanded_keywords": ["keyword 1", "keyword 2"]
}}

Topic ID:
{topic.get("id")}

Topic name:
{topic.get("name")}

Description:
{topic.get("description")}

Seed keywords:
{json.dumps(topic.get("seed_keywords"), ensure_ascii=False, indent=2)}

Include terms:
{json.dumps(topic.get("include", []), ensure_ascii=False, indent=2)}

Exclude terms:
{json.dumps(topic.get("exclude", []), ensure_ascii=False, indent=2)}
"""

    result = call_llm_json(prompt)
    if "expanded_keywords" not in result:
        return {
            "topic_id": topic["id"],
            "expanded_keywords": topic.get("seed_keywords", []), # Fallback: use seed_keywords
            "fallback_used": True,
            "raw_model_output": result,
        }

    return {
        "topic_id": topic["id"],
        "expanded_keywords": sorted(set(result["expanded_keywords"])),
        "fallback_used": False,
    }


def load_or_create_expanded_keywords(config: dict[str, Any]) -> dict[str, Any]:
    topics = config.get("topics", [])
    topics_hash = stable_hash(topics)
    if EXPANDED_KEYWORDS_PATH.exists():
        with open(EXPANDED_KEYWORDS_PATH, "r", encoding="utf-8") as f:
            cached = json.load(f)
        if cached.get("topics_hash") == topics_hash:
            return cached

    expanded_topics = []
    for topic in topics:
        expanded = expand_keywords_for_topic(topic)
        expanded_topics.append(expanded)

    expanded_config = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "topics_hash": topics_hash,
        "topic_snapshot": topics,
        "expanded_topics": expanded_topics,
    }

    with open(EXPANDED_KEYWORDS_PATH, "w", encoding="utf-8") as f:
        json.dump(expanded_config, f, indent=2, ensure_ascii=False)
    return expanded_config


def quote_arxiv_phrase(keyword: str) -> str:
    keyword = keyword.strip()
    if '"' in keyword:
        keyword = keyword.replace('"', "")
    if " " in keyword:
        return f'all:"{keyword}"'
    return f"all:{keyword}"


def build_arxiv_query(expanded_config: dict[str, Any], categories: list[str],)  -> str:
    all_keywords = []
    for topic in expanded_config["expanded_topics"]:
        all_keywords.extend(topic.get("expanded_keywords", []))
    unique_keywords = sorted(set(k.strip() for k in all_keywords if k.strip()))
    keyword_query = " OR ".join(quote_arxiv_phrase(k) for k in unique_keywords)
    category_query = " OR ".join(f"cat:{cat}" for cat in categories)
    return f"({keyword_query}) AND ({category_query})"


def relevance_filter_against_topics(title, abstract, topics: list[dict[str, Any]],) -> dict[str, Any]:
    topic_briefs = []
    for topic in topics:
        topic_briefs.append({
            "id": topic.get("id"),
            "name": topic.get("name"),
            "description": topic.get("description", ""),
            "include": topic.get("include", []),
            "exclude": topic.get("exclude", []),
        })
    
    prompt = f"""
You are filtering arXiv papers for a researcher's configurable paper watcher.

Determine whether this paper is genuinely relevant to at least one of the research topics.

Important rules:
- Treat each topic's "include" list as positive relevance criteria.
- Treat each topic's "exclude" list as negative relevance criteria.
- A paper may match multiple topics.
- A paper should be marked relevant if it substantially matches one or more include criteria.
- A paper should be marked not relevant if the match is only superficial.
- A paper should be marked not relevant if it mainly falls under a topic's exclude criteria.
- Use the abstract and title only; do not infer unsupported details.
- Return only valid JSON.

Return only valid JSON in this format:
{{
  "is_relevant": true,
  "matched_topic_ids": ["topic_id_1"],
  "matched_topic_names": ["Topic Name"],
  "relevance_score": 0.0,
  "reason": "brief explanation"
}}

Relevance score guidance:
- 0.90-1.00: directly about one or more include criteria.
- 0.70-0.89: clearly relevant, though not central to the topic.
- 0.50-0.69: partially relevant or borderline.
- below 0.50: not relevant.

Research topics:
{json.dumps(topic_briefs, ensure_ascii=False, indent=2)}

Paper title:
{title}

Paper abstract:
{abstract}
"""
    result = call_llm_json(prompt)
    if result.get("parse_error"):
        return {
            "is_relevant": False,
            "matched_topic_ids": [],
            "matched_topic_names": [],
            "relevance_score": 0.0,
            "reason": f"Could not parse relevance filter output: {result.get('raw_output', '')}",
        }

    return {
        "is_relevant": bool(result.get("is_relevant", False)),
        "matched_topic_ids": result.get("matched_topic_ids", []),
        "matched_topic_names": result.get("matched_topic_names", []),
        "relevance_score": result.get("relevance_score", 0.0),
        "reason": result.get("reason", ""),
    }


def summarize_paper(title, abstract, matched_topic_names: list[str],) -> str:
    prompt = f"""
You are a research assistant for Legal AI / Legal NLP.

Summarize the following paper in 3-5 concise sentences.
Focus on:
1. the problem/task,
2. the method,
3. main findings or results,
4. summary of contributions.

Matched topics:
{matched_topic_names}

Title:
{title}

Abstract:
{abstract}
"""
    return call_llm_text(prompt)


def fetch_since(query):
    search = arxiv.Search(
        query=query,
        max_results=30,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )
    arxiv_client = arxiv.Client()
    return arxiv_client.results(search)


def process_papers(
    config: dict[str, Any],
    expanded_config: dict[str, Any],
    last_run_iso: str,
    seen_papers: set[str],
) -> tuple[list[dict[str, Any]], set[str]]:
    last_run = datetime.fromisoformat(last_run_iso)
    topics = config.get("topics", [])
    categories = config.get(
        "default_categories",
        ["cs.CL", "cs.AI", "cs.IR", "cs.LG", "cs.CY", "stat.ML"],
    )

    query = build_arxiv_query(expanded_config, categories)

    rows = []
    newly_seen = set()
    for paper in fetch_since(query):
        arxiv_id = get_arxiv_id(paper)
        published = paper.published.replace(tzinfo=timezone.utc)
        if arxiv_id in seen_papers:
            continue
        if published <= last_run:
            continue

        title = paper.title.strip().replace("\n", " ")
        abstract = paper.summary.strip().replace("\n", " ")
        relevance = relevance_filter_against_topics(title, abstract, topics)
        newly_seen.add(arxiv_id)

        if not relevance["is_relevant"]:
            continue

        summary = summarize_paper(
            title=title,
            abstract=abstract,
            matched_topic_names=relevance["matched_topic_names"],
        )

        rows.append({
            "arxiv_id": arxiv_id,
            "published": published.isoformat(),
            "title": title,
            "authors": ", ".join(author.name for author in paper.authors),
            "link": paper.entry_id,
            "categories": ", ".join(paper.categories),
            "matched_topic_ids": "; ".join(relevance["matched_topic_ids"]),
            "matched_topic_names": "; ".join(relevance["matched_topic_names"]),
            "relevance_score": relevance["relevance_score"],
            "relevance_reason": relevance["reason"],
            "abstract": abstract,
            "codex_summary": summary,
        })

    return rows, newly_seen


def save_report(rows, start_time, end_time):
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_path = REPORT_DIR / f"arxiv_digest_{date}.csv"
    md_path = REPORT_DIR / f"arxiv_digest_{date}.md"

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# arXiv Research Paper Digest\n\n")
        f.write(f"**Time Window:** {start_time} to {end_time}\n\n")
        f.write(f"**Relevant papers found:** {len(rows)}\n\n")

        grouped = {}

        for row in rows:
            topic_names = row["matched_topic_names"] or "Uncategorized"
            grouped.setdefault(topic_names, []).append(row)

        for topic_name, papers in grouped.items():
            f.write(f"# Topic: {topic_name}\n\n")

            for i, row in enumerate(papers, 1):
                f.write(f"## {i}. {row['title']}\n\n")
                f.write(f"**Authors:** {row['authors']}\n\n")
                f.write(f"**Published:** {row['published']}\n\n")
                f.write(f"**arXiv ID:** {row['arxiv_id']}\n\n")
                f.write(f"**Link:** {row['link']}\n\n")
                f.write(f"**Categories:** {row['categories']}\n\n")
                f.write(f"**Matched topics:** {row['matched_topic_names']}\n\n")
                f.write(f"**Relevance score:** {row['relevance_score']}\n\n")
                f.write(f"**Relevance reason:** {row['relevance_reason']}\n\n")
                f.write(f"**Abstract:** {row['abstract']}\n\n")
                f.write(f"**Codex summary:** {row['codex_summary']}\n\n")
                f.write("---\n\n")

    return csv_path, md_path


def main():
    config = load_yaml(TOPICS_PATH)
    expanded_config = load_or_create_expanded_keywords(config)
    last_run = load_last_run()
    seen_papers = load_seen_papers()
    now = datetime.now(timezone.utc).isoformat()
    rows, newly_seen = process_papers(
        config=config,
        expanded_config=expanded_config,
        last_run_iso=last_run,
        seen_papers=seen_papers,
    )

    csv_path, md_path = save_report(rows, last_run, now)
    seen_papers.update(newly_seen)
    save_seen_papers(seen_papers)
    save_last_run(now)
    print("Done.")
    print(f"Relevant papers found: {len(rows)}")
    print(f"New papers processed: {len(newly_seen)}")
    print(f"Total tracked papers: {len(seen_papers)}")
    print(f"CSV report: {csv_path}")
    print(f"Markdown report: {md_path}")
    print(f"Expanded keywords: {EXPANDED_KEYWORDS_PATH}")

if __name__ == "__main__":
    main()
