class MysteryBag(GameObject):
    '''A dusty sack — its contents (and value) are revealed on collection.'''
    def __init__(self, kind, x=None, y=None):
        super().__init__(kind, x, y)
        self.value = random.choice([50, 150, 500])
    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        r = self.radius
        # sack body
        pygame.draw.circle(surface, BAG_COLOR, (x, y + r // 4), r)
        # tied neck
        pygame.draw.rect(surface, BAG_COLOR, (x - r // 3, y - r, r * 2 // 3, r), border_radius=2)
        pygame.draw.line(surface, (90, 60, 30), (x - r // 2, y - r // 3), (x + r // 2, y - r // 3), 3)
        pygame.draw.circle(surface, BAG_COLOR, (x, y - r), r // 3)
        # question mark
        font = _get_font(max(16, r))
        label = font.render("?", True, WHITE)
        surface.blit(label, label.get_rect(center=(x, y + r // 4)))