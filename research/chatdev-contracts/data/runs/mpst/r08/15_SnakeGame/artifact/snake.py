'''
snake.py
Defines the Snake entity: body representation, direction handling with a
small input queue (to avoid missed/reversed turns), movement, growth and
collision checks.
'''
from collections import deque
# Direction vectors: (dx, dy)
DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)
MAX_QUEUED_TURNS = 2
class Snake:
    '''Grid-based snake whose body is a list of (x, y) cells, head first.'''
    def __init__(self, start_x, start_y, initial_length=3):
        if initial_length < 1:
            raise ValueError("initial_length must be at least 1")
        if start_x - (initial_length - 1) < 0:
            # FIX: fail loudly instead of silently clamping, which could
            # create overlapping segments and false self-collisions.
            raise ValueError(
                "initial_length too long for start position: "
                f"start_x={start_x}, initial_length={initial_length}"
            )
        # Build the body extending to the left of the start cell so that the
        # snake initially moves to the right without overlapping itself.
        self.body = [(start_x - i, start_y) for i in range(initial_length)]
        self.direction = DIR_RIGHT
        self.direction_queue = deque()
        self.grow_pending = 0
    def set_direction(self, direction):
        '''Queue a direction change, ignoring reversals and duplicates.'''
        last = self.direction_queue[-1] if self.direction_queue else self.direction
        if direction == last:
            return
        if direction[0] == -last[0] and direction[1] == -last[1]:
            return  # 180-degree reversal is not allowed
        if len(self.direction_queue) < MAX_QUEUED_TURNS:
            self.direction_queue.append(direction)
    def move(self):
        '''Advance one cell in the current direction; returns the new head.'''
        if self.direction_queue:
            self.direction = self.direction_queue.popleft()
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
        return new_head
    def grow(self, amount=1):
        '''Schedule the snake to grow by `amount` cells on subsequent moves.'''
        self.grow_pending += amount
    def hits_self(self):
        '''True if the head overlaps any body segment.'''
        return self.body[0] in self.body[1:]
    def hits_boundary(self, grid_width, grid_height):
        '''True if the head is outside the playfield.'''
        head_x, head_y = self.body[0]
        return (
            head_x < 0 or head_y < 0
            or head_x >= grid_width or head_y >= grid_height
        )
    @property
    def length(self):
        return len(self.body)