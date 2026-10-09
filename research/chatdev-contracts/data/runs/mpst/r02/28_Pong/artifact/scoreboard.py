'''
Scoreboard module.
Tracks both players' scores, renders them at the top of the screen and
reports when one of them reaches the winning threshold. Rendering is
done on a tkinter Canvas (Python standard library only).
'''
from settings import (
    COLOR_TEXT,
    SCREEN_WIDTH,
    SCORE_FONT_NAME,
    SCORE_FONT_SIZE,
    WINNING_SCORE,
)
class Scoreboard:
    """Keeps the score of the left (index 0) and right (index 1) players."""
    def __init__(self):
        """Create the scoreboard with both scores at zero."""
        self.scores = [0, 0]
    def score_point(self, player_index):
        """Add one point to the given player (0 = left, 1 = right)."""
        self.scores[player_index] += 1
    def winner(self):
        """Return the index of the winning player, or None if nobody
        has reached the winning score yet."""
        for index, score in enumerate(self.scores):
            if score >= WINNING_SCORE:
                return index
        return None
    def reset(self):
        """Set both scores back to zero for a fresh match."""
        self.scores = [0, 0]
    def draw(self, canvas):
        """Render both scores centred at the top of the screen."""
        text = f"{self.scores[0]}   {self.scores[1]}"
        canvas.create_text(
            SCREEN_WIDTH // 2, 40, text=text,
            fill=COLOR_TEXT,
            font=(SCORE_FONT_NAME, SCORE_FONT_SIZE, "bold"),
        )