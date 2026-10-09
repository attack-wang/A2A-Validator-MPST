import pygame
from constants import CANDY_COLORS, NUM_CANDY_TYPES
class Candy:
    def __init__(self, candy_type):
        if not 0 <= candy_type < NUM_CANDY_TYPES:
            raise ValueError(f"candy_type must be in [0, {NUM_CANDY_TYPES}), got {candy_type}")
        self.type = candy_type
        self.fall_offset = 0.0
        self.clear_progress = -1.0
    @property
    def color(self):
        return CANDY_COLORS[self.type]
    def is_clearing(self):
        return self.clear_progress >= 0.0
    def draw(self, surface, cx, cy, cell_size, scale=1.0):
        radius = cell_size * 0.38 * scale
        if radius <= 1:
            return
        color = self.color
        shape = self.type
        if shape == 0:  # red circle
            pygame.draw.circle(surface, color, (int(cx), int(cy)), int(radius))
            self._draw_gloss(surface, cx, cy, radius)
        elif shape == 1:  # orange rounded square
            rect = pygame.Rect(0, 0, int(radius*1.8), int(radius*1.8))
            rect.center = (int(cx), int(cy))
            pygame.draw.rect(surface, color, rect, border_radius=int(radius*0.4))
            self._draw_gloss(surface, cx, cy, radius)
        elif shape == 2:  # yellow diamond
            points = [(cx, cy - radius), (cx + radius, cy), (cx, cy + radius), (cx - radius, cy)]
            pygame.draw.polygon(surface, color, points)
            self._draw_gloss(surface, cx, cy, radius)
        elif shape == 3:  # green hexagon
            points = []
            for i in range(6):
                ang = math.pi / 3 * i - math.pi / 6
                points.append((cx + radius * math.cos(ang), cy + radius * math.sin(ang)))
            pygame.draw.polygon(surface, color, points)
            self._draw_gloss(surface, cx, cy, radius)
        elif shape == 4:  # blue capsule/oval
            rect = pygame.Rect(0, 0, int(radius*1.7), int(radius*1.1))
            rect.center = (int(cx), int(cy))
            pygame.draw.ellipse(surface, color, rect)
            self._draw_gloss(surface, cx, cy, radius)
        else:  # purple triangle
            points = [(cx, cy - radius), (cx + radius*0.95, cy + radius*0.7), (cx - radius*0.95, cy + radius*0.7)]
            pygame.draw.polygon(surface, color, points)
            self._draw_gloss(surface, cx, cy, radius)
        # outline
        ...