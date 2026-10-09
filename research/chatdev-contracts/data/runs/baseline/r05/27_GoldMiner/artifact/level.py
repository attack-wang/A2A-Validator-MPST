counts = {
    "gold_small": max(2, 6 - level),
    "gold_medium": 3 + level // 2,
    "gold_large": 1 + level // 2,
    "diamond": (1 + (level - 2) // 3) if level >= 2 else 0,
    "rock_small": 2 + level,
    "rock_large": 1 + level // 2,
    "bone": 1 + level // 2,
    "tnt": 0 if level < 2 else min(6, 1 + (level - 2) // 2),
}