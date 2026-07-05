---
name: arxiv-paper-watcher-digest-zh
description: 监控 arXiv 上用户研究领域的最新论文，并生成自上次运行以来的相关论文摘要。当用户想要查找 arXiv 上的相关新论文、获取 arXiv 论文订阅、跟踪或监控某个 arXiv 主题、接收近期 arXiv 论文摘要，或在无需手动搜索或浏览的情况下发现与配置的研究兴趣相关的新发表论文时使用。
type: prompt
---

# arXiv 论文监控与摘要 Skill

## 用途

监控 arXiv 上用户研究领域的最新论文，并生成自上次运行以来的相关论文摘要。工作流应获取自上次记录运行以来到当前日期的新 arXiv 论文，筛选真正相关的内容，总结相关论文，并保存摘要报告。

## 仓库结构

假设项目包含：

- `config/topics.yaml`
- `.claude/skills/arxiv-paper-watcher-digest-zh/scripts/arxiv_paper_watcher_digest.py`
- `.claude/skills/arxiv-paper-watcher-digest-zh/references/topics-example.yaml`
- `state/last_run.json`
- `state/seen_papers.json`
- `state/expanded_keywords.json`
- `reports/`
- `requirements.txt`
- `.env`
- `.claude/skills/arxiv-paper-watcher-digest-zh/SKILL.md`

## 工作流

1. 运行 `.claude/skills/arxiv-paper-watcher-digest-zh/scripts/arxiv_paper_watcher_digest.py`；如果缺少依赖，提示用户根据 `requirements.txt` 安装。
2. 脚本需要从 `.env` 中读取 `OPENAI_API_KEY`；切勿打印、暴露或记录 API 密钥。如果密钥不可用，停止执行并请用户配置。
3. 从 `config/topics.yaml` 读取研究主题。在解释或重建配置格式时，使用 `references/topics-example.yaml` 作为参考模板。
4. 从 `state/last_run.json` 读取上次运行时间戳；如果文件不存在，使用默认开始日期（例如 `2026-01-01`）。
5. 检索 `last_run` 之后发表的论文，处理论文，并在整个工作流成功完成后更新 `last_run`。

## 错误处理

- 如果 arXiv API 调用失败，记录错误并停止执行。
- 如果 OpenAI API 调用失败，记录错误并停止执行。
- 如果某个论文处理步骤失败，记录错误，跳过该论文，并继续处理下一篇。单个论文失败不应终止整个摘要生成。
