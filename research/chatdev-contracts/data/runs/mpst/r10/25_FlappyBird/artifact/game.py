    # ------------------------------------------------------------------ #
    # Input
    # ------------------------------------------------------------------ #
    def _handle_events(self):
        """Process quit, flap and restart input from keyboard/mouse."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    self._primary_action()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._primary_action()
    def _primary_action(self):
        """Flap / start / restart depending on the current state."""
        if self.state == READY:
            self.state = PLAYING
            self.bird.flap()
        elif self.state == PLAYING:
            self.bird.flap()
        elif self.state == GAME_OVER and self.restart_timer <= 0.0:
            self.reset()