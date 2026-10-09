'''Candy entity: type, grid position, animated pixel position, fall/clear state.'''
import math
import random
import pygame
import config
class Candy:
    """A single candy on the board with grid coordinates and animation state."""
    def __init__(self, type_index, row, col):
        self.type = type_index
        self.row = row
        self.col = col
        self.x, self.y = self._cell_to_pixel(row, col)
        self.target_x, self.target_y = self.x, self.y
        self.falling = False
        self.vy = 0.0
        self.moving = False
        self.move_speed = 0.0
        self.clearing = False
        self.clear_timer = 0.0
        self.scale = 1.0
        self.wobble = random.random() * math.tau  # idle bobbing phase
    # ------------------------------------------------------------------ #
    def _cell_to_pixel(self, row, col):
        """Convert grid coordinates to the top-left pixel position on screen."""
        return (config.BOARD_X + col * config.CELL_SIZE,
                config.BOARD_Y + row * config.CELL_SIZE)
    def start_fall(self, target_row):
        """Begin an accelerated gravity fall toward target_row."""
        self.row = target_row
        self.target_x, self.target_y = self._cell_to_pixel(target_row, self.col)
        self.falling = True
        self.vy = 0.0
    def start_move(self, target_row, target_col, duration):
        """Begin a linear move (used for swap animations)."""
        self.row = target_row
        self.col = target_col
        self.target_x, self.target_y = self._cell_to_pixel(target_row, target_col)
        distance = math.hypot(self.target_x - self.x, self.target_y - self.y)
        self.move_speed = distance / duration if duration > 0 else 0.0
        self.moving = True
    def is_animating(self):
        """Return True while the candy is falling, moving or clearing."""
        return self.falling or self.moving or self.clearing
    def update(self, dt):
        """Advance fall/move/clear animation; return True while still animating."""
        if self.falling:
            self.vy += config.FALL_ACCELERATION * dt
            self.y += self.vy * dt
            if self.y >= self.target_y:
                self.y = self.target_y
                self.vy = 0.0
                self.falling = False
        if self.moving:
            self._step_towards(dt)
        if self.clearing:
            self.clear_timer += dt
            self.scale = max(0.0, 1.0 - self.clear_timer / config.CLEAR_DURATION)
        return self.is_animating()
    def _step_towards(self, dt):
        """Move one linear step toward the target pixel position."""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        step = self.move_speed * dt
        dist = math.hypot(dx, dy)
        if dist <= step:
            self.x, self.y = self.target_x, self.target_y
            self.moving = False
        else:
            self.x += dx / dist * step
            self.y += dy / dist * step
    # ------------------------------------------------------------------ #
    def _shape_points(self, cx, cy, radius):
        """Return polygon points for this candy's shape, or None for circles."""
        shape = config.CANDY_TYPES[self.type]["shape"]
        if shape == "circle":
            return None
        if shape == "square":
            half = radius * 0.82
            return [(cx - half, cy - half), (cx + half, cy - half),
                    (cx + half, cy + half), (cx - half, cy + half)]
        if shape == "diamond":
            return [(cx, cy - radius), (cx + radius, cy),
                    (cx, cy + radius), (cx - radius, cy)]
        if shape == "hexagon":
            return [(cx + radius * math.cos(math.pi / 3 * i - math.pi / 6),
                     cy + radius * math.sin(math.pi / 3 * i - math.pi / 6))
                    for i in range(6)]
        if shape == "triangle":
            return [(cx + radius * math.cos(math.pi * 2 / 3 * i - math.pi / 2),
                     cy + radius * math.sin(math.pi * 2 / 3 * i - math.pi / 2))
                    for i in range(3)]
        if shape == "star":
            points = []
            for i in range(10):
                angle = math.pi / 5 * i - math.pi / 2
                r = radius if i % 2 == 0 else radius * 0.45
                points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
            return points
        return None
    def draw(self, surface):
        """Render the candy with depth shading, highlight and animations."""
        info = config.CANDY_TYPES[self.type]
        size = config.CELL_SIZE
        cx = self.x + size / 2
        cy = self.y + size / 2
        # idle bobbing (suppressed while falling/moving/clearing)
        if not (self.falling or self.moving or self.clearing):
            cy += math.sin(pygame.time.get_ticks() * 0.003 + self.wobble) * 2.0
        radius = size * 0.36 * self.scale
        if radius <= 0.5:
            return
        points = self._shape_points(cx, cy, radius)
        if points is None:
            pygame.draw.circle(surface, info["dark"], (int(cx) + 3, int(cy) + 3), int(radius))
            pygame.draw.circle(surface, info["color"], (int(cx), int(cy)), int(radius))
            pygame.draw.circle(surface, info["dark"], (int(cx), int(cy)), int(radius), 2)
            shine = (int(cx - radius * 0.3), int(cy - radius * 0.3))
            pygame.draw.circle(surface, (255, 255, 255), shine, max(1, int(radius * 0.18)))
        else:
            shadow = [(px + 3, py + 3) for px, py in points]
            pygame.draw.polygon(surface, info["dark"], shadow)
            pygame.draw.polygon(surface, info["color"], points)
            pygame.draw.polygon(surface, info["dark"], points, 2)
            shine = (int(cx - radius * 0.3), int(cy - radius * 0.3))
            pygame.draw.circle(surface, (255, 255, 255), shine, max(1, int(radius * 0.15)))