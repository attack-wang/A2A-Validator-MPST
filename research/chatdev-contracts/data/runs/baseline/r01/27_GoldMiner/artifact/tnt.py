class TNT(GameObject):
    """Explodes while being reeled in; destroys nearby objects and costs points."""
    def __init__(self, x, y):
        super().__init__(x, y, 16, 0, 1.0, 'tnt')
        self.fuse = None
    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        r = int(self.radius)
        body = pygame.Rect(x - r, y - r, 2 * r, 2 * r)
        pygame.draw.rect(surface, TNT_RED, body)
        pygame.draw.rect(surface, TNT_DARK, body, 2)
        pygame.draw.rect(surface, WHITE, (x - r // 2, y - 4, r, 8))
        pygame.draw.line(surface, BLACK, (x, y - r), (x, y - r - 6), 2)