    # ----------------------------- drawing ----------------------------
    def _update_screen(self):
        '''Redraw everything and flip to the new frame.'''
        self.screen.fill(self.settings.bg_color)
        if self.stats.game_active:
            for bullet in self.player_bullets.sprites():
                bullet.draw(self.screen)
            for bullet in self.alien_bullets.sprites():
                bullet.draw(self.screen)
            self.aliens.draw(self.screen)
            self.ship.blitme()
        else:
            self._draw_message()
        self.scoreboard.draw()
        pygame.display.flip()
    def _draw_message(self):
        '''Show the start screen, game-over or victory message.'''
        if self.stats.game_won:
            title, color = "YOU WIN!", (0, 255, 90)
        elif self.stats.game_over:
            title, color = "GAME OVER", (255, 80, 80)
        else:
            title, color = "SPACE INVADERS", (0, 220, 255)
        center_x = self.settings.screen_width // 2
        center_y = self.settings.screen_height // 2
        title_image = self.title_font.render(title, True, color)
        title_rect = title_image.get_rect(center=(center_x, center_y - 40))
        self.screen.blit(title_image, title_rect)
        prompt_image = self.text_font.render(
            "Press SPACE to play", True, (230, 230, 230))
        prompt_rect = prompt_image.get_rect(center=(center_x, center_y + 20))
        self.screen.blit(prompt_image, prompt_rect)
        if not self.stats.game_over and not self.stats.game_won:
            controls_image = self.text_font.render(
                "Move: LEFT / RIGHT arrows   Fire: SPACE   Quit: Q",
                True, (160, 160, 180))
            controls_rect = controls_image.get_rect(
                center=(center_x, center_y + 60))
            self.screen.blit(controls_image, controls_rect)
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()