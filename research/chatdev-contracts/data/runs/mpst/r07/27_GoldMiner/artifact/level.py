'''
level.py
Procedural level generation for the Gold Miner game. Difficulty ascends
with the level number: more objects, more obstacles (rocks, TNT) and
tighter time limits.
'''
import random
import settings
from objects import Gold, Rock, Diamond, Bone, TNT, MysteryBag
def level_time_limit(level):
    return max(settings.MIN_LEVEL_TIME,
               settings.LEVEL_START_TIME - (level - 1) * settings.LEVEL_TIME_DECREMENT)
def level_target(level):
    '''Cumulative total score required to finish level `level`.'''
    return settings.BASE_TARGET + (level - 1) * settings.TARGET_INCREMENT
def generate_objects(level):
    '''Return the list of GameObjects for the given level.'''
    objects = []
    # counts scale with level
    gold_counts = {'small': 3 + level // 2,
                   'medium': 2 + level // 2,
                   'large': 1 + (level + 1) // 3}
    rock_count = 1 + level // 2
    diamond_count = 1 if level >= 2 else 0  # diamonds appear from level 2
    bone_count = max(0, 2 - level // 3)
    tnt_count = min(4, level // 2)
    mystery_count = 1 + level // 3
    # Build a spawn list of (factory, count)
    spawn_plan = []
    for size, count in gold_counts.items():
        spawn_plan.append((lambda x, y, s=size: Gold(x, y, s), count))
    for size, count in ... rocks
    ...