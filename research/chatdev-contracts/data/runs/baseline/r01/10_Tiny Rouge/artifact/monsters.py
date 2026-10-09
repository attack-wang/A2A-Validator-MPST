'''
Monster templates used by the map generator to spawn monsters per level.
'''
import random
MONSTER_TEMPLATES = [
    {"name": "Slime",    "hp": (3, 6),   "color": (90, 200, 90),   "glyph": "s"},
    {"name": "Bat",      "hp": (4, 8),   "color": (170, 110, 220), "glyph": "b"},
    {"name": "Skeleton", "hp": (6, 12),  "color": (225, 220, 200), "glyph": "k"},
    {"name": "Orc",      "hp": (9, 16),  "color": (200, 80, 60),   "glyph": "o"},
    {"name": "Golem",    "hp": (14, 24), "color": (140, 140, 150), "glyph": "g"},
    {"name": "Wraith",   "hp": (18, 30), "color": (60, 190, 190),  "glyph": "w"},
    {"name": "Demon",    "hp": (24, 40), "color": (230, 60, 90),   "glyph": "d"},
]
def pick_monster_template(level, rng):
    """Pick a monster template whose difficulty scales with the level."""
    # Higher levels unlock stronger templates
    max_index = min(len(MONSTER_TEMPLATES) - 1, (level - 1) // 2)
    index = rng.randint(0, max_index)
    return MONSTER_TEMPLATES[index]