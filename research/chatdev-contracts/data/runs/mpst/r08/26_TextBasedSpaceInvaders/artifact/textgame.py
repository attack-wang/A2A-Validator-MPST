'''Terminal fallback version of Space Invaders for machines without pygame.
The playfield is drawn as characters in the console. The player controls a
ship on the bottom row, fires upward, and must destroy every alien before
the fleet descends onto the ship.
Controls:
  a / LEFT arrow  : move left
  d / RIGHT arrow : move right
  SPACE           : fire
  q               : quit
'''
import random
import sys
import settings
# Text playfield dimensions (characters)
WIDTH = 60
HEIGHT = 24
ALIEN_CHAR = "W"
PLAYER_CHAR = "A"
BULLET_CHAR = "|"
EMPTY_CHAR = " "
class TextGame:
    '''Turn-based terminal rendition of Space Invaders.'''
    def __init__(self):
        self.score = 0
        self.lives = settings.PLAYER_START_LIVES
        self.player_x = WIDTH // 2
        self.bullets = []          # player bullets: (x, y)
        self.alien_bullets = []    # alien bullets: (x, y)
        self.alien_points = list(settings.ALIEN_POINTS_PER_ROW)
        self.fleet = self._build_fleet()
        self.direction = 1
        self.message = ""
        self.game_over = False
        self.victory = False
    def _build_fleet(self):
        '''Create the alien grid as a dict mapping (row, col) -> (x, y).'''
        fleet = {}
        start_x = (WIDTH - settings.ALIEN_COLUMNS * 2) // 2  # 2 chars per alien
        for row in range(settings.ALIEN_ROWS):
            for col in range(settings.ALIEN_COLUMNS):
                x = start_x + col * 3
                y = 2 + row
                fleet[(row, col)] = [x, y]
        return fleet
    def alive_cells(self):
        return self.fleet.items()
    def run(self):
        '''Main terminal loop.'''
        import termios, tty ...