class TNT(GameObject):
    '''Explosive crate: grabbing it triggers a blast (handled by the Game).'''
    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        r = self.radius
        rect = pygame.Rect(0, 0, r * 2, int(r * 1.6))
        rect.center = (x, y)
        pygame.draw.rect(surface, TNT_COLOR, rect, border_radius=3)
        pygame.draw.rect(surface, TNT_DARK, rect, 2, border_radius=3)
        # white band with TNT text
        band = pygame.Rect(rect.x, rect.centery - r // 4, rect.width, max(8, r // 2))
        pygame.draw.rect(surface, WHITE, band)
        font = _get_font(max(14, r))
        label = font.render("TNT", True, TNT_DARK)
        surface.blit(label, label.get_rect(center=(x, y)))
        # fuse
        pygame.draw.line(surface, (90, 60, 30), (x, rect.top), (x + 6, rect.top - 8), 2)