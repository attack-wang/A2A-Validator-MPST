class TNT(GameObject):
    """A stick of dynamite: grabbing it triggers an explosion that destroys
    nearby objects and costs a score penalty."""
    def __init__(self, x, y):
        super().__init__(x, y, 'tnt', S.TNT_VALUE, S.TNT_WEIGHT, S.TNT_RADIUS)
    def draw(self, surface):
        r = self.radius
        w, h = int(r * 1.5), int(r * 2.0)
        rect = pygame.Rect(int(self.x - w / 2), int(self.y - h / 2), w, h)
        pygame.draw.rect(surface, S.TNT_COLOR, rect, border_radius=3)
        pygame.draw.rect(surface, S.TNT_DARK, rect, 2, border_radius=3)
        # fuse
        pygame.draw.line(surface, (90, 70, 40), (self.x, rect.top), (self.x + 6, rect.top - 8), 2)
        # label band
        pygame.draw.line(surface, (250, 240, 210), (rect.left + 3, self.y - 2), (rect.right - 3, self.y - 2), 3)