"""Check one content module on its own.
  python3 src/check_bank.py dom3        # section bank + cards
  python3 src/check_bank.py mock1_a     # one half of the mock (list ITEMS): validation with per-option why + EXAM LEVEL
"""
import importlib, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_site import validate, exam_level, check_cards

name = sys.argv[1]; mod = importlib.import_module(name)
if name.startswith("mock"):
    items = mod.ITEMS
    bank = dict(id=name, minutes=90, items=items)
    ok = validate(bank, need_why=True) and exam_level(bank)
    by = {}
    for q in items: by[q["skill"]] = by.get(q["skill"], 0) + 1
    print("  by section:", by)
else:
    ok = validate(mod.BANK) and check_cards(mod)
    print(f"  cards: {len(mod.CARDS)}  clusters: {[c for c, _ in mod.CLUSTERS]}")
sys.exit(0 if ok else 1)
