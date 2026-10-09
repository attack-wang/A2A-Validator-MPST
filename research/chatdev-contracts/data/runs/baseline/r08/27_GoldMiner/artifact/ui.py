def draw_hud(self, surface, game):
    pygame.draw.rect(surface, settings.COLOR_PANEL, (0, 0, settings.SCREEN_WIDTH, 44))
    texts = [
        self.font_small.render(f"Gold: {game.level_score} / {game.goal}", True, settings.COLOR_TEXT_GOLD),
        self.font_small.render(f"Level {game.level_number}", True, settings.COLOR_TEXT),
        self.font_small.render(f"Time: {int(game.time_left)}", True, time_color),
        self.font_small.render(f"Total: {game.total_score}", True, settings.COLOR_TEXT),
    ]
    # Lay out left to right with fixed gaps, right-aligning the last item.
    x = 16
    for i, t in enumerate(texts):
        surface.blit(t, (x, 12))
        x += t.get_width() + 30