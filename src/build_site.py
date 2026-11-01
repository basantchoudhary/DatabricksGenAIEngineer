"""Build the DatabricksGenAIEngineer site.  Run:  python3 src/build_site.py
Exits non-zero if any bank fails validation or the mock fails the EXAM LEVEL check."""
import copy, html, importlib, json, os, random, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

E = html.escape
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap">'
CHECKED = "1 November 2026"

# (module, folder, n, weight, official section name, h1, lede)
SECTIONS = [
    ("dom1", "S1-Design-Apps", 1, "14%", "Design Applications", "Design <span>applications</span>",
     "Prompts that return a set format, picking model tasks and chain parts, ordering tools for multi-step reasoning, and when an Agent Bricks agent beats building your own. <em>Mostly reasoning from requirements; the Databricks part is Agent Bricks.</em>"),
    ("dom2", "S2-Data-Prep", 2, "14%", "Data Preparation", "Data <span>preparation</span>",
     "Chunking, cleaning and extracting documents, writing chunks to Delta tables in Unity Catalog, and measuring and improving retrieval. <em>The RAG front end you know, with Databricks' tables and functions.</em>"),
    ("dom3", "S3-App-Dev", 3, "30%", "Application Development", "Application <span>development</span>",
     "The biggest section: prompts, guardrails, choosing LLMs and embedding models, MLflow and the Agent Framework, and Genie in multi-agent systems. <em>Concepts carry over from Azure and Claude; spend your time on the Databricks names.</em>"),
    ("dom4", "S4-Assemble-Deploy", 4, "22%", "Assembling and Deploying Applications", "Assemble and <span>deploy</span>",
     "pyfunc chains, registering to Unity Catalog, Model Serving and Foundation Model APIs, Vector Search set-up, ai_query() batch jobs, memory stores, CI/CD, MCP servers, prompt versioning and user interfaces. <em>The most Databricks-specific section.</em>"),
    ("dom5", "S5-Governance", 5, "8%", "Governance", "<span>Governance</span>",
     "Masking, guardrails against malicious input, licensing of data sources, and what to do about problem text in a source. <em>Small section, mostly judgement.</em>"),
    ("dom6", "S6-Eval-Monitor", 6, "12%", "Evaluation and Monitoring", "Evaluate and <span>monitor</span>",
     "MLflow evaluation, scorers and judges, tracing, inference tables, AI Gateway, cost controls and SME feedback. <em>Know which judges need ground truth and which Databricks table holds what.</em>"),
]

def md(s):
    s = E(s)
    s = re.sub(r"`([^`]+)`", r'<span class="k">\1</span>', s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)

def nav_items():
    return [("Home", "index.html")] + [(f"S{n}", f"{f}/index.html") for _, f, n, *_ in SECTIONS] + [("Mock #1", "Mock-Exam-1/index.html")]

def page(title, rel, body, extra_head="", scripts=""):
    links = "".join(f'<li><a href="{rel}{h}">{t}</a></li>' for t, h in nav_items())
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>{FONTS}<link rel="stylesheet" href="{rel}assets/site.css">{extra_head}</head>
<body><div class="bar"><div class="bar-in"><a class="brand" href="{rel}index.html">Databricks GenAI Engineer Associate</a><ul class="nav">{links}</ul></div></div>
<main>{body}</main>
<footer>Original study material for the Databricks Certified Generative AI Engineer Associate exam. Not affiliated with Databricks. Practice items are original and are not real exam questions. Exam facts from the official exam guide; product facts checked against docs.databricks.com on {CHECKED}.</footer>
{scripts}</body></html>"""

# ---------- validation ----------
def _shuffle(q, idx):
    q["options"] = [q["options"][i] for i in idx]
    if q.get("why"): q["why"] = [q["why"][i] for i in idx]
    if q["type"] == "single": q["answer"] = idx.index(q["answer"])
    else: q["answer"] = sorted(idx.index(a) for a in q["answer"])
    if q.get("runner") is not None: q["runner"] = idx.index(q["runner"])

def best_seed(bank):
    """Pick the shuffle seed that balances answer positions and keeps length strategies near chance."""
    def score(seed):
        b = copy.deepcopy(bank); r = random.Random(seed); sg = []
        for q in b["items"]:
            if q["type"] in ("single", "multi"):
                idx = list(range(len(q["options"]))); r.shuffle(idx); _shuffle(q, idx)
                if q["type"] == "single": sg.append(q)
        pos = [sum(q["answer"] == k for q in sg) for k in range(4)]
        lo = sum(max(range(4), key=lambda k: (len(q["options"][k]), -k)) == q["answer"] for q in sg)
        sh = sum(min(range(4), key=lambda k: (len(q["options"][k]), k)) == q["answer"] for q in sg)
        return (max(pos) - min(pos)) * 3 + max(lo, sh)
    return min(range(1, 600), key=score)

def validate(bank, need_why=False):
    fail = []
    ids = [q["id"] for q in bank["items"]]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup: fail.append(f"duplicate ids {sorted(dup)}")
    for q in bank["items"]:
        if q["type"] == "single" and len(q["options"]) != 4: fail.append(f"{q['id']}: single needs 4 options")
        if q["type"] in ("single", "multi"):
            if q.get("why") and len(q["why"]) != len(q["options"]): fail.append(f"{q['id']}: why/options length mismatch")
            if need_why and not q.get("why"): fail.append(f"{q['id']}: missing per-option why")
            if q["type"] == "multi" and len(q["answer"]) != q["pick"]: fail.append(f"{q['id']}: pick/answer mismatch")
    rng = random.Random(best_seed(bank))
    singles = [q for q in bank["items"] if q["type"] == "single"]
    for q in bank["items"]:
        if q["type"] in ("single", "multi"):
            idx = list(range(len(q["options"]))); rng.shuffle(idx); _shuffle(q, idx)
    def rate(pick): return sum(pick(q) == q["answer"] for q in singles) / max(1, len(singles))
    longest = rate(lambda q: max(range(4), key=lambda k: (len(q["options"][k]), -k)))
    shortest = rate(lambda q: min(range(4), key=lambda k: (len(q["options"][k]), k)))
    pos = [sum(q["answer"] == k for q in singles) for k in range(4)]
    if max(pos) - min(pos) > max(2, len(singles) // 4): fail.append(f"answer positions skewed {pos}")
    if longest > .35: fail.append(f"pick-longest {longest:.0%}")
    if shortest > .35: fail.append(f"pick-shortest {shortest:.0%}")
    for q in bank["items"]:
        if q["type"] == "multi":
            right = [len(q["options"][a]) for a in q["answer"]]; wrong = [len(o) for k, o in enumerate(q["options"]) if k not in q["answer"]]
            if min(right) > max(wrong): fail.append(f"{q['id']}: correct options are the longest")
        if q["type"] == "yesno":
            ys = sum(s["answer"] for s in q["statements"])
            if ys in (0, len(q["statements"])): fail.append(f"{q['id']}: all statements share one answer")
    sol = [q["answer"] for q in bank["items"] if q["type"] == "solution"]
    if sol and (all(sol) or not any(sol)): fail.append("solution series all one answer")
    kinds = {}
    for q in bank["items"]: kinds[q["type"]] = kinds.get(q["type"], 0) + 1
    print(f"{bank['id']}: {len(bank['items'])} items {kinds} · singles pick-longest={longest:.0%} pick-shortest={shortest:.0%} positions={pos}")
    print("  VALIDATION:", "PASS" if not fail else fail)
    return not fail

def exam_level(bank):
    stems = [len(q["stem"].split()) for q in bank["items"] if not q.get("case") and q["type"] not in ("yesno", "solution")]
    cases = bank.get("cases") or {}
    case_words = {k: len(" ".join(x for t in c["tabs"] for x in t["items"]).split()) for k, c in cases.items()}
    lvl = sum(stems) / len(stems) >= 40 and min(stems) >= 35 and (not case_words or min(case_words.values()) >= 700)
    print(f"  EXAM LEVEL: stem mean {sum(stems)/len(stems):.0f} min {min(stems)}" + (f" · case words {case_words}" if case_words else " · no case studies (none on this exam)") + " →", "PASS" if lvl else "FAIL")
    return lvl

def check_cards(mod):
    ids = {q["id"] for q in mod.BANK["items"]}; bad = []
    for c in mod.CARDS:
        for k in ("id", "c", "title", "one", "bridge", "steps", "facts", "traps", "checks", "src"):
            if k not in c: bad.append(f"card {c.get('id')}: missing {k}")
        bad += [f"card {c['id']}: check {x} not in bank" for x in c.get("checks", []) if x not in ids]
    if bad: print("  CARDS:", bad)
    return not bad

# ---------- pages ----------
def cards_html(mod):
    out = []
    for cid, cname in mod.CLUSTERS:
        items = []
        for c in [c for c in mod.CARDS if c["c"] == cid]:
            steps = "".join(f"<li>{md(x)}</li>" for x in c["steps"])
            facts = "".join(f"<li>{md(x)}</li>" for x in c["facts"])
            traps = "".join(f"<li>{md(x)}</li>" for x in c["traps"])
            checks = " · ".join(f'<a href="practice.html#Q-{q}">{q}</a>' for q in c["checks"])
            t = c.get("table")
            table = ('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{E(h)}</th>" for h in t["head"]) + '</tr></thead><tbody>' +
                     "".join("<tr>" + "".join(f"<td>{md(x)}</td>" for x in r) + "</tr>" for r in t["rows"]) + '</tbody></table></div>') if t else ""
            code = f'<pre class="code">{E(c["code"])}</pre>' if c.get("code") else ""
            src = c["src"] if isinstance(c["src"], list) else [c["src"]]
            srcs = " · ".join(f'<a href="{E(u)}" target="_blank" rel="noopener">{E(u.replace("https://docs.databricks.com/aws/en/", "docs: ").replace("https://mlflow.org/docs/latest/", "mlflow: "))}</a>' for u in src)
            items.append(f'''<article class="card" id="C-{c["id"]}"><header><span class="cid">{c["id"]}</span><h3>{md(c["title"])}</h3></header>
<p class="one">{md(c["one"])}</p>
<div class="bridge"><b>If you know this from Azure/Claude:</b> {md(c["bridge"])}</div>
<div class="cgrid"><div class="box"><h4>How it works</h4><ol>{steps}</ol></div><div class="box"><h4>Must know</h4><ul>{facts}</ul></div></div>
{table}{code}<div class="box trapbox"><h4>Traps</h4><ul>{traps}</ul></div>
<p class="note">Quick check: {checks} · Source: {srcs}</p></article>''')
        out.append(f'<section class="cluster"><h2><span class="cl">{cid}</span>{E(cname)}</h2>{"".join(items)}</section>')
    return "\n".join(out)

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True); open(path, "w").write(text)

def bank_js(bank):
    return "window.BANK=" + json.dumps(bank, ensure_ascii=False) + ";"

def build_section(modname, folder, n, w, full, h1, lede):
    mod = importlib.import_module(modname)
    ok = validate(mod.BANK) and check_cards(mod)
    d = os.path.join(ROOT, folder); k = len(mod.BANK["items"])
    ey = f'<div class="eyebrow"><b>Section {n} · {w}</b>{E(full)}</div>'
    write(os.path.join(d, "bank.js"), bank_js(mod.BANK))
    write(os.path.join(d, "practice.html"), page(f"S{n} practice · Databricks GenAI", "../", f'''{ey}
<h1>S{n} practice <span>bank</span></h1>
<p class="lede">{k} original items. <em>Practice mode explains each answer as you go; exam mode is timed and scores at the end.</em></p>
<p class="note">The real exam uses only two formats: choose one, and choose two (multiple selection). Items marked "study drill" (yes/no, put in order, complete the code) are extra practice formats, not exam formats.</p>
<div id="bank"></div>''', scripts='<script src="bank.js"></script><script src="../assets/practice.js"></script>'))
    write(os.path.join(d, "index.html"), page(f"S{n} · {full} · Databricks GenAI", "../", f'''{ey}
<h1>{h1}</h1>
<p class="lede">{lede}</p>
<div class="tiles"><a class="tile" href="practice.html"><span class="lv">Practice</span><b>S{n} practice bank →</b><p>{k} items, practice or timed exam mode.</p></a>
<div class="tile"><span class="lv">Teaching cards</span><b>{len(mod.CARDS)} cards</b><p>One-liner, how it works, must-know facts, traps and a quick check for each.</p></div></div>
{cards_html(mod)}'''))
    return ok, mod

def build_mock1():
    import mock1
    b = mock1.BANK; ok = validate(b, need_why=True); ok = exam_level(b) and ok
    d = os.path.join(ROOT, "Mock-Exam-1")
    write(os.path.join(d, "bank.js"), bank_js(b))
    dom, fmt = {}, {}
    for q in b["items"]:
        k = q["skill"]; dom[k] = dom.get(k, 0) + 1
        fmt[q["type"]] = fmt.get(q["type"], 0) + 1
    wt = {f"S{n}": w for _, _, n, w, *_ in SECTIONS}
    rows = "".join(f"<tr><td><b>{E(k)}</b></td><td>{wt.get(k.split(' ·')[0], '')}</td><td>{v}</td></tr>" for k, v in sorted(dom.items()))
    write(os.path.join(d, "index.html"), page("Mock Exam #1 · Databricks GenAI", "../", f'''<div class="eyebrow"><b>Mock exam</b>Generative AI Engineer Associate · full length</div>
<h1>Mock Exam <span>#1</span></h1>
<p class="lede">{len(b["items"])} original items in {b["minutes"]} minutes, weighted like the real exam's six sections. <em>It opens in practice mode: the answer and a full explanation show as soon as you answer. For a timed run, switch to exam mode, which hides answers until you finish.</em></p>
<div class="tbl"><table><thead><tr><th>Section</th><th>Exam weight</th><th>Items</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="note">Formats match the real exam: {fmt.get("single", 0)} choose-one and {fmt.get("multi", 0)} choose-two items. In a choose-two item each correct selection is worth one point here. Every explanation says why the key wins and why each other option loses. Databricks does not publish its pass mark; aim for 80% or more here. These are original questions, not real exam content.</p>
<div id="bank"></div>''', scripts='<script src="bank.js"></script><script src="../assets/practice.js"></script>'))
    return ok, b

def build_home(mods, mock):
    import hub
    sec_rows = "".join(f'<tr><td><b>Section {n}</b></td><td><a href="{f}/index.html">{E(full)}</a></td><td>{w}</td><td>{round(int(w[:-1]) * 45 / 100)}</td><td>{len(mods[m].CARDS)} cards · {len(mods[m].BANK["items"])} items</td></tr>' for m, f, n, w, full, *_ in SECTIONS)
    tiles = "".join(f'<a class="tile" href="{f}/index.html"><span class="lv">S{n} · {w}</span><b>{E(full)}</b><p>{len(mods[m].CARDS)} teaching cards and a {len(mods[m].BANK["items"])}-item practice bank.</p></a>' for m, f, n, w, full, *_ in SECTIONS)
    tiles += f'<a class="tile" href="Mock-Exam-1/index.html"><span class="lv">Mock · {mock["minutes"]} min</span><b>Mock Exam #1</b><p>{len(mock["items"])} items weighted by section, exam-level stems, every option explained.</p></a>'
    body = f'''<div class="eyebrow"><b>Databricks certification</b>Generative AI Engineer Associate</div>
<h1>Pass the <span>Databricks GenAI Engineer</span> Associate</h1>
<p class="lede">Study guide, teaching cards, practice banks and a full mock for the <b>Databricks Certified Generative AI Engineer Associate</b>. <em>Built to the official exam guide, with bridges from what you already know from Azure AI-103 and Claude CCA-F.</em></p>
{hub.facts_html()}
<h2>Sections and weights</h2>
<div class="tbl"><table><thead><tr><th>Section</th><th>Name (official)</th><th>Weight</th><th>≈ items of 45</th><th>Here</th></tr></thead><tbody>{sec_rows}</tbody></table></div>
<p class="note">Weights from the official exam guide and certification page. The item counts are this site's rounding of 45 × weight; Databricks doesn't publish per-section counts.</p>
<h2>Start here</h2>
<div class="tiles">{tiles}</div>
{hub.map_html()}
{hub.plan_html()}
<div class="frame"><b>About the questions:</b> every practice item is original, written to the exam guide's objectives. None is a real exam question, and none comes from a dump. Each has a deliberate runner-up and a plain-language explanation, and the build checks that "pick the longest option" or "pick the shortest option" score near chance and that answer positions are balanced.</div>'''
    write(os.path.join(ROOT, "index.html"), page("Databricks GenAI Engineer Associate", "", body))

if __name__ == "__main__":
    ok, mods = True, {}
    for s in SECTIONS:
        r, mods[s[0]] = build_section(*s); ok = ok and r
    r, mock = build_mock1(); ok = ok and r
    build_home(mods, mock)
    print("BUILD:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
