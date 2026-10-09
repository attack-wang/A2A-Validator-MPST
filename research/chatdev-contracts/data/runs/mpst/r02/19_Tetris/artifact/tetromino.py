if key == pygame.K_ESCAPE:
    self.running = False
elif self.game_over:
    if key == pygame.K_r:
        self.restart()
    return
elif key == pygame.K_p:
    self.paused = not self.paused
if self.paused or self.game_over:
    return