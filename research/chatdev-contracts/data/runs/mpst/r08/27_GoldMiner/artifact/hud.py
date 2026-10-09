'''
HUD and message rendering for the Gold Miner game.
'''
import math
import pygame
from settings import (WIDTH, HEIGHT, HUD_HEIGHT, HUD_BG, WHITE, BLACK, GOLD,
                      GREEN, RED, CYAN, GRAY_DARK)
def draw_hud(surface, fonts, level, score, target, time_left, level_score=0):
    """Draw the top HUD bar: level, total score, level target progress and timer."""
    pygame.draw.rect(surface, HUD_BG, (0, 0, WIDTH, HUD_HEIGHT))
    pygame.draw.line(surface, GRAY_DARK, (0, HUD_HEIGHT - 2), (WIDTH, HUD_HEIGHT - 2), 2)
    small = fonts['small']
    # Level
    text = small.render('Level %d' % level, True, WHITE)
    surface.blit(text, (16, 10))
    # Score
    text = small.render('Score: %d' % score, True, GOLD)
    surface.blit(text, (16, 38))
    # Target
    text = small.render('Target: %d' % target, True, CYAN)
    surface.blit(text, (170, 10))
    # Timer
    color = GREEN if time_left > 10 else RED
    text = small.render('Time: %d' % max(0, int(math.ceil(time_left))), True, color)
    surface.blit(text, (170, 38))
    # Progress bar
    draw_progress_bar(surface, (300, 14, 340, 18), level_score, target)
    label = fonts['tiny'].render('Level progress', True, WHITE)
    surface.blit(label, (300, 36))
def draw_progress_bar(surface, rect, value, maximum):
    """Draw a bordered progress bar filled to value/maximum."""
    x, y, w, h = rect
    pygame.draw.rect(surface, BLACK, (x, y, w, h))
    pygame.draw.rect(surface, GRAY_DARK, (x, y, w, h), 2)
    if maximum > 0:
        fill = max(0, min(1.0, value / maximum))
        if fill > 0:
            pygame.draw.rect(surface, GREEN, (x + 2, y + 2, int((w - 4) * fill), h - 4))
def draw_center_message(surface, font, lines, sub_font=None):
    """Draw a list of (text, color) lines centered on a translucent panel."""
    line_h = font.get_height() + 14
    total_h = line_h * len(lines)
    panel = pygame.Surface((WIDTH - 160, total_h + 40), pygame.SRCALPHA)
    panel.fill((20, 20, 35, 200))
    panel_x = 80
    panel_y = (HEIGHT - panel.get_height()) // 2
    surface.blit(panel, (panel_x, panel_y))
    y = panel_y + 20
    for text, color in lines:
        rendered = font.render(text, True, color)
        surface.blit(rendered,
                     rendered.get_rect(center=(WIDTH // 2, y + line_h // 2)))
        y += line_h