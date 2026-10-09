class MysteryBag(GameObject):
    """A mystery sack: value is randomized when it is grabbed."""
    POSSIBLE_VALUES = (50, 100, 250, 500, 800)
    def __init__(self, x, y):
        spec = config.MYSTERY_BAG
        super().__init__(x, y, spec["name"], spec["value"], spec["weight"],
                         spec["radius"], config.COLOR_BAG, "mystery")
    def randomize_value(self):
        self.value = random.choice(self.POSSIBLE_VALUES)
    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.radius
        # sack body
        pygame.draw.circle(surface, self.color, (cx, cy + r // 4), r)
        # tied neck
        pygame.draw.rect(surface, (110, 65, 28),
                         (cx - r // 3, cy - r, r * 2 // 3, r // 2))
        pygame.draw.line(surface, (90, 50, 20), (cx - r // 3, cy - r + r // 4),
                         (cx + r // 3, cy - r + r // 4), 2)
        # question mark
        font = _get_font(max(12, r))
        img = font.render("?", True, (255, 240, 200))
        surface.blit(img, img.get_rect(center=(cx, cy + r // 4)))