class TNT(GameObject):
    """Explosive barrel: grabbing it destroys nearby objects!"""
    def __init__(self, x, y):
        spec = config.TNT
        super().__init__(x, y, spec["name"], spec["value"], spec["weight"],
                         spec["radius"], config.COLOR_TNT, "tnt")
    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.radius
        rect = pygame.Rect(cx - r, cy - r, r * 2, r * 2)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (120, 20, 20), rect, 2)
        pygame.draw.line(surface, (120, 20, 20), (cx - r, cy), (cx + r, cy), 2)
        font = _get_font(max(10, r - 4))
        img = font.render("TNT", True, (255, 255, 255))
        surface.blit(img, img.get_rect(center=(cx, cy)))
        # fuse
        pygame.draw.line(surface, (80, 60, 30), (cx, cy - r), (cx + r // 2, cy - r - r // 2), 2)