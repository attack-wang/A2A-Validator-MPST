'''
snake.py
Defines the Snake entity: body storage, direction handling with an
input queue that prevents illegal 180-degree turns, and movement.
'''
from collections import deque
import config
class Snake:
    '''
    Represents the player-controlled snake on the grid.
    The body is stored as a deque of (x, y) cells from head to tail.
    Direction changes are queued so that multiple key presses within a
    single game tick are applied one per tick, and reversing directly
    into the snake's own neck is rejected.
    '''
    def __init__(self, start_x, start_y, initial_length=4):
        self.initial_length = initial_length
        self.direction = config.RIGHT
        self.pending_directions = deque()
        self.growth_pending = 0
        self.body = deque()
        self._reset(start_x, start_y)
    def _reset(self, start_x, start_y):
        '''Rebuild the snake facing right with its head at (start_x, start_y).'''
        self.direction = config.RIGHT
        self.pending_directions.clear()
        self.growth_pending = 0
        self.body.clear()
        for i in range(self.initial_length):
            self.body.append((start_x - i, start_y))
    def reset(self, start_x, start_y):
        '''Public reset used when a new game session starts.'''
        self._reset(start_x, start_y)
    def set_direction(self, new_direction):
        '''
        Queue a direction change. The move is ignored if it would
        reverse the snake (opposite of the last queued/current direction)
        or duplicate the last queued direction.
        '''
        if new_direction not in (config.UP, config.DOWN, config.LEFT, config.RIGHT):
            return
        last = self.pending_directions[-1] if self.pending_directions else self.direction
        if (new_direction[0] == -last[0] and new_direction[1] == -last[1]):
            return
        if new_direction == last:
            return
        if len(self.pending_directions) < 3:
            self.pending_directions.append(new_direction)
    def peek_next_head(self):
        '''Compute the head cell for the next tick without moving.'''
        if self.pending_directions:
            direction = self.pending_directions[0]
        else:
            direction = self.direction
        hx, hy = self.body[0]
        return (hx + direction[0], hy + direction[1])
    def advance(self, grow=False):
        '''
        Move the snake one cell in its (possibly queued) direction.
        If `grow` is True the tail is kept, otherwise it is removed.
        '''
        if self.pending_directions:
            self.direction = self.pending_directions.popleft()
        hx, hy = self.body[0]
        dx, dy = self.direction
        self.body.appendleft((hx + dx, hy + dy))
        if grow:
            self.growth_pending = 0  # already grew by not popping
        else:
            self.body.pop()
    def grow(self, amount=1):
        '''Schedule extra growth for subsequent ticks (unused for now).'''
        self.growth_pending += amount
    def get_body(self):
        '''Return the body cells as a list, head first.'''
        return list(self.body)
    def get_direction(self):
        '''Return the current movement direction.'''
        return self.direction