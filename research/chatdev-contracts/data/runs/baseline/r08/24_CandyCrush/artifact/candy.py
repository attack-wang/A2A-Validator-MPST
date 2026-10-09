'''Candy module: defines the Candy entity with type-based shape/color and animation state.'''
import math
import pygame
import config
class Candy:
    """A single candy on the board with center-based coordinates and animation state."""
    def __init__(self, candy_type, row, col):
        self.type = candy_type
        self.row = row
        self.col = col
        self.x = config.BOARD_X + col * config.CELL_SIZE + config.CELL_SIZE // 2
        self.y = config.BOARD_Y + row * config.CELL_SIZE + config.CELL_SIZE // 2
        self.scale = 1.0
        self.clearing = False
        self.clear_timer = 0.0
        self.fall_speed = 0.0
        self.selected = False
    @property
    def target_x(self):
        return config.BOARD_X + self.col * config.CELL_SIZE + config.CELL_SIZE // 2
    @property
    def target_y(self):
        return config.BOARD_Y + self.row * config.CELL_SIZE + config.CELL_SIZE // 2
    @property
    def is_at_target(self):
        return (abs(self.x - self.target_x) < 0.5 and
                abs(self.y - self.target_y) < 0.5)
    def move_towards_target(self, speed, dt):
        """Advance x/y toward target by speed*dt; return True when arrived."""
        arrived = True
        tx, ty = self.target_x, self.target_y
        dx = tx - self.x
        dy = ty - self.y
        step = speed * dt
        if abs(dx) > step:
            self.x += step if dx > 0 else -step
            arrived = False
        else:
            self.x = tx
        if abs(dy) > step:
            self.y += step if dy > 0 else -step
            arrived = False
        else:
            self.y = ty
        return arrived
    def start_clearing(self):
        self.clearing = True
        self.clear_timer = 0.0
    def update_clear(self, dt):
        """Progress clearing animation; return True when finished."""
        self.clear_timer += dt
        progress = min(1.0, self.clear_timer / config.CLEAR_DURATION)
        self.scale = 1.0 - progress
        return progress >= 1.0
    def draw(self, surface):
        info = config.CANDY_TYPES[self.type]
        radius = max(1, int((config.CELL_SIZE // 2 - 6) * self.scale))
        cx, cy = int(self.x), int(self.y)
        if radius <= 1:
            return
        shape = info["shape"]
        color = info["color"]
        dark = info["dark"]
        rect = pygame.Rect(cx - radius, cy - radius, radius * 2, radius * 2)
        if shape == "circle":
            pygame.draw.circle(surface, color, (cx, cy), radius)
            pygame.draw.circle(surface, dark, (cx, cy), radius, 3)
            highlight = (cx - radius // 3, cy - radius // 3)
            pygame.draw.circle(surface, (255, 255, 255), highlight, max(1, radius // 4))
        elif shape == "square":
            pygame.draw.rect(surface, color, rect, border_radius=radius // 2)
            pygame.draw.rect(surface, dark, rect, 3, border_radius=radius // 2)
        elif shape == "diamond":
            pts = [(cx, cy - radius), (cx + radius, cy), (cx, cy + radius), (cx - radius, cy)]
            pygame.draw.polygon(surface, color, pts)
            pygame.draw.polygon(surface, dark, pts, 3)
        elif shape == "triangle":
            pts = [(cx, cy - radius), (cx + radius, cy + radius), (cx - radius, cy + radius)]
            pygame.draw.polygon(surface, color, pts)
            pygame.draw.polygon(surface, dark, pts, 3)
        elif shape == "hexagon":
            pts = []
            for i in range(6):
                ang = math.pi / 3 * i - math.pi / 6
                pts.append((cx + radius * math.cos(ang), cy + radius * math.sin(ang)))
            pygame.draw.polygon(surface, color, pts)
            pygame.draw.polygon(surface, dark, pts, 3)
        else:  # oval
            oval_rect = pygame.Rect(cx - radius, cy - int(radius * 0.75), radius * 2, int(radius * 1.5))
            pygame.draw.ellipse(surface, color, oval_rect)
            pygame.draw.ellipse(surface, dark, oval_rect, 3)
        if self.selected:
            pygame.draw.rect(surface, config.SELECTED_COLOR, rect.inflate(10, 10), 3, border_radius=8)