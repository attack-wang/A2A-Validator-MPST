class MysteryBag(GameObject):
    """Random value bag; actual value rolled when deposited."""
    def __init__(self, x, y):
        super().__init__(x, y, 15, 0, 1.2, 'mystery')
    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        r = int(self.radius)
        pygame.draw.circle(surface, BAG_COLOR, (x, y + 2), r)
        pygame.draw.rect(surface, BAG_COLOR, (x - r // 2, y - r - 2, r, 8))
        pygame.draw.rect(surface, (80, 50, 25), (x - r // 2, y - r - 2, r, 8), 1)
        pygame.draw.circle(surface, (200, 170, 90), (x, y), 3)