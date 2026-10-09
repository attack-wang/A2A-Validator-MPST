'''
ui.py
HUD and menu rendering helpers (score display, messages, game-over panel).
Fix applied from the test report: SCREEN_HEIGHT is now imported — it was used
in draw_game_over() but missing from the import list, which would have raised
a NameError the first time the game-over panel was drawn.
'''
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TEXT_COLOR, TEXT_OUTLINE, SCORE_COLOR, PANEL_COLOR,
)
def _blit_centered(surface, text_surf, center):
    rect = text_surf.get_rect(center=center)
    surface.blit(text_surf, rect)
def draw_text(surface, text, font, center, color=TEXT_COLOR, outline=True):
    """Render text with an optional outline, centred on `center`."""
    text_surf = font.render(text, True, color)
    if outline:
        outline_surf = font.render(text, True, TEXT_OUTLINE)
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)):
            _blit_centered(surface, outline_surf, (center[0] + dx, center[1] + dy))
    _blit_centered(surface, text_surf, center)
def draw_score(surface, score, font):
    draw_text(surface, str(score), font, (SCREEN_WIDTH // 2, 70), SCORE_COLOR)
def draw_center_text(surface, text, font, y, color=TEXT_COLOR):
    draw_text(surface, text, font, (SCREEN_WIDTH // 2, y), color)
def draw_game_over(surface, score, best, font_big, font_small):
    panel = pygame.Rect(0, 0, 320, 190)
    panel.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
    pygame.draw.rect(surface, PANEL_COLOR, panel, border_radius=12)
    pygame.draw.rect(surface, TEXT_OUTLINE, panel, 3, border_radius=12)
    draw_text(surface, "GAME OVER", font_big, (panel.centerx, panel.top + 40), TEXT_OUTLINE, outline=False)
    draw_text(surface, f"Score: {score}", font_small, (panel.centerx, panel.top + 95), TEXT_OUTLINE, outline=False)
    draw_text(surface, f"Best: {best}", font_small, (panel.centerx, panel.top + 130), TEXT_OUTLINE, outline=False)
    draw_text(surface, "Press SPACE to restart", font_small, (panel.centerx, panel.bottom - 28), TEXT_OUTLINE, outline=False)