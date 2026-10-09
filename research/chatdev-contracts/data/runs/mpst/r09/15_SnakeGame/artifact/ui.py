'''
ui.py
Reusable drawing helpers for the Snake game: text rendering with
anchor points (center / topleft / topright) and a semi-transparent
centred overlay used for the game-over and win screens.
'''
import pygame
import settings
def draw_text(surface, text, size, color, center=None, topleft=None,
              topright=None, bold=False):
    """Render `text` and blit it onto `surface` at the given anchor."""
    font = pygame.font.SysFont(settings.FONT_NAME, size, bold=bold)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center is not None:
        rect.center = center
    elif topleft is not None:
        rect.topleft = topleft
    elif topright is not None:
        rect.topright = topright
    else:
        rect.topleft = (0, 0)
    surface.blit(rendered, rect)
    return rect
def draw_overlay(surface, lines, title_color=None):
    """Draw a centred, semi-transparent overlay with the given text lines."""
    if title_color is None:
        title_color = settings.COLOR_HIGHLIGHT
    overlay = pygame.Surface(
        (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA
    )
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))
    cx = settings.WINDOW_WIDTH // 2
    y = settings.WINDOW_HEIGHT // 2 - len(lines) * 30
    for i, line in enumerate(lines):
        if i == 0:
            draw_text(surface, line, settings.FONT_SIZE_MENU, title_color,
                      center=(cx, y), bold=True)
            y += 50
        else:
            draw_text(surface, line, settings.FONT_SIZE_HUD,
                      settings.COLOR_TEXT, center=(cx, y))
            y += 32