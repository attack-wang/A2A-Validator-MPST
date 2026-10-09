'''
snake.py
Snake entity: body storage, direction handling with an input queue,
growth, self-collision and occupancy checks.
'''
from collections import deque
import settings
class Snake:
    """Grid-based snake with a deque body and queued direction changes."""
    def __init__(self):
        cx = settings.BOARD_WIDTH // 2
        cy = settings.BOARD_HEIGHT // 2
        # Head first; initial body extends to the left, moving RIGHT.
        self.body = deque(
            (cx - i, cy) for i in range(settings.INITIAL_SNAKE_LENGTH)
        )
        self.direction = settings.RIGHT
        self.pending_directions = deque()
        self.grow_pending = 0
    def head(self):
        """Return the current head cell."""
        return self.body[0]
    def occupies(self, cell):
        """True if any body segment sits on `cell`."""
        return cell in self.body
    def change_direction(self, new_direction):
        """Queue a direction change, rejecting 180-degree reversals."""
        last = self.pending_directions[-1] if self.pending_directions else self.direction
        if (new_direction[0] + last[0], new_direction[1] + last[1]) != (0, 0):
            if len(self.pending_directions) < 3:
                self.pending_directions.append(new_direction)
    def peek_direction(self):
        """Pop the next queued direction (if any) and make it current."""
        if self.pending_directions:
            self.direction = self.pending_directions.popleft()
        return self.direction
    def grow(self):
        """Schedule one extra segment on the next move."""
        self.grow_pending += 1
    def move(self):
        """Advance one cell; returns the new head position."""
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.appendleft(new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
        return new_head
    def hits_self(self, head=None):
        """True if the head overlaps any body segment.
        The tail cell is ignored when the snake did not just eat, because
        the tail vacates its cell on the same tick the head enters it.
        """
        if head is None:
            head = self.body[0]
        segments = list(self.body)[1:]
        if self.grow_pending == 0 and len(segments) > 1:
            segments = segments[:-1]
        return head in segments