        if new_best:
            if pygame.time.get_ticks() // 400 % 2 == 0:
                nb = self.medium_font.render("NEW BEST!", True, settings.NEW_BEST_COLOR)
                surface.blit(nb, nb.get_rect(center=(center_x, panel.bottom - 30)))
        else:
            hint = self.small_font.render("PRESS SPACE TO RETRY", True, settings.TEXT_MUTED)
            surface.blit(hint, hint.get_rect(center=(center_x, panel.bottom - 28)))