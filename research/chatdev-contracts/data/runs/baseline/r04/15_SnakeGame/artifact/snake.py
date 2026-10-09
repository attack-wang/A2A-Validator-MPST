'''
snake.py
Defines the Snake entity for the Classic Snake game.
The snake is stored as a deque of (x, y) grid cells, head first. It supports
direction changes (with reversal protection), stepping one cell per move,
deferred growth after eating, and collision queries against its own body and
the board boundaries.
'''
from collections import deque
import settings
class Snake:
    '''Grid-based snake with head-first body storage and growth support.'''
    def __init__(self, start_x, start_y, initial_length=3):
        '''Spawn a horizontal snake of `initial_length` cells heading right.'''
        self.body = deque()
        for i in range(initial_length):
            # Append cells to the left of the head so the body trails behind.
            self.body.appendleft((start_x - i, start_y))
        self.direction = settings.RIGHT
        self.pending_growth = 0
    # ------------------------------------------------------------------ #
    # Queries
    # ------------------------------------------------------------------ #
    def get_head(self):
        '''Return the current head cell as (x, y).'''
        return self.body[0]
    def get_length(self):
        '''Return the number of cells the snake currently occupies.'''
        return len(self.body)
    def hits_wall(self, cell):
        '''Return True if `cell` lies outside the board boundaries.'''
        x, y = cell
        return not (0 <= x < settings.GRID_WIDTH and 0 <= y < settings.GRID_HEIGHT)
    def hits_self(self, cell):
        '''
        Return True if `cell` overlaps the snake's body.
        The tail cell is excluded when the snake is not about to grow,
        because the tail vacates its cell on the same tick the head enters.
        '''
        cells = list(self.body)
        if self.pending_growth == 0 and len(cells) > 1:
            cells = cells[:-1]
        return cell in cells
    # ------------------------------------------------------------------ #
    # Commands
    # ------------------------------------------------------------------ #
    def set_direction(self, new_direction):
        '''Change heading unless that would instantly reverse the snake.'''
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite and new_direction != self.direction:
            self.direction = new_direction
    def grow(self, amount=1):
        '''Schedule `amount` extra cells to be added on upcoming moves.'''
        self.pending_growth += amount
    def move(self):
        '''
        Step one cell in the current direction.
        The new head is prepended; the tail is removed unless growth is
        pending. Returns the new head cell so callers can react (e.g. to
        food being eaten).
        '''
        head_x, head_y = self.get_head()
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.appendleft(new_head)
        if self.pending_growth > 0:
            self.pending_growth -= 1
        else:
            self.body.pop()
        return new_head