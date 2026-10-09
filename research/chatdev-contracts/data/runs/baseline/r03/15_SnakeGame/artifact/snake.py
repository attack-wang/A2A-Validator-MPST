'''
snake.py
Defines the Snake entity for the Snake game.
The Snake class manages:
  * the body as a list of (x, y) grid cells (index 0 = head),
  * buffered direction changes (prevents 180-degree reversals
    and multiple turns within a single move step),
  * growth scheduling when food is eaten,
  * self-collision detection.
'''
import settings
class Snake:
    """Player-controlled snake composed of grid-aligned segments."""
    def __init__(self, start_x=None, start_y=None):
        """
        Create a snake. It spawns at the board center (or at the
        given grid coordinates) facing right, three segments long.
        """
        if start_x is None:
            start_x = settings.GRID_WIDTH // 2
        if start_y is None:
            start_y = settings.GRID_HEIGHT // 2
        self.start_position = (start_x, start_y)
        self.reset()
    def reset(self):
        """Restore the snake to its initial spawn state."""
        x, y = self.start_position
        self.body = [(x, y), (x - 1, y), (x - 2, y)]
        self.direction = settings.RIGHT
        self.next_direction = settings.RIGHT
        self.grow_pending = 0
    def get_head_position(self):
        """Return the (x, y) grid coordinates of the head segment."""
        return self.body[0]
    def get_body(self):
        """Return the full list of body segments (head first)."""
        return self.body
    def get_length(self):
        """Return the current number of segments."""
        return len(self.body)
    def set_direction(self, new_direction):
        """
        Queue a direction change for the next move step.
        Rules enforced:
          * The snake cannot reverse 180 degrees into itself.
          * Only one turn may be buffered per move step, which
            prevents players from turning twice inside a single
            tick and clipping through their own neck.
        """
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction == opposite:
            return
        if self.next_direction == self.direction:
            self.next_direction = new_direction
    def update(self):
        """
        Advance the snake one cell in the buffered direction.
        The new head is inserted at the front of the body; the tail
        is removed unless growth is pending. The new head position
        is returned so the Game can validate boundaries.
        """
        self.direction = self.next_direction
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
        return new_head
    def grow(self, amount=1):
        """Schedule the snake to grow by `amount` extra segments."""
        self.grow_pending += amount
    def check_self_collision(self):
        """Return True if the head overlaps any other body segment."""
        head = self.get_head_position()
        return head in self.body[1:]