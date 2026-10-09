"""Level generation: object layouts, targets and time limits per level."""
import math
import random
from objects import Gold, Rock, Diamond, TNT, Bone, MysteryBag
from settings import *
def level_config(n):
    """Return dict describing difficulty parameters for level n (1-indexed)."""
    target = BASE_TARGET + (n - 1) * TARGET_STEP
    time_limit = max(MIN_TIME, BASE_TIME - (n - 1) * TIME_PER_LEVEL)
    swing_speed = min(MAX_SWING, BASE_SWING + (n - 1) * SWING_STEP)
    return {
        'target': target,
        'time_limit': time_limit,
        'swing_speed': swing_speed,
    }
def generate_objects(n):
    """Create the object layout for level n with non-overlapping placement."""
    count = min(MAX_OBJECTS, BASE_OBJECTS + (n - 1) * OBJECTS_PER_LEVEL)
    tnt_count = min(MAX_TNT, 1 + (n - 1) // 2)
    diamond_count = 1 + (n - 1) // 3
    objects = []
    # candidate x bands across the pit, y bands by depth
    placed = []
    max_attempts = 400
    def try_place(make_obj, radius):
        for _ in range(max_attempts):
            x = random.uniform(40, WIDTH - 40)
            y = random.uniform(GROUND_Y + 90, HEIGHT - 40)
            ok = True
            for (ox, oy, orad) in placed:
                if math.hypot(x - ox, y - oy) < radius + orad + 14:
                    ok = False
                    break
            if ok:
                obj = make_obj(x, y)
                objects.append(obj)
                placed.append((x, y, radius))
                return True
        return False
    # TNT first (guaranteed hazards), then diamonds, then gold, rocks, bones, bags
    for _ in range(tnt_count):
        try_place(lambda x, y: TNT(x, y), 16)
    for _ in range(diamond_count):
        try_place(lambda x, y: Diamond(x, y), 14)
    remaining = count - len(objects)
    gold_sizes = ['small', 'medium', 'large']
    for _ in range(remaining):
        roll = random.random()
        if roll < 0.45:
            size = random.choices(gold_sizes, weights=[0.4, 0.4, 0.2])[0]
            radius = Gold.SIZES[size]['radius']
            try_place(lambda x, y: Gold(x, y, size), radius)
        elif roll < 0.70:
            size = random.choice(['small', 'large'])
            radius = Rock.SIZES[size]['radius']
            try_place(lambda x, y: Rock(x, y, size), radius)
        elif roll < 0.85:
            try_place(lambda x, y: MysteryBag(x, y), 15)
        else:
            try_place(lambda x, y: Bone(x, y), 12)
    return objects