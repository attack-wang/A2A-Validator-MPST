"""Small visual effects such as explosions."""
class Explosion:
    """A short-lived expanding ring shown when something is destroyed."""
    def __init__(self, center, color, max_radius=28, duration=0.3):
        self.center = tuple(center)
        self.color = color
        self.max_radius = max_radius
        self.duration = duration
        self.timer = 0.0
    @property
    def finished(self):
        return self.timer >= self.duration
    @property
    def progress(self):
        return min(1.0, self.timer / self.duration)
    @property
    def radius(self):
        return int(self.max_radius * self.progress)
    def update(self, dt):
        self.timer += dt