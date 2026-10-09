'''
Heads-up display: score, target, timer, level, and messages.
'''
import pygame
import settings
_FONT_CACHE = {}
def get_font(size, bold=False):
    key = (size, bold)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = pygame.font.SysFont("arial", size, bold=bold)
    return _FONT_CACHE[key]
class HUD:
    def __init__(self):
        self.font = get_font(22, bold=True)
        self.big_font = get_font(48, bold=True)
        self.small_font = get_font(16)
        self.message = ""
        self.message_timer = 0.0
    def show_message(self, text, duration=2.0):
        self.message = text
        self.message_timer = duration
    def update(self, dt):
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""
    def draw(self, surface, game):
        # top bar
        pygame.draw.rect(surface, settings.COLOR_DIRT_DARK,
                         (0, 0, settings.SCREEN_WIDTH, 60))
        # score / target
        score_text = self.font.render(f"Gold: {game.gold}", True, settings.COLOR_YELLOW)
        target_text = self.font.render(f"Target: {game.level.target}", True, settings.COLOR_WHITE)
        level_text = self.font.render(f"Level {game.level_number}", True, settings.COLOR_WHITE)
        time_color = settings.COLOR_RED if game.time_left <= 10 else settings.COLOR_WHITE
        time_text = self.font.render(f"Time: {max(0, int(math.ceil(game.time_left)))}", True, time_color)
        ...