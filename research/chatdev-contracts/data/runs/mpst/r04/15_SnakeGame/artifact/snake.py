'''
Snake entity: manages the snake's body, movement, growth and self-collision.
'''
from collections import deque
import settings
class Snake:
    '''Represents the player-controlled snake.'''
    def __init__(self):
        self.reset()
    def reset(self):
        '''Reset the snake to its initial state.'''
        start_x = settings.GRID_WIDTH // 2
        start_y = settings.GRID_HEIGHT // 2
        # Body is a deque of (x, y) tuples, head is the last element
        self.body = deque([
            (start_x - 2, start_y),
            (start_x - 1, start_y),
            (start_x, start_y),
        ])
        self.direction = settings.RIGHT
        self.direction_queue = []
        self.growth_pending = 0
    @property
    def head(self):
        '''Return the current head position (x, y).'''
        return self.body[-1]
    def turn(self, new_direction):
        '''
        Queue a direction change, preventing 180-degree reversals.
        The check is made against the last queued direction so that two
        quick key presses within a single tick are handled correctly.
        '''
        last = self.direction_queue[-1] if self.direction_queue else self.direction
        opposite = (-last[0], -last[1])
        if new_direction != opposite and new_direction != last:
            if len(self.direction_queue) < 2:
                self.direction_queue.append(new_direction)
    def move(self):
        '''
        Advance the snake one cell in its current direction.
        Returns the new head position.
        '''
        if self.direction_queue:
            self.direction = self.direction_queue.pop(0)
        head_x, head_y = self.head
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.append(new_head)
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.body.popleft()
        return new_head
    def grow(self, amount=1):
        '''Schedule the snake to grow by `amount` cells on subsequent moves.'''
        self.growth_pending += amount
    def hits_self(self):
        '''Return True if the head collides with any other body segment.'''
        head = self.head
        return any(segment == head for segment in list(self.body)[:-1])
    def hits_boundary(self):
        '''Return True if the head is outside the board limits.'''
        x, y = self.head
        return x < 0 or x >= settings.GRID_WIDTH or y < 0 or y >= settings.GRID_HEIGHT
    def occupies(self, position):
        '''Return True if any body segment occupies the given grid position.'''
        return position in self.body