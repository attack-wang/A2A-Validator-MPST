class TNT(GameObject):
    def __init__(self, x, y):
        spec = OBJECT_TYPES['tnt']
        super().__init__('tnt', x, y, spec['radius'], spec['value'], spec['reel_time'])
    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.radius
        rect = pygame.Rect(cx - r, cy - r, 2 * r, 2 * r)
        pygame.draw.rect(surface, COLOR_TNT, rect, border_radius=3)
        pygame.draw.rect(surface, (120, 20, 20), rect, 2, border_radius=3)
        # white band with TNT text
        band = pygame.Rect(cx - r, cy - r // 3, 2 * r, max(8, r))
        pygame.draw.rect(surface, COLOR_WHITE, band)
        # fuse
        pygame.draw.line(surface, (80, 60, 30), (cx, cy - r), (cx + 4, cy - r - 6), 2)
        pygame.draw.circle(surface, (255, 160, 40), (cx + 4, cy - r - 7), 3)