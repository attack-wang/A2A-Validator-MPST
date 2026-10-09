'''
snake.py
Snake entity for the Classic Snake game.
The snake keeps its body as an ordered list of (x, y) grid cells where
index 0 is the head. It supports direction changes (blocking illegal
180-degree reversals), stepping one cell per tick, growing after eating,
and self-collision detection.
'''
import settings
class Snake:
    """Player-controlled snake moving on a 2D grid."""
    def __init__(self, start_position, start_direction=settings.RIGHT,
                 initial_length=3):
        self.direction = start_direction
        self.pending_growth = 0
        x, y = start_position
        dx, dy = start_direction
        self.body = [
            (x - dx * i, y - dy * i) for i in range(initial_length)
        ]
    # Queries -----------------------------------------------------------
    @property
    def head(self):
        return self.body[0]
    @property
    def length(self):
        return len(self.body)
    def get_next_head(self):
        hx, hy = self.head
        dx, dy = self.direction
        return (hx + dx, hy + dy)
    def occupies(self, cell):
        return cell in self.body
    def collides_with_self(self, position):
        """True if `position` hits the body. The tail cell is excluded
        when it will vacate this tick (i.e. the snake is not growing)."""
        body = list(self.body)
        if self.pending_growth == 0 and len(body) > 1:
            body = body[:-1]
        return position in body
    # Commands ----------------------------------------------------------
    def set_direction(self, new_direction):
        """Accept a new direction unless it is identical or a 180-degree
        reversal. Returns True if the direction was accepted."""
        cx, cy = self.direction
        nx, ny = new_direction
        if (nx, ny) == (cx, cy):
            return False
        if (nx, ny) == (-cx, -cy):
            return False
        self.direction = (nx, ny)
        return True
    def move(self):
        """Advance one cell: insert the new head, drop the tail unless
        the snake still has pending growth."""
        new_head = self.get_next_head()
        self.body.insert(0, new_head)
        if self.pending_growth > 0:
            self.pending_growth -= 1
        else:
            self.body.pop()
        return new_head
    def grow(self, amount=1):
        self.pending_growth += amount