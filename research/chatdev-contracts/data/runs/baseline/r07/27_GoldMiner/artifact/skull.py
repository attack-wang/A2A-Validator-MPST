class Skull(GameObject):
    """Worthless hazard that wastes time when grabbed."""
    def __init__(self, x, y):
        super().__init__(x, y, 0, 2.5, 16, 'skull')
    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        pygame.draw.circle(surface, SKULL_COLOR, (cx, cy - 3), self.radius)
        pygame.draw.rect(surface, SKULL_COLOR, (cx - self.radius // 2, cy + 4, self.radius, self.radius // 2), border_radius=4)
        pygame.draw.circle(surface, BLACK, (cx - 6, cy - 5), 4)
        pygame.draw.circle(surface, BLACK, (cx + 6, cy - 5), 4)
        pygame.draw.circle(surface, BLACK, (cx, cy + 6), 3)