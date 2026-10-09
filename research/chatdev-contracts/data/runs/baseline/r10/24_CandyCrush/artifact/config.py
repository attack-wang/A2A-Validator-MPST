"""Candy entity with grid position, animated pixel position and per-state animation."""
import pygame
from config import (CELL_SIZE, BOARD_LEFT, BOARD_TOP, SWAP_DURATION,
                    CLEAR_DURATION, FALL_GRAVITY, FALL_MAX_SPEED)
from graphics import get_candy_image
def pixel_pos(row, col):
    """Center pixel coordinates of the cell at (row, col)."""
    return (BOARD_LEFT + col * CELL_SIZE + CELL_SIZE // 2,
            BOARD_TOP + row * CELL_SIZE + CELL_SIZE // 2)
class Candy:
    """A single candy: logical grid cell + animated on-screen position."""
    IDLE, SWAPPING, FALLING, CLEARING = 'idle', 'swapping', 'falling', 'clearing'
    def __init__(self, type_id, row, col):
        self.type = type_id
        self.row = row
        self.col = col
        self.px, self.py = pixel_pos(row, col)
        self.state = Candy.IDLE
        self.anim_time = 0.0
        self.anim_duration = 0.0
        self.start_px, self.start_py = self.px, self.py
        self.target_px, self.target_py = self.px, self.py
        self.fall_velocity = 0.0
        self.scale = 1.0
        self.alpha = 255
        self.dead = False
    # ----- animation starters -------------------------------------------
    def start_swap(self, row, col):
        """Animate from current pixel pos to the new grid cell."""
        self.row, self.col = row, col
        self.state = Candy.SWAPPING
        self.anim_time = 0.0
        self.anim_duration = SWAP_DURATION
        self.start_px, self.start_py = self.px, self.py
        self.target_px, self.target_py = pixel_pos(row, col)
    def start_fall(self, row, col):
        """Gravity fall to the new grid cell (may start above the board)."""
        self.row, self.col = row, col
        self.state = Candy.FALLING
        self.start_px, self.start_py = self.px, self.py
        self.target_px, self.target_py = pixel_pos(row, col)
        self.fall_velocity = 0.0
    def start_clear(self):
        """Shrink + fade-out animation."""
        self.state = Candy.CLEARING
        self.anim_time = 0.0
        self.anim_duration = CLEAR_DURATION
    # ----- per-frame update ---------------------------------------------
    def update(self, dt):
        if self.state == Candy.SWAPPING:
            self.anim_time += dt
            t = min(self.anim_time / self.anim_duration, 1.0)
            t = t * t * (3 - 2 * t)  # smoothstep easing
            self.px = self.start_px + (self.target_px - self.start_px) * t
            self.py = self.start_py + (self.target_py - self.start_py) * t
            if self.anim_time >= self.anim_duration:
                self.px, self.py = self.target_px, self.target_py
                self.state = Candy.IDLE
        elif self.state == Candy.FALLING:
            self.fall_velocity = min(self.fall_velocity + FALL_GRAVITY * dt,
                                     FALL_MAX_SPEED)
            self.py += self.fall_velocity * dt
            if self.py >= self.target_py:
                self.py = self.target_py
                self.px = self.target_px
                self.state = Candy.IDLE
        elif self.state == Candy.CLEARING:
            self.anim_time += dt
            t = min(self.anim_time / self.anim_duration, 1.0)
            self.scale = 1.0 - t
            self.alpha = int(255 * (1.0 - t))
            if self.anim_time >= self.anim_duration:
                self.dead = True
    @property
    def animating(self):
        """True while the candy still plays an animation."""
        return self.state != Candy.IDLE
    def draw(self, surface):
        img = get_candy_image(self.type)
        if self.scale != 1.0:
            w = max(1, int(img.get_width() * self.scale))
            h = max(1, int(img.get_height() * self.scale))
            img = pygame.transform.smoothscale(img, (w, h))
        if self.alpha < 255:
            img = img.copy()
            img.set_alpha(self.alpha)
        rect = img.get_rect(center=(int(self.px), int(self.py)))
        surface.blit(img, rect)