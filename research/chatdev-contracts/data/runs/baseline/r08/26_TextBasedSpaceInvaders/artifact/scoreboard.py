'''
scoreboard.py
Draws the HUD: score, high score, wave counter and remaining lives
(rendered as tiny ship icons). Uses tkinter canvas text items.
'''
from settings import Settings
class Scoreboard:
    """Renders score / high score / wave / lives on screen."""
    def __init__(self, game):
        self.game = game
        self.high_score = 0
    def update_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
    def _text(self, canvas, text, x, y, color, size=22, anchor="w"):
        canvas.create_text(x, y, text=text, fill=color,
                           font=(Settings.FONT_FAMILY, size, "bold"),
                           anchor=anchor)
    def draw(self, canvas, score, lives, wave):
        self.update_high_score(score)
        self._text(canvas, f"SCORE: {score}", 16, 10, Settings.HUD_COLOR, 22, "nw")
        self._text(canvas, f"HI: {self.high_score}",
                   Settings.SCREEN_WIDTH // 2, 10, Settings.ACCENT_COLOR, 22, "n")
        self._text(canvas, f"WAVE: {wave}/{Settings.MAX_WAVES}",
                   Settings.SCREEN_WIDTH - 16, 10, Settings.HUD_COLOR, 22, "ne")
        # Lives as tiny ship icons at the bottom-left.
        self._text(canvas, "LIVES", 16, Settings.SCREEN_HEIGHT - 34,
                   Settings.HUD_COLOR, 14, "nw")
        for i in range(lives):
            x = 16 + i * 26
            y = Settings.SCREEN_HEIGHT - 16
            canvas.create_polygon(x + 9, y - 11, x + 18, y, x, y,
                                  fill=Settings.SHIP_COLOR, outline="")