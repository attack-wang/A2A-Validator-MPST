'''
level.py
Level generation and difficulty curve for the Gold Miner game.
Higher levels get MORE objects (including obstacles), a FASTER swinging
claw and a TIGHTER time limit, while the cumulative score goal grows.
'''
import random
import settings
from objects import Gold, Rock, Diamond, Skull
# kind -> concrete class used by the level generator
OBJECT_CLASSES = {
    "gold_small": Gold,
    "gold_medium": Gold,
    "gold_large": Gold,
    "rock": Rock,
    "diamond": Diamond,
    "skull": Skull,
}
def level_time_limit(level):
    """Tighter time limits as levels ascend: 60s down to a 30s floor."""
    return max(30, 60 - (level - 1) * 4)
def level_goal(level):
    """Cumulative gold value required to finish `level`.
    The player's score carries over between levels, so the goal is the
    running total: level 1 needs 250, level 2 needs 600 in total, etc.
    """
    goal = 0
    for i in range(1, level + 1):
        goal += 250 + (i - 1) * 100
    return goal
def level_swing_speed(level):
    """The claw swings faster on higher levels (capped at 3.0 deg/frame)."""
    return min(3.0, 1.6 + (level - 1) * 0.15)
class Level:
    """One mining field: a target goal, a time limit and a set of objects."""
    def __init__(self, number):
        self.number = number
        self.time_limit = level_time_limit(number)
        self.goal = level_goal(number)
        self.objects = []
        self._generate()
    def _generate(self):
        """Populate the dirt field with gold, rocks, diamonds and skulls.
        Fully random each playthrough (no fixed seed) so replays differ.
        Objects are placed with rejection sampling so they never overlap.
        """
        rng = random.Random()
        level = self.number
        specs = []
        specs += ["gold_small"] * (3 + min(4, level))          # 4..7
        specs += ["gold_medium"] * (2 + level // 2)            # 2..
        specs += ["gold_large"] * (1 + (level - 1) // 2)       # 1..
        specs += ["rock"] * (2 + level // 2)                   # obstacles
        specs += ["skull"] * (max(0, level - 2) // 2 + 1)      # obstacles
        specs += ["diamond"] * (1 + (level - 1) // 2)          # jackpot
        placed = []
        margin = 40
        top = settings.GROUND_Y + 30
        for kind in specs:
            r = settings.OBJECT_STATS[kind]["radius"]
            for _ in range(200):  # rejection sampling: avoid overlaps
                x = rng.randint(margin, settings.SCREEN_WIDTH - margin)
                y = rng.randint(top, settings.SCREEN_HEIGHT - margin)
                if all((x - px) ** 2 + (y - py) ** 2 > (r + pr + 12) ** 2
                       for px, py, pr in placed):
                    self.objects.append(OBJECT_CLASSES[kind](kind, x, y))
                    placed.append((x, y, r))
                    break