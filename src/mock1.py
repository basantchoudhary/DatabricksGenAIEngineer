"""Mock Exam #1: 45 original items (the real exam's scored count), 90 minutes, weighted by section.
Part A (mock1_a): S1 6 · S2 6 · S3 14.  Part B (mock1_b): S4 10 · S5 4 · S6 5.
Items are interleaved with a fixed seed so sections mix, as on the real exam."""
import random
from mock1_a import ITEMS as A
from mock1_b import ITEMS as B

items = A + B
random.Random(45).shuffle(items)
BANK = dict(id="m1", title="Mock Exam #1", minutes=90, mode="practice", v=1, items=items)
