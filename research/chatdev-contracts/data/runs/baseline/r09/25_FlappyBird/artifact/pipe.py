'''
pipe.py
Defines the Pipe obstacle: random gap placement, movement,
collision and scoring helpers (tkinter edition).
'''
import random
import settings
from utils import Rect
class Pipe:
    """A vertical pipe pair with a random gap the bird must fly through."""
    def __init__(self, x, gap_center, gap_size, speed):
        self.x = float(x)
        self.gap_center = float(gap_center)
        self.gap_size = gap_size
        self.speed = speed
        self.scored = False
        self.width = settings.PIPE_WIDTH
        play_bottom = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        self.gap_top = max(0.0, self.gap_center - gap_size / 2)
        self.gap_bottom = min(play_bottom, self.gap_center + gap_size / 2)
    def update(self, dt):
        self.x -= self.speed * dt
    def offscreen(self):
        return self.x + self.width < -10
    def get_top_rect(self):
        return Rect(int(self.x), 0, self.width, int(self.gap_top))
    def get_bottom_rect(self):
        play_bottom = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        return Rect(int(self.x), int(self.gap_bottom), self.width,
                    play_bottom - int(self.gap_bottom))
    def collides(self, rect):
        return rect.colliderect(self.get_top_rect()) or rect.colliderect(self.get_bottom_rect())
    def has_passed(self, bird_x):
        return not self.scored and bird_x > self.x + self.width
    def mark_scored(self):
        self.scored = True
    def draw(self, canvas):
        """Render top and bottom pipe bodies with caps and shading."""
        for item in self.canvas_ids:
            canvas.delete(item)
        self.canvas_ids = []
        cap_h = 26
        cap_overhang = 6
        ...