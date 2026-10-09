class TNT(GameObject):
    def __init__(self, x, y):
        super().__init__("tnt", x, y)
    def on_grab(self, game):
        # explodes: destroys itself and nearby objects
        self.destroyed = True
        for other in game.level.objects:
            if other is not self and not other.destroyed:
                dist = math.hypot(other.x - self.x, other.y - self.y)
                if dist <= config.TNT_BLAST_RADIUS:
                    other.destroyed = True
        game.on_explosion(self.x, self.y)
    def draw(self, surface):
        w = self.radius * 1.6
        h = self.radius * 2.0
        rect = pygame.Rect(int(self.x - w/2), int(self.y - h/2), int(w), int(h))
        pygame.draw.rect(surface, config.COLOR_TNT, rect, border_radius=3)
        pygame.draw.rect(surface, (140, 35, 30), rect, 2, border_radius=3)
        # band
        band = pygame.Rect(rect.x, int(self.y - h*0.15), int(w), int(h*0.3))
        pygame.draw.rect(surface, (240, 220, 180), band)
        # fuse
        pygame.draw.line(surface, (90, 60, 30), (self.x, rect.top), (self.x + 6, rect.top - 8), 2)
        # label T
        font = _small_font()
        label = font.render("TNT", True, (60, 10, 10))
        surface.blit(label, (self.x - label.get_width()//2, self.y - label.get_height()//2))