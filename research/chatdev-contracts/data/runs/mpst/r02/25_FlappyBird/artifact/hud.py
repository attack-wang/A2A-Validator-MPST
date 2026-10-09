'''
HUD module: score tracking, best-score persistence and on-screen score display.
Contains:
- draw_text_with_outline(): helper that renders readable text with an
  8-direction outline so it stays legible on any background.
- Score: tracks the current run score and the all-time best score, which is
  persisted to disk (settings.HIGHSCORE_FILE) between sessions.
'''
import pygame
import settings
def draw_text_with_outline(surface, text, font, center, fill, outline, outline_width=2):
    '''Render text with an 8-direction outline so it stays readable on any background.'''
    base = font.render(text, True, fill)
    outline_surf = font.render(text, True, outline)
    rect = base.get_rect(center=center)
    for dx, dy in [(-1, -1), (0, -1), (1, -1),
                   (-1, 0), (1, 0),
                   (-1, 1), (0, 1), (1, 1)]:
        offset_rect = outline_surf.get_rect(center=(rect.centerx + dx * outline_width,
                                                    rect.centery + dy * outline_width))
        surface.blit(outline_surf, offset_rect)
    surface.blit(base, rect)
class Score:
    '''Tracks the current score and the persistent best score.'''
    def __init__(self):
        '''Initialize the current score to 0 and load the best score from disk.'''
        self.current = 0
        self.best = self._load_best()
    def _load_best(self):
        '''Read the best score from disk; return 0 if unavailable.'''
        try:
            with open(settings.HIGHSCORE_FILE) as f:
                return int(f.read().strip() or 0)
        except (FileNotFoundError, ValueError, OSError):
            return 0
    def increment(self):
        '''Add one to the current score.'''
        self.current += 1
    def reset(self):
        '''Save the best score if beaten, then reset the current score.'''
        if self.current > self.best:
            self.best = self.current
            self._save_best(self.best)
        self.current = 0
    def game_over(self):
        '''Persist the best score when a run ends.'''
        if self.current > self.best:
            self.best = self.current
            self._save_best(self.best)
    def _save_best(self, value):
        '''Write the best score to disk, ignoring write errors.'''
        try:
            with open(settings.HIGHSCORE_FILE, "w") as f:
                f.write(str(value))
        except OSError:
            pass
    def draw(self, surface, font):
        '''Draw the current score centered near the top of the screen.'''
        draw_text_with_outline(surface, str(self.current), font,
                               (settings.WINDOW_WIDTH // 2, 60),
                               settings.WHITE, settings.SCORE_OUTLINE, 3)