'''
snake.py
Snake entity: body management, direction queuing, movement and
collision queries for the Classic Snake game.
'''
import settings
class Snake:
    def __init__(self, initial_length=3):
        self.initial_length = initial_length
        self.reset()
    def reset(self):
        start_x = settings.GRID_WIDTH // 2
        start_y = settings.GRID_HEIGHT // 2
        self.direction = settings.DIR_RIGHT
        self.pending_directions = []
        self.body = [(start_x - i, start_y) for i in range(self.initial_length)]
    def get_head(self):
        """Return the current head cell."""
        return self.body[0]
    def get_body(self):
        """Return the list of body cells (head first)."""
        return self.body
    def get_length(self):
        """Return the current snake length in cells."""
        return len(self.body)
    def queue_direction(self, new_dir):
        """Queue a direction change, rejecting reversals and duplicates."""
        last_dir = self.pending_directions[-1] if self.pending_directions else self.direction
        if new_dir == last_dir:
            return
        # Reject a 180-degree turn (would instantly collide with the neck).
        if new_dir[0] == -last_dir[0] and new_dir[1] == -last_dir[1]:
            return
        if len(self.pending_directions) < 2:
            self.pending_directions.append(new_dir)
    def apply_queued_turn(self):
        """Consume the oldest queued direction, if any."""
        if self.pending_directions:
            self.direction = self.pending_directions.pop(0)
    def compute_next_head(self):
        """Return the cell the head will occupy after the next move."""
        dx, dy = self.direction
        head_x, head_y = self.body[0]
        return (head_x + dx, head_y + dy)
    def advance(self, grow=False):
        """Move head to computed next cell; keep tail if growing."""
        new_head = self.compute_next_head()
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()
        return new_head
    def occupies(self, point):
        """True if any body segment occupies the given cell."""
        return point in self.body
    def collides_with_point(self, point, ignore_tail=False):
        """True if the snake body collides with the point.
        When ignore_tail is True the tail cell is excluded because it
        will move away on the same tick (unless the snake is growing).
        """
        if ignore_tail and len(self.body) > 1:
            return point in self.body[:-1]
        return point in self.body