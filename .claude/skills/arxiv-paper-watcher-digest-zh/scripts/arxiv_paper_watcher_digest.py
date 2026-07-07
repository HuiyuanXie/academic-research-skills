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
        if (parent / ".claude").exists() and (parent / "config").exists():
            return parent
    raise RuntimeError("无法从脚本路径定位仓库根目录。")


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
        raise FileNotFoundError(f"缺少配置文件：{path}")
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
你正在帮助构建一个 arXiv 论文监控器。

给定一个研究主题，将用户的种子关键词和包含条件扩展为高召回率的 arXiv 搜索关键词。

请同时使用：
1. seed_keywords：用户的初始搜索词；
2. include：应被视为相关并应在搜索关键词中体现的概念。

规则：
- 仅返回有效的 JSON。
- 生成可能出现在 arXiv 标题或摘要中的高召回率搜索关键词。
- 使用短短语，而非完整句子。
- 包含同义词、常见变体和相邻术语。
- 不要包含 AND/OR 等布尔运算符。
- 不要包含过于宽泛的单独术语，如 "AI"、"NLP"、"LLM"、"machine learning" 或 "reasoning"，除非由主题限定。
- 保持大约 10-25 个关键词。
- 保留 seed_keywords 和 include 术语中的重要领域短语。
- 避免使用主要由 exclude 列表描述的关键词。

返回格式：
{{
  "topic_id": "{topic["id"]}",
  "expanded_keywords": ["关键词 1", "关键词 2"]
}}

主题 ID：
{topic.get("id")}

主题名称：
{topic.get("name")}

描述：
{topic.get("description")}

种子关键词：
{json.dumps(topic.get("seed_keywords"), ensure_ascii=False, indent=2)}

包含术语：
{json.dumps(topic.get("include", []), ensure_ascii=False, indent=2)}

排除术语：
{json.dumps(topic.get("exclude", []), ensure_ascii=False, indent=2)}
"""

    result = call_llm_json(prompt)
    if "expanded_keywords" not in result:
        return {
            "topic_id": topic["id"],
            "expanded_keywords": topic.get("seed_keywords", []),  # 回退：使用种子关键词
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
你正在为一个可配置的论文监控器筛选 arXiv 论文。

判断这篇论文是否真正与至少一个研究主题相关。

重要规则：
- 将每个主题的 "include" 列表视为正相关标准。
- 将每个主题的 "exclude" 列表视为负相关标准。
- 一篇论文可以匹配多个主题。
- 如果论文实质性匹配一个或多个 include 标准，则应标记为相关。
- 如果匹配只是表面的，则应标记为不相关。
- 如果论文主要属于某个主题的 exclude 标准，则应标记为不相关。
- 仅使用摘要和标题；不要推断没有依据的细节。
- 仅返回有效的 JSON。

仅按以下格式返回有效的 JSON：
{{
  "is_relevant": true,
  "matched_topic_ids": ["topic_id_1"],
  "matched_topic_names": ["主题名称"],
  "relevance_score": 0.0,
  "reason": "简要解释"
}}

相关度分数指引：
- 0.90-1.00：直接涉及一个或多个 include 标准。
- 0.70-0.89：明显相关，但非主题核心。
- 0.50-0.69：部分相关或边界情况。
- 低于 0.50：不相关。

研究主题：
{json.dumps(topic_briefs, ensure_ascii=False, indent=2)}

论文标题：
{title}

论文摘要：
{abstract}
"""
    result = call_llm_json(prompt)
    if result.get("parse_error"):
        return {
            "is_relevant": False,
            "matched_topic_ids": [],
            "matched_topic_names": [],
            "relevance_score": 0.0,
            "reason": f"无法解析相关性过滤输出：{result.get('raw_output', '')}",
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
你是一位法律 AI / 法律 NLP 研究助理。

用 3-5 个简洁的句子总结以下论文。重点包括：
1. 问题/任务，
2. 方法，
3. 主要发现或结果，
4. 贡献总结。

匹配主题：
{matched_topic_names}

标题：
{title}

摘要：
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
            "summary": summary,
        })

    return rows, newly_seen


def save_report(rows, start_time, end_time):
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_path = REPORT_DIR / f"arxiv_digest_{date}.csv"
    md_path = REPORT_DIR / f"arxiv_digest_{date}.md"

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# arXiv 研究论文摘要\n\n")
        f.write(f"**时间窗口：** {start_time} 至 {end_time}\n\n")
        f.write(f"**相关论文数量：** {len(rows)}\n\n")

        grouped = {}

        for row in rows:
            topic_names = row["matched_topic_names"] or "未分类"
            grouped.setdefault(topic_names, []).append(row)

        for topic_name, papers in grouped.items():
            f.write(f"# 主题：{topic_name}\n\n")

            for i, row in enumerate(papers, 1):
                f.write(f"## {i}. {row['title']}\n\n")
                f.write(f"**作者：** {row['authors']}\n\n")
                f.write(f"**发表时间：** {row['published']}\n\n")
                f.write(f"**arXiv ID：** {row['arxiv_id']}\n\n")
                f.write(f"**链接：** {row['link']}\n\n")
                f.write(f"**类别：** {row['categories']}\n\n")
                f.write(f"**匹配主题：** {row['matched_topic_names']}\n\n")
                f.write(f"**相关度分数：** {row['relevance_score']}\n\n")
                f.write(f"**相关原因：** {row['relevance_reason']}\n\n")
                f.write(f"**摘要：** {row['abstract']}\n\n")
                f.write(f"**总结：** {row['summary']}\n\n")
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
    print("完成。")
    print(f"相关论文数量：{len(rows)}")
    print(f"新处理论文数量：{len(newly_seen)}")
    print(f"累计跟踪论文数量：{len(seen_papers)}")
    print(f"CSV 报告：{csv_path}")
    print(f"Markdown 报告：{md_path}")
    print(f"扩展关键词：{EXPANDED_KEYWORDS_PATH}")


if __name__ == "__main__":
    main()
