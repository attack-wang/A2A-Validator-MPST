'''
Snake class representing the player-controlled snake.
'''
from config import UP, DOWN, LEFT, RIGHT
class Snake:
    '''Represents the snake: its body, direction, movement and collisions.'''
    def __init__(self, start_x, start_y, initial_length=3):
        '''Initialize the snake with a horizontal body pointing right.'''
        self._direction = RIGHT
        self._next_direction = RIGHT
        # Body is a list of (x, y) tuples, head first
        self.body = [(start_x - i, start_y) for i in range(initial_length)]
        self.grow_pending = False
    @property
    def head(self):
        '''Return the current head position (x, y).'''
        return self.body[0]
    @property
    def direction(self):
        '''Return the current movement direction.'''
        return self._direction
    def set_direction(self, direction):
        '''Queue a new direction, ignoring 180-degree reversals.'''
        opposite = {
            UP: DOWN,
            DOWN: UP,
            LEFT: RIGHT,
            RIGHT: LEFT,
        }
        if direction != opposite[self._direction]:
            self._next_direction = direction
    def move(self):
        '''Advance the snake one cell in its direction.'''
        self._direction = self._next_direction
        dx, dy = self._direction
        head_x, head_y = self.head
        new_head = (head_x + dx, head_y + dy)
        # Insert new head
        self.body.insert(0, new_head)
        # Remove tail unless the snake is growing this tick
        if self.grow_pending:
            self.grow_pending = False
        else:
            self.body.pop()
    def grow(self):
        '''Mark the snake to grow one segment on the next move.'''
        self.grow_pending = True
    def check_self_collision(self):
        '''Return True if the head collides with any body segment.'''
        return self.head in self.body[1:]
    def check_boundary_collision(self, grid_width, grid_height):
        '''Return True if the head is outside the board boundaries.'''
        x, y = self.head
        return x < 0 or x >= grid_width or y < 0 or y >= grid_height