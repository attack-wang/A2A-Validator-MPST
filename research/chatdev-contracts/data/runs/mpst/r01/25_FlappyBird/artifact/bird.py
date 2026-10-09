"""Bird entity: physics, animation, and rendering for the player character."""
import pygame
import settings
class Bird:
    """The player-controlled bird with gravity physics and flap mechanics."""
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.wing_frame = 0
        self.wing_timer = 0.0
        self._build_sprites()
    def _build_sprites(self):
        """Pre-render the bird's animation frames (body, wing, eye, beak)."""
        self.frames = []
        for wing_offset in (-4, 0, 4):
            frame = pygame.Surface((settings.BIRD_WIDTH, settings.BIRD_HEIGHT), pygame.SRCALPHA)
            pygame.draw.ellipse(frame, settings.YELLOW, (0, 2, 30, 20))
            pygame.draw.ellipse(frame, settings.BLACK, (0, 2, 30, 20), 1)
            pygame.draw.ellipse(frame, settings.ORANGE, (6, 10 + wing_offset, 14, 8))
            pygame.draw.circle(frame, settings.WHITE, (22, 8), 4)
            pygame.draw.circle(frame, settings.BLACK, (24, 8), 2)
            pygame.draw.polygon(frame, settings.RED, [(28, 11), (34, 13), (28, 16)])
            self.frames.append(frame)
        self.rect_size = (settings.BIRD_WIDTH - 8, settings.BIRD_HEIGHT - 6)
    def flap(self):
        """Apply an upward impulse to the bird."""
        self.velocity = settings.FLAP_VELOCITY
        self.wing_timer = 0.0
        self.wing_frame = 0
    def update(self, dt):
        """Advance bird physics and animation by dt seconds."""
        self.velocity = min(self.velocity + settings.GRAVITY * dt, settings.MAX_FALL_SPEED)
        self.y += self.velocity * dt
        if self.y < 0:
            self.y = 0
            self.velocity = 0.0
        # rotation follows velocity: tilt up on flap, nose-dive when falling
        target = max(-25.0, min(90.0, self.velocity * 0.08))
        self.rotation += (target - self.rotation) * min(1.0, dt * 12)
        self.wing_timer += dt
        if self.wing_timer >= settings.WING_FLAP_INTERVAL:
            self.wing_timer = 0.0
            self.wing_frame = (self.wing_frame + 1) % 3
    def get_hitbox(self):
        """Return a slightly shrunken rect for fairer collisions."""
        w, h = self.rect_size
        return pygame.Rect(int(self.x - w / 2), int(self.y - h / 2), w, h)
    def draw(self, surface):
        """Draw the rotated bird at its current position."""
        frame = self.frames[self.wing_frame]
        rotated = pygame.transform.rotate(frame, -self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)
    def reset(self):
        """Restore the bird to its starting state."""
        self.x = float(self.start_x)
        self.y = float(self.start_y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.wing_frame = 0
        self.wing_timer = 0.0