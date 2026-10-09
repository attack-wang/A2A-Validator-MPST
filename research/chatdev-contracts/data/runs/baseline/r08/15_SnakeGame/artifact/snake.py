'''
snake.py
Snake entity: body management, direction handling, movement and
collision checks (self-collision and boundary collision).
'''
from collections import deque
import config
class Snake:
    """Represents the player-controlled snake on the grid."""
    def __init__(self, start_x, start_y, initial_length=3):
        # Head first; body stretches to the left, moving right initially.
        self.body = [(start_x - i, start_y) for i in range(initial_length)]
        self.direction = config.RIGHT
        self.pending_directions = deque()  # queued turns for responsive controls
        self.grow_pending = 0
    @property
    def head(self):
        return self.body[0]
    @property
    def length(self):
        return len(self.body)
    def queue_direction(self, new_direction):
        """Queue a direction change, ignoring reversals and duplicates."""
        last = self.pending_directions[-1] if self.pending_directions else self.direction
        if new_direction == last:
            return
        # forbid 180-degree reversal relative to the last effective direction
        if new_direction[0] + last[0] == 0 and new_direction[1] + last[1] == 0:
            return
        if len(self.pending_directions) < 2:
            self.pending_directions.append(new_direction)
    def next_direction(self):
        """Pop the next queued direction (if any) to use for this tick."""
        if self.pending_directions:
            self.direction = self.pending_directions.popleft()
        return self.direction
    def next_head(self):
        """Compute the prospective head cell for the current direction."""
        dx, dy = self.direction
        hx, hy = self.head
        return (hx + dx, hy + dy)
    def step(self, grow=False):
        """Advance the snake one cell forward.
        Args:
            grow: If True, the tail is retained this tick so the snake
                  grows by one segment.
        """
        dx, dy = self.direction
        hx, hy = self.head
        self.body.insert(0, (hx + dx, hy + dy))
        if grow:
            self.grow_pending += 1
        if self.grow_pending > 0:
            self.grow_pending -= 1   # tail kept -> snake grew
        else:
            self.body.pop()          # normal move -> drop the tail
    def check_boundary(self, cell):
        """Return True if `cell` lies outside the board grid."""
        x, y = cell
        return not (0 <= x < config.GRID_WIDTH and 0 <= y < config.GRID_HEIGHT)
    def check_self_collision(self, cell, ignore_tail=True):
        """Return True if `cell` hits the snake's own body.
        Args:
            cell: prospective head position.
            ignore_tail: when True, exclude the last tail segment because
                         it moves away this tick (only valid when NOT growing).
        """
        body = self.body[:-1] if ignore_tail else self.body
        return cell in body