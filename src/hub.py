"""Hub content: verified exam facts, services and features map, docs drift note, 2-week study plan."""
import html
E = html.escape
from build_site import md

CERT = "https://www.databricks.com/learn/certification/genai-engineer-associate"
GUIDE = "https://www.databricks.com/sites/default/files/2026-10/databricks-certified-gen-ai-associate-exam-guide-august-2026.pdf"
D = "https://docs.databricks.com/aws/en/"

FACTS = [
    ("Exam", "Databricks Certified Generative AI Engineer Associate (proctored)"),
    ("Exam guide", "Titled \"Exam Guide – August 2026\" and linked from the certification page (file path dated 2026-10). Its updates table says: exam published **18 March 2026**, guide updated **18 March 2026**."),
    ("Scored items", "**45** scored items, multiple choice and multiple selection"),
    ("Unscored items", "Up to **10** more unscored items, not identified, which don't count"),
    ("Time", "**90 minutes**, with extra time for unscored items already included"),
    ("Passing score", "**Not published** in the guide or on the certification page. This site's mock and banks use a self-set target of 80%."),
    ("Question types", "Multiple choice (choose one) and multiple selection (\"Which TWO…\"). No case studies, drag and drop or code-completion items."),
    ("Test aids", "None allowed (closed book)"),
    ("Fee", "USD 200 plus tax"),
    ("Delivery", "Guide: online proctored. Certification page: online or test center."),
    ("Languages", "English, Japanese, Brazilian Portuguese, Korean"),
    ("Prerequisites", "None. Training is highly recommended, along with 6+ months of hands-on experience with the outline's tasks."),
    ("Validity", "2 years. You recertify by taking the current live exam."),
    ("Recommended training", "Instructor-led: Generative AI Engineering with Databricks. Self-paced (Databricks Academy): Building RAG Agents with Agent Bricks; Building Agentic Applications on Databricks; Agent Evaluation on Databricks; Deploying and Monitoring Agent Applications on Databricks."),
]

def facts_html():
    rows = "".join(f"<tr><td><b>{E(k)}</b></td><td>{md(v)}</td></tr>" for k, v in FACTS)
    return f'''<div class="tbl"><table><thead><tr><th>The exam (verified 1 Nov 2026)</th><th></th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="note">Sources: <a href="{CERT}" target="_blank" rel="noopener">certification page</a> · <a href="{GUIDE}" target="_blank" rel="noopener">official exam guide (PDF)</a>. The guide asks you to check it again two weeks before your exam, because the outline can change.</p>
<div class="frame"><b>Docs have moved past the exam guide.</b> The guide is from March 2026, but the Databricks docs changed several names in the months after it. The exam tests the guide's names, so this site uses them and notes the new names on the cards.
<ul style="margin:6px 0 0;padding-left:18px">
<li><b>Mosaic AI Vector Search</b> is now called <b>Databricks AI Search</b>. Many APIs still use "vector-search" in paths and identifiers (<a href="{D}ai-search/ai-search" target="_blank" rel="noopener">docs</a>).</li>
<li><b>Knowledge Assistant</b> and <b>Supervisor Agent</b> (the guide's "Multiagent Supervisor") are labelled legacy for new agents. The docs point to <b>Genie Agents</b> (formerly Genie Spaces), the <b>Agent Bricks CLI</b> and <b>Agent Runtime</b> on Databricks Apps (<a href="{D}agents/concepts/" target="_blank" rel="noopener">docs</a>). The guide still tests all three Agent Bricks.</li>
<li>The serving-endpoint <b>AI Gateway</b> is labelled legacy beside the newer <b>Unity Gateway</b>, which has the same jobs: rate limits, inference tables, usage tracking, and guardrails through service policies (<a href="{D}ai-gateway/" target="_blank" rel="noopener">docs</a>).</li>
<li>Databricks Asset Bundles appear in the docs as Declarative Automation Bundles.</li></ul></div>'''

# (piece, what it's for, exam depth, sections)
MAP = [
    ("Agent Bricks: Knowledge Assistant", "No-code document Q&A agent with citations over UC volumes, tables or indexes; SMEs improve it with labelled questions and guidelines.", "Medium: when to use it vs build your own", "S1"),
    ("Agent Bricks: Supervisor Agent (Multi-Agent Supervisor)", "Coordinates subagents and tools, including Genie, agent endpoints and UC functions. Each end user needs access to each subagent.", "Medium", "S1"),
    ("Agent Bricks: Information Extraction", "Turns documents into JSON for a schema you define. Built on `ai_extract`; runs from SQL, a pipeline or a REST endpoint.", "Medium", "S1"),
    ("Mosaic AI Vector Search (now AI Search)", "Managed vector index. Endpoint types: standard (about 320M vectors at 768 dims, high QPS) or storage-optimized (over 1B vectors, about 250 ms slower, triggered sync only). Index types: Delta Sync (managed or self-managed embeddings) or Direct Vector Access. Supports hybrid search, filters and a reranker.", "High: create, query, choose an endpoint, keep in sync", "S2, S4"),
    ("Delta Lake + Unity Catalog", "Chunk tables (Change Data Feed on for Delta Sync), volumes for raw files, three-level names, grants, models and functions in UC, row filters and column masks.", "High", "S2, S4, S5"),
    ("AI Functions", "`ai_query` (general batch inference in SQL), `ai_parse_document` (PDF, Office and images to elements), `ai_extract`, `ai_mask`, `ai_classify`, `ai_summarize`.", "Medium: batch inference with `ai_query` is an objective", "S2, S4, S5"),
    ("Foundation Model APIs", "Databricks-hosted LLMs and embedding models. Pay-per-token (including a priority tier) for prototyping, provisioned throughput for production, fine-tuned weights and HIPAA.", "High", "S3, S4"),
    ("Model Serving", "Endpoints for agents, custom models and external models. Permissions are CAN VIEW, CAN QUERY and CAN MANAGE. Resource access works through automatic passthrough (declared `resources`), on-behalf-of-user (preview) or secrets.", "High", "S4"),
    ("MLflow models: pyfunc and models from code", "Wrap a chain with pre- and post-processing, set a signature and input example, log dependencies, and register to UC with aliases (no stages).", "High", "S4"),
    ("Mosaic AI Agent Framework", "Author agents with MLflow `ResponsesAgent`, tools from UC functions, retriever tools, and deploy with `agents.deploy()`. Deploying also sets up a Review App, tracing and inference tables.", "High", "S3, S4"),
    ("LangChain on Databricks", "`databricks-langchain` classes: `ChatDatabricks`, `DatabricksEmbeddings`, `DatabricksVectorSearch` retriever, `UCFunctionToolkit`, `GenieAgent`.", "Medium", "S3"),
    ("Genie Spaces (now Genie Agents) and Conversation API", "Natural-language questions over tables. The API returns SQL and results and applies the caller's UC permissions. In multi-agent systems, Genie is the structured-data worker.", "Medium", "S3"),
    ("MLflow Prompt Registry (Beta)", "Immutable prompt versions, movable aliases such as `@production`, loaded by URI. This is how you promote prompts across environments and roll back.", "Medium", "S4"),
    ("MCP servers", "Managed (Databricks-hosted: Genie, Vector Search, UC functions, SQL), external (third-party, registered through a UC connection with secrets) and custom (your own, hosted on Databricks Apps).", "Medium", "S4"),
    ("Agent memory (Lakebase)", "Sessions keep one conversation; memory keeps facts across conversations. Both are managed and backed by Lakebase.", "Light to medium", "S4"),
    ("Databricks Apps, Review App, Slack/Teams", "User-facing interfaces. Apps keep tokens server-side and use the signed-in user's identity. The Review App collects SME feedback. Genie integrates with Teams and Slack.", "Medium", "S4, S6"),
    ("MLflow evaluation: judges and scorers", "`mlflow.genai.evaluate()` with built-in judges. Correctness, RetrievalSufficiency and ToolCallCorrectness need ground truth; RelevanceToQuery, RetrievalRelevance, RetrievalGroundedness, Safety and Guidelines don't. Custom `@scorer` functions; `make_judge` and judge alignment from SME labels.", "High", "S6"),
    ("MLflow Tracing", "Records every step's inputs, outputs, latency and tokens. Autolog covers common frameworks, and `@mlflow.trace` covers your own functions.", "Medium", "S6"),
    ("Production monitoring (Agent Monitoring)", "The same scorers run on a sample of live traces (`register()` then `start(sampling_config=...)`). Beta.", "Medium", "S6"),
    ("AI Gateway (legacy; now Unity Gateway)", "On serving endpoints: inference tables (requests and responses to Delta), usage tracking (`system.serving.endpoint_usage`), rate limits (QPM/TPM by endpoint, user or group), guardrails (safety filter; PII Block or Mask; preview).", "High", "S3, S5, S6"),
    ("Cost controls", "Pay-per-token vs provisioned throughput, scale to zero, rate limits, smaller models, batch with `ai_query`, usage system tables. Serverless budget policies only tag usage; they don't cap spend.", "Medium", "S6"),
    ("Open-source parsers", "pypdf / PyPDF2 (PDF text), unstructured (mixed formats), Tesseract / pytesseract (OCR on scans), BeautifulSoup (HTML).", "Light: pick the right package for the format", "S2"),
]

def map_html():
    rows = "".join(f"<tr><td><b>{md(a)}</b></td><td>{md(b)}</td><td>{md(c)}</td><td>{E(d)}</td></tr>" for a, b, c, d in MAP)
    return f'''<h2>Services and features map</h2>
<p class="note">Only what the March 2026 outline covers. "Depth" is this site's reading of the objectives: High means expect several questions on details and trade-offs; Light means know what it's for.</p>
<div class="tbl"><table><thead><tr><th>Databricks piece</th><th>What it's for</th><th>Exam depth</th><th>Sections</th></tr></thead><tbody>{rows}</tbody></table></div>'''

PLAN = [
    ("1", "Re-read the official exam guide (it asks for this two weeks before the exam). Read this hub's map and drift note, then the S1 cards.", "S1 practice bank"),
    ("2", "S2 cards: chunking, parsers, writing chunks to Delta, retrieval metrics, reranking.", "S2 practice bank"),
    ("3", "S3 clusters A and B: frameworks, choosing models, prompts, guardrails. Skim anything you already know from AI-103 and CCA-F.", "First half of S3 bank"),
    ("4", "S3 cluster C: Agent Framework, evaluation vs monitoring, Genie in multi-agent systems.", "Rest of S3 bank"),
    ("5", "S4 clusters A and B: pyfunc, signatures, UC registration, Vector Search endpoints and indexes.", "S4 items on these cards"),
    ("6", "S4 cluster C: serving access, Foundation Model APIs, ai_query, MCP, memory, prompt registry, CI/CD, interfaces.", "Rest of S4 bank"),
    ("7", "Hands-on in Databricks Free Edition (the guide recommends it): parse a few PDFs, chunk to a Delta table, build a Vector Search index, query it, then batch-summarise with `ai_query`.", "Write down what surprised you"),
    ("8", "S5 and S6 cards: masking, guardrails, licensing; judges, scorers, tracing, inference tables, AI Gateway, cost.", "S5 bank"),
    ("9", "Learn the judges table by heart: which need ground truth, which don't.", "S6 bank"),
    ("10", "Mock Exam #1 in exam mode: 90 minutes, no notes.", "Score it; list every miss"),
    ("11", "For each mock miss, reread its card and write down the rule you missed.", "Redo the missed items in practice mode"),
    ("12", "Hands-on: log a small agent with `ResponsesAgent`, register it to UC with an alias, run `mlflow.genai.evaluate()` with two built-in judges and one custom scorer.", "Re-run S3 and S4 banks in exam mode"),
    ("13", "Weakest two sections again. Re-run their banks in exam mode until you score 80% or more.", "S5 and S6 banks in exam mode"),
    ("14", "Light day: drift note, judges table, Vector Search endpoint table. Retake Mock #1 in exam mode only if day 10 was under 80%.", "Rest"),
]

def plan_html():
    rows = "".join(f"<tr><td><b>Day {d}</b></td><td>{md(f)}</td><td>{md(p)}</td></tr>" for d, f, p in PLAN)
    return f'''<h2>Two-week study plan</h2>
<p class="note">About 90 minutes a day, starting the day after AI-103. S3 and S4 together are 52% of the exam, so they get four days. Where Azure or Claude already taught the concept, read the bridge line on the card and spend the time on the Databricks names.</p>
<div class="tbl"><table><thead><tr><th>Day</th><th>Study</th><th>Practice</th></tr></thead><tbody>{rows}</tbody></table></div>'''
