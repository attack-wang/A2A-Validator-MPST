class Skull(GameObject):
    """A creepy skull: small value, moderate weight."""
    def __init__(self, x, y):
        spec = config.SKULL
        super().__init__(x, y, spec["name"], spec["value"], spec["weight"],
                         spec["radius"], config.COLOR_BONE, "skull")
    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.radius
        pygame.draw.circle(surface, self.color, (cx, cy - r // 4), r)  # cranium
        jaw = pygame.Rect(cx - r // 2, cy + r // 2, r, r // 2)
        pygame.draw.rect(surface, self.color, jaw)
        # eyes
        pygame.draw.circle(surface, (40, 40, 40), (cx - r // 3, cy - r // 4), max(2, r // 5))
        pygame.draw.circle(surface, (40, 40, 40), (cx + r // 3, cy - r // 4), max(2, r // 5))
        # nose
        pygame.draw.circle(surface, (40, 40, 40), (cx, cy + r // 8), max(1, r // 8))
        # teeth lines
        for i in range(-1, 2):
            pygame.draw.line(surface, (120, 110, 90),
                             (cx + i * r // 4, cy + r // 2),
                             (cx + i * r // 4, cy + r), 1)