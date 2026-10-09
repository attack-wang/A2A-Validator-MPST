'''
Utility helpers: high score persistence and drawing helpers.
'''
import os
import pygame
from settings import *
HIGHSCORE_FILE = "highscore.dat"
def load_high_score():
    """Read the persisted high score; return 0 if missing/corrupt."""
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip() or 0)
    except (IOError, ValueError):
        return 0
def save_high_score(score):
    """Persist the high score to disk (silently ignore IO errors)."""
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))
    except IOError:
        pass
def make_gradient_surface(width, height, top_color, bottom_color):
    """Create a vertical gradient surface between two colours."""
    surf = pygame.Surface((width, height))
    for y in range(height):
        t = y / max(1, height - 1)
        color = [int(top_color[i] + (bottom_color[i] - top_color[i]) * t) for i in range(3)]
        pygame.draw.line(surf, color, (0, y), (width, y))
    return surf
def draw_cloud(surface, x, y, scale=1.0):
    """Draw a simple puffy cloud made of overlapping circles."""
    color = CLOUD
    r = int(14 * scale)
    pygame.draw.circle(surface, color, (int(x), int(y)), r)
    pygame.draw.circle(surface, color, (int(x + r), int(y - r * 0.4)), int(r * 0.8))
    pygame.draw.circle(surface, color, (int(x - r), int(y - r * 0.3)), int(r * 0.7))
    pygame.draw.circle(surface, color, (int(x + r * 1.6), int(y + r * 0.1)), int(r * 0.6))
def draw_ground(surface, scroll_x):
    """Draw the scrolling grass + dirt ground strip."""
    ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
    pygame.draw.rect(surface, GRASS, (0, ground_y, SCREEN_WIDTH, GROUND_HEIGHT))
    # top edge
    pygame.draw.rect(surface, GRASS_DARK, (0, ground_y, SCREEN_WIDTH, 8))
    # scrolling stripes
    stripe_w = 24
    offset = scroll_x % (stripe_w * 2)
    for x in range(-stripe_w * 2, SCREEN_WIDTH + stripe_w * 2, stripe_w * 2):
        pygame.draw.polygon(surface, GRASS_LIGHT, [
            (x + offset, ground_y + 8),
            (x + offset + stripe_w, ground_y + 8),
            (x + offset + stripe_w - 12, ground_y + 24),
            (x + offset - 12, ground_y + 24),
        ])
    # dirt below
    pygame.draw.rect(surface, DIRT, (0, ground_y + 24, SCREEN_WIDTH, GROUND_HEIGHT - 24))
    pygame.draw.rect(surface, DIRT_DARK, (0, ground_y + 24, SCREEN_WIDTH, 4))