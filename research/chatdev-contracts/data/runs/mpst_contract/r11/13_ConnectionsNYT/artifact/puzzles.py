"""Puzzle pool and daily selection for ChatDev Connections."""
import random
from datetime import date

# (category, words, difficulty 0-3 -> yellow, green, blue, purple)
POOL = [
    ("PLANETS", ["MERCURY", "VENUS", "EARTH", "MARS"], 0),
    ("CHESS PIECES", ["ROOK", "BISHOP", "KNIGHT", "PAWN"], 0),
    ("DOG COMMANDS", ["SIT", "STAY", "HEEL", "ROLL"], 0),
    ("___ BOARD", ["KEY", "SKATE", "SURF", "SNOW"], 1),
    ("BEARS", ["GRIZZLY", "POLAR", "PANDA", "KOALA"], 1),
    ("MOVIE GENRES", ["WESTERN", "HORROR", "ROMANCE", "THRILLER"], 1),
    ("HOMOPHONES OF NUMBERS", ["WON", "TOO", "FORE", "ATE"], 2),
    ("COFFEE DRINKS", ["LATTE", "MOCHA", "ESPRESSO", "CORTADO"], 2),
    ("SAILING TERMS", ["JIB", "MAST", "TACK", "REEF"], 2),
    ("___ PRESS", ["BENCH", "PRINT", "CIDER", "FRENCH"], 3),
    ("SPOKEN AS LETTERS", ["WHY", "BEE", "SEA", "ARE"], 3),
    ("CARD GAMES", ["BRIDGE", "HEARTS", "SOLITAIRE", "RUMMY"], 3),
]


def daily_puzzle(day=None):
    """Deterministically build today's 4x4 puzzle: 4 disjoint categories, shuffled words."""
    rng = random.Random(f"chatdev-connections-{(day or date.today()).isoformat()}")
    groups = sorted(rng.sample(POOL, 4), key=lambda g: g[2])
    return [(name, level, rng.sample(words, len(words))) for name, words, level in groups]