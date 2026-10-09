'''On-screen display for score, lives, and end-of-game messages.'''
import pygame
from settings import (WHITE, HUD_FONT_SIZE, LARGE_FONT_SIZE, SCREEN_WIDTH,
                      SCREEN_HEIGHT)
class HUD:
    '''Draws the score, lives, and center messages on the screen.'''
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("monospace", HUD_FONT_SIZE, bold=True)
        self.large_font = pygame.font.SysFont("monospace", LARGE_FONT_SIZE, bold=True)
    def draw(self, screen, score, lives):
        '''Render the score and remaining lives.'''
        score_surf = self.font.render(f"SCORE: {score}", True, WHITE)
        screen.blit(score_surf, (10, 8))
        lives_surf = self.font.render(f"LIVES: {lives}", True, WHITE)
        screen.blit(lives_surf, (SCREEN_WIDTH - lives_surf.get_width() - 10, 8))
    def draw_center_message(self, screen, title, subtitle):
        '''Render a large centered message with a smaller line beneath it.'''
        title_surf = self.large_font.render(title, True, WHITE)
        sub_surf = self.font.render(subtitle, True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(title_surf, title_rect)
        screen.blit(sub_surf, sub_rect)