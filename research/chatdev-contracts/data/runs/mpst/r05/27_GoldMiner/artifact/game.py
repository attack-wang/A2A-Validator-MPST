            if event.type == pygame.MOUSEBUTTONDOWN and self.state == Game.STATE_PLAYING:
                self.claw.launch()