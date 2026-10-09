'''
Overlay screens: start menu and game-over display.
'''
import pygame
import settings
from ui import draw_text
class Screens:
    """Static renderers for the start and game-over overlays."""
    @staticmethod
    def draw_start(surface):
        """Draw the title screen with control hints."""
        cx = settings.SCREEN_WIDTH // 2
        cy = settings.SCREEN_HEIGHT
        draw_text(surface, "FLAPPY BIRD", 44, settings.TEXT_COLOR, (cx, int(cy * 0.26)))
        draw_text(surface, "Press SPACE / UP to flap", 20, settings.TEXT_COLOR, (cx, int(cy * 0.44)))
        draw_text(surface, "Click or press any key to start", 16, settings.TEXT_COLOR,
                  (cx, int(cy * 0.54)), outline=False)
    @staticmethod
    def draw_game_over(surface, score, best):
        """Draw the game-over overlay with final and best scores."""
        cx = settings.SCREEN_WIDTH // 2
        cy = settings.SCREEN_HEIGHT
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))
        draw_text(surface, "GAME OVER", 44, settings.TEXT_COLOR, (cx, int(cy * 0.30)))
        draw_text(surface, "Score: {}   Best: {}".format(score, best), 22, settings.TEXT_COLOR,
                  (cx, int(cy * 0.44)))
        draw_text(surface, "Press R or SPACE to restart", 16, settings.TEXT_COLOR,
                  (cx, int(cy * 0.54)), outline=False)