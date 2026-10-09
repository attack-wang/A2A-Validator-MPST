'''
snake.py
Defines the Snake entity: body storage, direction handling (with
reversal protection), movement, growth, and self-collision detection.
'''
class Snake:
    """Represents the player-controlled snake on the grid."""
    def __init__(self, start_x, start_y, initial_length=3):
        """Create a snake of `initial_length` segments with its head at
        (start_x, start_y), extending leftwards, initially moving right."""
        self.body = [(start_x - i, start_y) for i in range(initial_length)]
        self.direction = (1, 0)          # Currently applied direction
        self.pending_direction = (1, 0)  # Direction applied on next move
        self.grow_pending = False        # If True, next move keeps the tail
    def update_direction(self, new_direction):
        """Queue a direction change, ignoring 180-degree reversals."""
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite and new_direction != self.direction:
            self.pending_direction = new_direction
    def move(self):
        """Advance one cell in the pending direction.
        Inserts a new head; pops the tail unless a growth is pending.
        Returns the new head position (x, y).
        """
        self.direction = self.pending_direction
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        if self.grow_pending:
            self.grow_pending = False   # Keep tail: snake grows by one
        else:
            self.body.pop()
        return new_head
    def grow(self):
        """Schedule growth: the tail is retained on the next move."""
        self.grow_pending = True
    def check_self_collision(self):
        """Return True if the head overlaps any body segment."""
        return self.body[0] in self.body[1:]
    def get_head_position(self):
        """Return the head's grid position."""
        return self.body[0]
    def get_body(self):
        """Return the list of all body segments (head first)."""
        return self.body