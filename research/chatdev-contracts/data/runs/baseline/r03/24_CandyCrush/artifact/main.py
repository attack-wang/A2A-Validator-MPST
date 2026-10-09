overlay = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA)
overlay.fill((10, 10, 20, 200))
self.screen.blit(overlay, (0, 0))