'''
HUD rendering: score display and difficulty indicator.
'''
import pygame
import settings
_FONT_CACHE = {}
def _get_font(size, bold=True):
    """Return a cached SysFont to avoid re-loading fonts every frame."""
    key = (size, bold)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = pygame.font.SysFont("arial", size, bold=bold)
    return _FONT_CACHE[key]
def draw_text(surface, text, size, color, center, outline=True, bold=True):
    """Render text with an optional dark outline for readability."""
    font = _get_font(size, bold)
    label = font.render(text, True, color)
    if outline:
        outline_label = font.render(text, True, settings.TEXT_OUTLINE)
        for offset in (-2, 2):
            surface.blit(outline_label, label.get_rect(center=(center[0] + offset, center[1])).topleft)
            surface.blit(outline_label, label.get_rect(center=(center[0], center[1] + offset)).topleft)
    surface.blit(label, label.get_rect(center=center).topleft)
class HUD:
    """Draws the in-game score and difficulty indicator."""
    def draw_score(self, surface, score):
        """Draw the current score centered near the top."""
        draw_text(surface, str(score), 48, settings.TEXT_COLOR, (settings.SCREEN_WIDTH // 2, 60))
    def draw_difficulty(self, surface, level):
        """Draw the current difficulty level (1..10)."""
        draw_text(surface, "Level {}/10".format(level), 16, settings.TEXT_COLOR,
                  (settings.SCREEN_WIDTH // 2, 96), outline=False)