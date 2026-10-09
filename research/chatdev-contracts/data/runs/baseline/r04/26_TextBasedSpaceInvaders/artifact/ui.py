'''
HUD and centered text drawing helpers.
'''
import pygame
import settings
def draw_hud(screen, font, score, lives, high_score=0):
    '''Draw score, lives and optional high score at the top of the screen.'''
    score_surf = font.render(f"Score: {score}", True, settings.COLOR_TEXT)
    screen.blit(score_surf, (16, 12))
    lives_surf = font.render(f"Lives: {lives}", True, settings.COLOR_TEXT)
    screen.blit(lives_surf, (settings.SCREEN_WIDTH - lives_surf.get_width() - 16, 12))
    if high_score:
        hi_surf = font.render(f"High: {high_score}", True, settings.COLOR_UI)
        rect = hi_surf.get_rect(midtop=(settings.SCREEN_WIDTH // 2, 12))
        screen.blit(hi_surf, rect)
def draw_center_text(screen, font, text, color, y_offset=0):
    '''Render text centered horizontally, optionally offset vertically.'''
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(settings.SCREEN_WIDTH // 2,
                                 settings.SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(surf, rect)