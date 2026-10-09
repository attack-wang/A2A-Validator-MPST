def draw(self):
    self.background.draw(self.screen)
    for p in self.pipes:
        p.draw(self.screen)
    self.bird.draw(self.screen)
    if self.state == MENU:
        self._draw_menu()
    elif self.state == PLAYING:
        self._draw_hud()
    elif self.state == GAME_OVER:
        self._draw_hud()
        self._draw_game_over()
    if self.flash_timer > 0:
        flash = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        flash.fill((255, 255, 255))
        flash.set_alpha(int(self.flash_timer * 160))
        self.screen.blit(flash, (0, 0))
    pygame.display.flip()