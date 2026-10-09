"""
hud.py
Heads-up display: score, level target with progress bar, remaining time,
level number, live claw position read-out and floating grab messages.
"""
import pygame
import settings as S
class HUD:
    def __init__(self):
        self.font_big = pygame.font.SysFont("arial", 34, bold=True)
        self.font = pygame.font.SysFont("arial", 22)
        self.font_small = pygame.font.SysFont("arial", 17)
        self.messages = []  # dicts: text, color, x, y, life
    def add_message(self, text, color, pos):
        """Spawn a floating score message at the given world position."""
        self.messages.append({
            'text': text,
            'color': color,
            'x': pos[0],
            'y': pos[1],
            'life': 1.4,
        })
    def update(self, dt):
        """Float messages upward and remove expired ones."""
        for m in self.messages:
            m['life'] -= dt
            m['y'] -= 30 * dt
        self.messages = [m for m in self.messages if m['life'] > 0]
    def draw(self, surface, game):
        """Render the top bar, progress bar, timer, claw read-out and messages."""
        panel = pygame.Rect(0, 0, S.SCREEN_WIDTH, 64)
        pygame.draw.rect(surface, S.HUD_PANEL, panel)
        pygame.draw.line(surface, S.HUD_TEXT, (0, 64), (S.SCREEN_WIDTH, 64), 2)
        # Score
        score_surf = self.font.render("Gold: %d" % game.score, True, S.HUD_TEXT)
        surface.blit(score_surf, (16, 8))
        # Level
        lvl_surf = self.font.render("Level %d" % game.level_number, True, S.HUD_TEXT)
        surface.blit(lvl_surf, (16, 34))
        # Target progress bar
        target = game.level.target if game.level else 1
        progress = min(1.0, game.score / target) if target > 0 else 1.0
        bar_x, bar_y, bar_w, bar_h = 200, 12, 300, 18
        pygame.draw.rect(surface, (60, 60, 75), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
        fill_w = int(bar_w * progress)
        if fill_w > 0:
            pygame.draw.rect(surface, S.GOLD_COLOR, (bar_x, bar_y, fill_w, bar_h), border_radius=6)
        pygame.draw.rect(surface, S.HUD_TEXT, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=6)
        tgt_surf = self.font_small.render("Target: %d / %d" % (game.score, target), True, S.HUD_TEXT)
        surface.blit(tgt_surf, (bar_x, bar_y + bar_h + 2))
        # Timer
        if game.level:
            time_left = max(0.0, game.level.time_left)
            color = S.HUD_TEXT if time_left > 10 else S.MESSAGE_BAD
            time_surf = self.font.render("Time: %d" % math.ceil(time_left), True, color)
            surface.blit(time_surf, (S.SCREEN_WIDTH - 150, 8))