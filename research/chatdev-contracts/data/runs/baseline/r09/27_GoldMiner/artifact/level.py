class Level:
    def __init__(self, number):
        self.number = number
        self.objects = []
        self.generate()
        self.total_value = sum(o.value for o in self.objects if o.kind != "tnt")
        frac = min(GOAL_MAX_FRACTION, GOAL_START_FRACTION + GOAL_FRACTION_STEP * (number - 1))
        self.goal = max(1, int(self.total_value * frac))
        self.time_limit = max(LEVEL_TIME_MIN, LEVEL_TIME_BASE - LEVEL_TIME_STEP * (number - 1))
    def remaining_value(self):
        return sum(o.value for o in self.objects if o.alive and o.kind != "tnt")
    def explode(self, tnt):
        destroyed = []
        queue = [tnt]
        tnt.alive = False
        while queue:
            t = queue.pop()
            destroyed.append(t)
            for o in self.objects:
                if o.alive and o is not t and o.distance_to(t.x, t.y) <= TNT_BLAST_RADIUS:
                    o.alive = False
                    if o.kind == "tnt":
                        queue.append(o)
        return destroyed