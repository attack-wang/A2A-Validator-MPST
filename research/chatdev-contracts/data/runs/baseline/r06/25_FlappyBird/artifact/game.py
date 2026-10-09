try:
    self.sounds = init_sounds()
except pygame.error:
    self.sounds = None