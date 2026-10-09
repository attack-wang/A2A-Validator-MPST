class Rock(GameObject):
    """Worthless stone: heavy, low value — a trap for greedy players."""
    def __init__(self, x, y, level=1):
        value = int(ROCK_VALUE + level * 2)
        super().__init__(x, y, value, 5.0, 24, 'rock')
        self._make_blob(8, 0.18)
    def draw(self, surface):
        pts = [(self.x + dx, self.y + dy) for dx, dy in self.shape]
        pygame.draw.polygon(surface, COLOR_ROCK, pts)
        pygame.draw.polygon(surface, COLOR_ROCK_DARK, pts, 3)