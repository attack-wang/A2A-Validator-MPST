'''
scoreboard.py
HUD rendering for score, high score and lives, plus high-score
persistence to disk between sessions.
'''
import pygame
import settings
class Scoreboard:
    """Tracks and renders score, high score and remaining lives."""
    def __init__(self):
        self.font = pygame.font.SysFont(None, settings.FONT_SIZE)
        self.score = 0
        self.high_score = self._load_high_score()
    def _load_high_score(self):
        """Read the persisted high score; return 0 if unavailable."""
        try:
            with open(settings.HIGH_SCORE_FILE, "r") as fh:
                return int(fh.read().strip() or 0)
        except (IOError, ValueError):
            return 0
    def save_high_score(self):
        """Persist the high score to disk (best effort)."""
        try:
            with open(settings.HIGH_SCORE_FILE, "w") as fh:
                fh.write(str(self.high_score))
        except IOError:
            pass
    def add_points(self, points):
        """Add points to the score, updating the high score if beaten."""
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
    def reset(self):
        """Reset the current score for a new game."""
        self.score = 0
    def draw(self, screen, lives):
        """Render score, high score and life icons along the top bar."""
        score_surf = self.font.render(f"SCORE: {self.score}", True, settings.WHITE)
        screen.blit(score_surf, (10, 8))
        hi_surf = self.font.render(f"HI: {self.high_score}", True, settings.CYAN)
        screen.blit(hi_surf, (settings.SCREEN_WIDTH // 2 - hi_surf.get_width() // 2, 8))
        # lives icons on the right
        life_label = self.font.render("LIVES:", True, settings.WHITE)
        icon_w = 24
        gap = 6
        icons_w = settings.PLAYER_LIVES * icon_w + (settings.PLAYER_LIVES - 1) * gap
        label_x = settings.SCREEN_WIDTH - 10 - icons_w - 8 - life_label.get_width()
        screen.blit(life_label, (label_x, 8))
        icon_x = label_x + life_label.get_width() + 8
        for i in range(lives):
            px = icon_x + i * (icon_w + gap)
            points = [(px + icon_w // 2, 10), (px, 30), (px + icon_w, 30)]
            pygame.draw.polygon(screen, settings.GREEN, points)