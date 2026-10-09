"""
level.py
Procedural level generation with ascending difficulty.
For each level number the generator decides how many of each object type
to spawn, how long the timer runs and what the gold target is. Placement
is random but overlap-free and keeps a clear zone under the miner.
"""
import random
import settings
from game_objects import Gold, Diamond, Rock, Bone, TNT
class LevelPlan:
    """Immutable description of one level: timer, goal and spawn counts."""
    def __init__(self, number, time_limit, goal, spawn_spec):
        self.number = number
        self.time_limit = time_limit
        self.goal = goal
        self.spawn_spec = spawn_spec  # list of (cls, spec, count)
def make_level_plan(level_number):
    """Build the difficulty-scaled plan for the given level number."""
    # Timer tightens every level until it hits the floor.
    time_limit = max(settings.MIN_LEVEL_TIME,
                     settings.BASE_LEVEL_TIME
                     - settings.TIME_DECREASE_PER_LEVEL * (level_number - 1))
    # Gold target grows every level.
    goal = settings.BASE_GOAL + settings.GOAL_INCREASE_PER_LEVEL * (level_number - 1)
    # Difficulty ramps: more junk/obstacles, richer gold to compensate.
    difficulty = level_number - 1
    spawn_spec = [
        (Gold, settings.GOLD_SMALL, 4 + max(0, 3 - difficulty // 2)),
        (Gold, settings.GOLD_MEDIUM, 3),
        (Gold, settings.GOLD_LARGE, 1 + difficulty // 3),
        (Diamond, settings.DIAMOND, 1 + difficulty // 4),
        (Rock, settings.ROCK_SMALL, 2 + difficulty),
        (Rock, settings.ROCK_LARGE, 1 + difficulty // 2),
        (Bone, settings.BONE, 1 + difficulty // 2),
        (TNT, settings.TNT, min(4, difficulty // 2)),
    ]
    return LevelPlan(level_number, time_limit, goal, spawn_spec)
def populate_objects(plan):
    """Randomly place the planned objects without overlaps.
    Returns the list of live GameObject instances for the level.
    """
    objects = []
    # Playfield for objects: below the surface line, with margins.
    top = settings.CLAW_PIVOT[1] + 90
    bottom = settings.SCREEN_HEIGHT - 40
    left = 40
    right = settings.SCREEN_WIDTH - 40
    for cls, spec, count in plan.spawn_spec:
        placed = 0
        attempts = 0
        while placed < count and attempts < 400:
            attempts += 1
            radius = spec["radius"]
            x = random.uniform(left + radius, right - radius)
            y = random.uniform(top + radius, bottom - radius)
            candidate = cls(x, y, spec)
            # Keep a clear column under the miner so the first swing
            # doesn't instantly grab something at point-blank range.
            if abs(x - settings.CLAW_PIVOT[0]) < 70 and y < top + 120:
                continue
            if any(candidate.overlaps(other) for other in objects):
                continue
            objects.append(candidate)
            placed += 1
    return objects