    def draw_overlay(self, surface, title, lines, footer):
        """Dim the screen and show a centred title, info lines and a footer."""
        dim = pygame.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), pygame.SRCALPHA)
        dim.fill((10, 10, 20, 180))
        surface.blit(dim, (0, 0))
        title_surf = self.font_big.render(title, True, S.GOLD_COLOR)
        surface.blit(title_surf, (S.SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 200))
        y = 270
        for line in lines:
            surf = self.font.render(line, True, S.HUD_TEXT)
            surface.blit(surf, (S.SCREEN_WIDTH // 2 - surf.get_width() // 2, y))
            y += 32
        foot = self.font_small.render(footer, True, S.MESSAGE_INFO)
        surface.blit(foot, (S.SCREEN_WIDTH // 2 - foot.get_width() // 2, S.SCREEN_HEIGHT - 90))