# Databricks Generative AI Engineer Associate · study and practice

Study material for the **Databricks Certified Generative AI Engineer Associate** exam: a study guide hub, teaching cards and a practice bank for each of the six exam sections, and a full-length mock exam. It uses the same engine as the AzureAIEngineer prep repo.

Open `index.html` in a browser after building. All pages are static HTML with no server and no tracking.

## Exam facts (official exam guide, checked 1 November 2026)

| | |
|---|---|
| Scored items | 45, multiple choice and multiple selection |
| Unscored items | up to 10 more, not identified |
| Time | 90 minutes |
| Passing score | not published by Databricks |
| Test aids | none |
| Fee | USD 200 |
| Validity | 2 years; recertify by taking the current exam |
| Guide | "Exam Guide – August 2026" PDF; its updates table says exam and guide dated 18 March 2026 |

| Section | Weight | Folder |
|---|:--:|---|
| 1 · Design Applications | 14% | `S1-Design-Apps/` |
| 2 · Data Preparation | 14% | `S2-Data-Prep/` |
| 3 · Application Development | 30% | `S3-App-Dev/` |
| 4 · Assembling and Deploying Applications | 22% | `S4-Assemble-Deploy/` |
| 5 · Governance | 8% | `S5-Governance/` |
| 6 · Evaluation and Monitoring | 12% | `S6-Eval-Monitor/` |

Sources: [certification page](https://www.databricks.com/learn/certification/genai-engineer-associate) · [exam guide PDF](https://www.databricks.com/sites/default/files/2026-10/databricks-certified-gen-ai-associate-exam-guide-august-2026.pdf). Check the guide again two weeks before your exam.

The Databricks docs have renamed several products since the March 2026 guide: Vector Search is now AI Search, Genie Spaces are now Genie Agents, Knowledge Assistant and Supervisor Agent are marked legacy, and AI Gateway is marked legacy beside Unity Gateway. The questions use the exam guide's names. The hub and the cards note the new ones.

## What's inside

- `index.html`: exam facts, sections and weights, a services and features map with exam depth, the docs-drift note, and a two-week plan.
- `S1-…` to `S6-…`: `index.html` holds the teaching cards (one-liner, how it works, must-know facts, traps, quick checks, and a bridge from Azure AI-103 and Claude CCA-F). `practice.html` is the bank, with practice and timed exam modes.
- `Mock-Exam-1/`: 45 items in 90 minutes, weighted by section, in the exam's two formats. It opens in practice mode, and every item explains why the key wins and why each other option loses.

## About the questions

**Original questions, not real exam content.** Every item was written for this repo from the official objectives and the Databricks documentation. None comes from an exam dump or reproduces a real exam question, including the guide's own sample questions. Product facts that a question depends on were checked on docs.databricks.com or mlflow.org. Section banks also include a few "study drill" formats (yes/no, put in order, complete the code), which are labelled as not appearing on the exam.

## Build

```bash
python3 src/build_site.py
```

The build writes every page and exits non-zero if a check fails:

- `validate()`: shuffles options with a seed that balances answer positions. It fails if "pick the longest" or "pick the shortest" option beats 35%, if a multi-select's correct options are the longest, or if ids are duplicated.
- `EXAM LEVEL` (mock): non-case stems must average 40+ words with none under 35.
- Card checks: every card's quick-check ids exist in its bank.

Render-check every bank in Node with a stub DOM (no browser needed): `node src/render_check.js .`

Check one content file while editing: `python3 src/check_bank.py dom3` or `python3 src/check_bank.py mock1_a`.

Content lives in `src/dom1.py` … `src/dom6.py` (cards and banks), `src/mock1_a.py` and `src/mock1_b.py` (mock), and `src/hub.py` (hub tables). The engine is `assets/practice.js` and `assets/site.css`.

Not affiliated with Databricks.
