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
import time
import settings
# Text playfield dimensions (in characters)
WIDTH = 60
HEIGHT = 24
ALIEN_CHAR = "W"
PLAYER_CHAR = "A"
BULLET_CHAR = "|"
EMPTY_CHAR = "."
try:  # Windows
    import msvcrt
except ImportError:
    msvcrt = None
try:  # POSIX
    import termios
    import tty
    import select
except ImportError:
    termios = None
def read_key():
    '''Return a normalized action for a pressed key, or None if no input.'''
    if msvcrt is not None:
        if not msvcrt.kbhit():
            return None
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):  # special keys (arrows)
            code = msvcrt.getwch()
            return {"K": "left", "M": "right"}.get(code)
        return {"a": "left", "d": "right", " ": "fire", "q": "quit"}.get(ch.lower())
    if termios is not None:
        if not select.select([sys.stdin], [], [], 0)[0]:
            return None
        ch = sys.stdin.read(1)
        if ch == "\x1b":  # escape sequence (arrows)
            if select.select([sys.stdin], [], [], 0)[0]:
                sys.stdin.read(1)  # '['
                if select.select([sys.stdin], [], [], 0)[0]:
                    code = sys.stdin.read(1)
                    return {"D": "left", "C": "right"}.get(code)
            return None
        return {"a": "left", "d": "right", " ": "fire", "q": "quit"}.get(ch.lower())
    return None
class TextGame:
    '''Turn-free, real-time terminal rendition of Space Invaders.'''
    TICK = 0.05  # seconds per simulation step
    def __init__(self):
        self.score = 0
        self.lives = settings.PLAYER_START_LIVES
        self.player_x = WIDTH // 2
        self.cooldown = 0
        self.bullets = []        # player bullets as [x, y]
        self.alien_bullets = []  # alien bullets as [x, y]
        self.fire_timer = random.uniform(1.0, settings.ALIEN_FIRE_INTERVAL)
        self.direction = 1
        self.step_accum = 0.0
        self.fleet = self._build_fleet()
        self.game_over = False
        self.victory = False
        self.quit = False
    def _build_fleet(self):
        '''Create the alien grid as {(row, col): [x, y]}.'''
        fleet = {}
        start_x = (WIDTH - settings.ALIEN_COLUMNS * 3) // 2
        for row in range(settings.ALIEN_ROWS):
            for col in range(settings.ALIEN_COLUMNS):
                fleet[(row, col)] = [start_x + col * 3, 2 + row]
        return fleet
    @property
    def alive(self):
        '''Return [(row, col, x, y), ...] for every living alien.'''
        return [(rc[0], rc[1], pos[0], pos[1]) for rc, pos in self.fleet.items()]
    def run(self):
        '''Main terminal loop.'''
        if termios is not None:
            old_attrs = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        try:
            while not self.quit and not self.game_over and not self.victory:
                self.handle_input()
                self.step()
                self.draw()
                time.sleep(self.TICK)
            self.draw()
            while not self.quit:
                action = read_key()
                if action == "quit" or action == "left" and False:
                    ...