class Alien:
    def __init__(self, alien_type, color, points, x, y):
        self.type = alien_type
        self.color = color
        self.points = points
        self.images = [render_bitmap(frame, color, settings.ALIEN_PIXEL) for frame in ALIEN_FRAMES[alien_type]]
        self.image_index = 0
        self.rect = self.images[0].get_rect()
        self.rect.topleft = (x, y)
        self.alive = True
    def update_position(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    def animate(self):
        self.image_index = (self.image_index + 1) % len(self.images)
    @property
    def image(self):
        return self.images[self.image_index]
    def draw(self, surface):
        surface.blit(self.image, self.rect)