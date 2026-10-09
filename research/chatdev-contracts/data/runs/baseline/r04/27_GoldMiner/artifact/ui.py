'''HUD, panels and overlay rendering.'''
import pygame
from settings import *
class UI:
    def __init__(self):
        pygame.font.init()
        self.font_big = pygame.font.SysFont('arial', 48, bold=True)
        self.font_med = pygame.font.SysFont('arial', 28, bold=True)
        self.font_small = pygame.font.SysFont('arial', 20)
        self.font_tiny = pygame.font.SysFont('arial', 16)
    def draw_hud(self, surface, level_num, score, target, time_left):
        bar = pygame.Rect(0, 0, SCREEN_WIDTH, HUD_HEIGHT)
        pygame.draw.rect(surface, COLOR_HUD_BG, bar)
        pygame.draw.rect(surface, COLOR_BLACK, bar, 2)
        t1 = self.font_med.render(f'Level {level_num}', True, COLOR_GOLD)
        surface.blit(t1, (16, 8))
        t2 = self.font_small.render(f'Gold: {score} / {target}', True, COLOR_WHITE)
        surface.blit(t2, (16, 40))
        # timer
        t3 = self.font_med.render(f'Time: {time_left:4.1f}', True,
                                  COLOR_RED if time_left <= 10 else COLOR_WHITE)
        surface.blit(t3, (SCREEN_WIDTH - 220, 20))
        # progress bar
        bar_rect = pygame.Rect(220, 24, 380, 24)
        pygame.draw.rect(surface, COLOR_BAR_BG, bar_rect, border_radius=6)
        frac = min(1.0, score / target) if target > 0 else 1.0
        fill = pygame.Rect(bar_rect.x + 2, bar_rect.y + 2,
                           int((bar_rect.width - 4) * frac), bar_rect.height - 4)
        if fill.width > 0:
            pygame.draw.rect(surface, COLOR_BAR_FILL if frac < 1 else COLOR_BAR_OK, fill, border_radius=6)
        pygame.draw.rect(surface, COLOR_BLACK, bar_rect, 2, border_radius=6)
        lbl = self.font_tiny.render('TARGET', True, COLOR_WHITE)
        surface.blit(lbl, (bar_rect.x, bar_rect.y - 2))  # hmm overlapping