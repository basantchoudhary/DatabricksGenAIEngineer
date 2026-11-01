"""Shared helpers for question banks. Write the correct option FIRST (answer=0 for single);
the build shuffles options with a seed chosen to balance answer positions and length tells."""
D = "https://docs.databricks.com/aws/en/"
ML = "https://mlflow.org/docs/latest/"
GUIDE = "https://www.databricks.com/sites/default/files/2026-10/databricks-certified-gen-ai-associate-exam-guide-august-2026.pdf"

# Mock exam skill labels (exact strings; the mock page groups by these)
S1, S2, S3 = "S1 · Design Applications", "S2 · Data Preparation", "S3 · Application Development"
S4, S5, S6 = "S4 · Assembling and Deploying Applications", "S5 · Governance", "S6 · Evaluation and Monitoring"

def T(premise, mp, apply, rule, guide):
    """Think-it-through block: premise to correct, mind map rows [observe, where, fix], stem quotes [quote, meaning], rule, exam-guide objective (verbatim)."""
    return dict(premise=premise, map=mp, apply=apply, rule=rule, guide=guide)

def single(id, skill, stem, options, runner, runnerWhy, think, eli5, learn, why=None):
    """Choose one. options[0] is the key. why = one reason per option, same order as options."""
    q = dict(id=id, type="single", skill=skill, stem=stem, options=options, answer=0, runner=runner, runnerWhy=runnerWhy, think=think, eli5=eli5, learn=learn)
    if why: q["why"] = why
    return q

def multi(id, skill, stem, options, answer, runner, runnerWhy, think, eli5, learn, why=None, pick=2):
    """Choose two (or three). answer = list of indexes into options."""
    q = dict(id=id, type="multi", pick=pick, skill=skill, stem=stem, options=options, answer=answer, runner=runner, runnerWhy=runnerWhy, think=think, eli5=eli5, learn=learn)
    if why: q["why"] = why
    return q

def yesno(id, skill, stem, statements, think, eli5, learn):
    """statements = [(text, True/False, why), ...]. Mixed answers required."""
    return dict(id=id, type="yesno", skill=skill, stem=stem, statements=[dict(text=t, answer=a, why=w) for t, a, w in statements], think=think, eli5=eli5, learn=learn)

def order(id, skill, stem, pool, answer, think, eli5, learn):
    return dict(id=id, type="order", skill=skill, stem=stem, pool=pool, answer=answer, think=think, eli5=eli5, learn=learn)

def code(id, skill, stem, src, blanks, think, eli5, learn):
    """src uses [[0]], [[1]] ... for blanks; blanks = [(options, answer_index, why), ...]."""
    return dict(id=id, type="code", skill=skill, stem=stem, code=src, blanks=[dict(options=o, answer=a, why=w) for o, a, w in blanks], think=think, eli5=eli5, learn=learn)
