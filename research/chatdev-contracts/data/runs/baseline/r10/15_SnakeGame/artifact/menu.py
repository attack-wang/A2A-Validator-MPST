'''
menu.py
Start-screen menu for the Classic Snake game where the player picks a
difficulty level (Easy / Medium / Hard) before each game session.
'''
import pygame
import settings
from highscore import load_highscore
class Menu:
    """Difficulty-selection screen shown before each game."""
    def __init__(self, screen):
        self.screen = screen
        self.options = list(settings.DIFFICULTY_LEVELS.keys())
        self.selected = 1  # default: Medium
        self.font_title = self._get_font(52, bold=True)
        self.font_option = self._get_font(32)
        self.font_hint = self._get_font(18)
    @staticmethod
    def _get_font(size, bold=False):
        try:
            return pygame.font.SysFont("consolas,menlo,monospace", size, bold=bold)
        except Exception:
            return pygame.font.Font(None, size)
    def run(self):
        """Display the menu and return the chosen difficulty name, or None to quit."""
        clock = pygame.time.Clock()
        while True:
            clock.tick(settings.FPS_CAP)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        return None
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return self.options[self.selected]
            self._render()
            pygame.display.flip()
    def _render(self):
        """Draw the title, difficulty options, high score and control hints."""
        self.screen.fill(settings.COLOR_MENU_BG)
        cx = settings.WINDOW_WIDTH // 2
        title = self.font_title.render("CLASSIC SNAKE", True,
                                       settings.COLOR_SNAKE_HEAD)
        self.screen.blit(title, (cx - title.get_width() // 2, 70))
        subtitle = self.font_hint.render(
            "Use arrow keys / WASD to steer - eat the red food - avoid walls and yourself",
            True, settings.COLOR_TEXT_DIM)
        self.screen.blit(subtitle, (cx - subtitle.get_width() // 2, 140))
        best = load_highscore()
        best_surf = self.font_hint.render(f"HIGH SCORE: {best}", True,
                                          settings.COLOR_TEXT_ACCENT)
        self.screen.blit(best_surf, (cx - best_surf.get_width() // 2, 175))
        y = 220
        for i, name in enumerate(self.options):
            speed = settings.DIFFICULTY_LEVELS[name]
            label = f"{name}  ({speed} moves/s)"
            if i == self.selected:
                surf = self.font_option.render(f"> {label} <",
                                               True, settings.COLOR_TEXT_ACCENT)
            else:
                surf = self.font_option.render(label, True, settings.COLOR_TEXT)
            self.screen.blit(surf, (cx - surf.get_width() // 2, y))
            y += 48
        hint = self.font_hint.render(
            "UP/DOWN: select    ENTER/SPACE: start    ESC/Q: quit",
            True, settings.COLOR_TEXT_DIM)
        self.screen.blit(hint, (cx - hint.get_width() // 2,
                                settings.WINDOW_HEIGHT - 50))