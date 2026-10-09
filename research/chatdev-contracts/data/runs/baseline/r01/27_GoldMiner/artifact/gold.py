class Gold(GameObject):
    def __init__(...):
        ...
        self.points = self._make_points()
    def _make_points(self):
        pts = []
        n = 8
        for i in range(n):
            ang = i * 2*math.pi/n
            r = self.radius * random.uniform(0.8, 1.05)
            pts.append((self.x + math.cos(ang)*r, self.y + math.sin(ang)*r))
        return pts