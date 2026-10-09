class MysteryBag(GameObject):
    """Surprise sack: random value revealed when delivered."""
    def __init__(self, x, y, level=1):
        super().__init__(x, y, MYSTERY_MIN, 1.5, 20, 'mystery bag')
        self.level = level
    def roll_value(self):
        """Roll the random value once, when the bag is delivered."""
        self.value = random.randint(MYSTERY_MIN, MYSTERY_MAX)
        return self.value
    def draw(self, surface):
        r = self.radius
        # sack body
        pts = [(self.x - r*0.8, self.y + r*0.7), (self.x - r*0.6, self.y - r*0.4),
               (self.x, self.y - r), (self.x + r*0.6, self.y - r*0.4),
               (self.x + r*0.8, self.y + r*0.7)]
        pygame.draw.polygon(surface, COLOR_MYSTERY, pts)
        pygame.draw.polygon(surface, COLOR_MYSTERY_DARK, pts, 3)
        # question mark
        font = _get_font(14)
        label = font.render("?", True, COLOR_WHITE)
        surface.blit(label, label.get_rect(center=(self.x, self.y + 2)))