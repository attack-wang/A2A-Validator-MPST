class TNT(GameObject):
    """Explosive barrel: grabbing it destroys it and nearby objects and costs points."""
    def __init__(self, x, y):
        super().__init__(x, y, -TNT_PENALTY, 1.0, 16, 'tnt')
    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        rect = pygame.Rect(cx - 14, cy - 16, 28, 32)
        pygame.draw.rect(surface, TNT_COLOR, rect, border_radius=4)
        pygame.draw.rect(surface, (120, 20, 20), rect, 2, border_radius=4)
        pygame.draw.rect(surface, (255, 255, 255), (cx - 12, cy - 6, 24, 12))
        font = pygame.font.SysFont(None, 18)
        text = font.render("TNT", True, (180, 30, 30))
        surface.blit(text, text.get_rect(center=(cx, cy)))