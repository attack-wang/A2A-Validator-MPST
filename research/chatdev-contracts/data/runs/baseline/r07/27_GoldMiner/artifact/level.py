'''Level generation with ascending difficulty: richer gold, more hazards, tighter time.'''
import math
import random
from settings import *
from objects import Gold, Diamond, Rock, Skull, TNT
class Level:
    """Builds the object field and difficulty parameters for one level."""
    def __init__(self, number):
        self.number = number
        self.goal = BASE_GOAL + (number - 1) * GOAL_INCREMENT
        self.time_limit = max(BASE_TIME - (number - 1) * TIME_DECREMENT, MIN_TIME)
        self.objects = []
        self.generate()
    def generate(self):
        n = self.number
        # --- object budget scales with level ---
        golds = [('small', 4 + n // 2), ('medium', 2 + n // 3), ('large', 1 + (n - 1) // 3)]
        rocks = [('small', 2 + n // 2), ('large', 1 + (n - 1) // 2)]
        skulls = 1 + n // 2
        tnts = 1 if n >= 2 else 0
        diamonds = 1 if n >= 3 else 0
        plan = []
        for size, count in golds:
            plan.extend([('gold', size)] * count)
        for size, count in rocks:
            plan.extend([('rock', size)] * count)
        plan.extend([('skull', None)] * skulls)
        plan.extend([('tnt', None)] * tnts)
        plan.extend([('diamond', None)] * diamonds)
        random.shuffle(plan)
        for kind, size in plan:
            self._place(kind, size)
    def _place(self, kind, size):
        """Try to find a non-overlapping spot inside the dirt field."""
        for _ in range(200):
            x = random.uniform(FIELD_LEFT + 30, FIELD_RIGHT - 30)
            y = random.uniform(FIELD_TOP + 20, FIELD_BOTTOM - 20)
            if kind == 'gold':
                obj = Gold(x, y, size)
            elif kind == 'rock':
                obj = Rock(x, y, size)
            elif kind == 'skull':
                obj = Skull(x, y)
            elif kind == 'tnt':
                obj = TNT(x, y)
            else:
                obj = Diamond(x, y)
            ok = True
            for other in self.objects:
                dist = math.hypot(obj.x - other.x, obj.y - other.y)
                if dist < obj.radius + other.radius + 12:
                    ok = False
                    break
            if ok:
                self.objects.append(obj)
                return
        # fallback: place anyway (rare)
        self.objects.append(obj)