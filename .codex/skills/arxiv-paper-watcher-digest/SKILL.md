---
name: arxiv-paper-watcher-digest
description: Monitor arXiv for new papers in the user's research areas and generate a digest of relevant results since the last run. Use when the user wants to find new related papers on arXiv, get an arXiv paper feed, track or monitor arXiv for a topic, receive a digest of recent arXiv papers, or discover newly published papers relevant to configured research interests without manually searching or skimming.
---

# arXiv Paper Watcher and Digest Skill

## Purpose

Monitor arXiv for new papers in the user's research areas and generate a digest of relevant results since the last run. The workflow should retrieve new arXiv papers from the last recorded run to the current date, filter for true relevance, summarize relevant papers, and save a digest report.

## Repository layout

Assume the project contains:

config/topics.yaml
.codex/skills/arxiv-paper-watcher-digest/scripts/arxiv_paper_watcher_digest.py
.codex/skills/arxiv-paper-watcher-digest/references/topics-example.yaml
state/last_run.json
state/seen_papers.json
state/expanded_keywords.json
reports/
requirements.txt
.env
.codex/skills/arxiv-paper-watcher-digest/SKILL.md

## Workflow
1. Run .codex/skills/arxiv-paper-watcher-digest/scripts/arxiv_paper_watcher_digest.py; if dependencies are missing, prompt to install from requirements.txt
2. The script requires OPENAI_API_KEY stored in .env; never print, expose, or log the API key. If the key is unavailable, stop execution and ask the user to configure it.
3. Read research topics from config/topics.yaml. Use references/topics-example.yaml as the reference template when explaining or recreating the config shape.
4. Read the last run timestamp from state/last_run.json; if the file doesn't exist, assume a default start date (e.g., 2026-01-01).
5. Retrieve papers published after last_run, process papers, and update last_run only after successful completion of the entire workflow.

## Error handling
- If the arXiv API call fails, log the error and stop execution.
- If the OpenAI API call fails, log the error and stop execution.
- If any paper processing step fails, log the error, skip the paper, and continue with the next one. A single paper failure should not terminate the entire digest.
