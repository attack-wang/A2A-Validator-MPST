class Alien(pygame.sprite.Sprite):
    """A single alien. Movement is controlled by the Fleet object."""
    def __init__(self, row, col, x, y):
        super().__init__()
        self.row = row
        self.points = settings.ALIEN_POINTS[min(row, len(settings.ALIEN_POINTS) - 1)]
        self.image = self._make_image(row)
        self.rect = self.image.get_rect(topleft=(x, y))
    @staticmethod
    def _make_image(row):
        colors = [settings.RED, settings.ORANGE, settings.YELLOW, settings.GREEN, settings.CYAN]
        color = colors[row % len(colors)]
        w, h = settings.ALIEN_WIDTH, settings.ALIEN_HEIGHT
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        # body
        pygame.draw.ellipse(surf, color, (2, 4, w - 4, h - 10))
        # eyes
        pygame.draw.circle(surf, settings.BLACK, (w // 2 - 7, h // 2), 3)
        pygame.draw.circle(surf, settings.BLACK, (w // 2 + 7, h // 2), 3)
        # legs / antennae
        pygame.draw.line(surf, color, (6, h - 6), (2, h - 1), 2)
        pygame.draw.line(surf, color, (w - 6, h - 6), (w - 2, h - 1), 2)
        return surf