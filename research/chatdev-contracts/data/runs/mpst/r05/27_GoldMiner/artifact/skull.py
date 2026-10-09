class Skull(GameObject):
    """Worthless and light — grabbing it wastes a swing."""
    def __init__(self, x, y):
        super().__init__(x, y, SKULL_VALUE, 0.8, 18, 'skull')
    def draw(self, surface):
        r = self.radius
        pygame.draw.circle(surface, COLOR_SKULL, (int(self.x), int(self.y)), r)
        pygame.draw.circle(surface, COLOR_SKULL_DARK, (int(self.x), int(self.y)), r, 2)
        # eyes
        pygame.draw.circle(surface, COLOR_TEXT, (int(self.x - r*0.35), int(self.y - r*0.15)), int(r*0.28))
        pygame.draw.circle(surface, COLOR_TEXT, (int(self.x + r*0.35), int(self.y - r*0.15)), int(r*0.28))
        # nose / teeth
        pygame.draw.rect(surface, COLOR_SKULL_DARK, (self.x - r*0.3, self.y + r*0.45, r*0.6, r*0.25))