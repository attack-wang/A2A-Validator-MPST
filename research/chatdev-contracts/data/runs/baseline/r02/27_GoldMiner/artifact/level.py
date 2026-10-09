'''
level.py
Procedural level generation with ascending difficulty.
'''
import random
from settings import (SCREEN_WIDTH, SCREEN_HEIGHT, MINE_TOP, MINE_MARGIN,
                      level_config)
from objects import Gold, Rock, Diamond, Bone, TNT, MysteryBag
OBJECT_CLASS_MAP = {
    'gold_small': Gold,
    'gold_medium': Gold,
    'gold_large': Gold,
    'rock_small': Rock,
    'rock_large': Rock,
    'diamond': Diamond,
    'bone': Bone,
    'tnt': TNT,
    'bag': MysteryBag,
}
def make_object(kind):
    return OBJECT_CLASS_MAP[kind](kind)
def place_objects(objects):
    '''Rejection sampling: random spots inside the mine, no overlaps.'''
    placed = []
    max_attempts = 400
    for obj in objects:
        r = obj.radius
        lo_x = MINE_MARGIN + r
        hi_x = SCREEN_WIDTH - MINE_MARGIN - r
        lo_y = MINE_TOP + r
        hi_y = SCREEN_HEIGHT - MINE_MARGIN - r
        for _ in range(max_attempts):
            x = random.uniform(lo_x, hi_x)
            y = random.uniform(lo_y, hi_y)
            ok = True
            for other in placed:
                dx = x - other.x
                dy = y - other.y
                if math.hypot(dx, dy) < (r + other.radius) * 1.15:
                    ok = False
                    break
            if ok:
                obj.x, obj.y = x, y
                placed.append(obj)
                break
        else:
            # fallback: shrink spacing requirement and force a spot
            ...