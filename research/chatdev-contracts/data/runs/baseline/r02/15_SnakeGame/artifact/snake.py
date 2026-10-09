'''
snake.py
Defines the Snake class: manages the snake's body segments, direction
changes (via an input queue), movement, growth, and collision detection
against itself and the board boundaries.
'''
import pygame
import settings
class Snake:
    """Grid-based snake controlled by directional input."""
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.reset()
    def reset(self):
        """Place the snake at the centre of the board facing right."""
        start_x = self.grid_width // 2
        start_y = self.grid_height // 2
        length = settings.INITIAL_SNAKE_LENGTH
        # Body is a list of (x, y) tuples, head first.
        self.body = [(start_x - i, start_y) for i in range(length)]
        self.direction = settings.RIGHT
        self.direction_queue = []
        self.grow_pending = 0
    @property
    def head(self):
        return self.body[0]
    def set_direction(self, new_direction):
        """Queue a direction change; 180-degree reversals are ignored.
        Queuing (instead of overwriting) ensures rapid successive presses
        (e.g. Up then Left within a single tick) are both honoured, and the
        reversal check uses the latest queued direction so the snake can
        never turn back into itself between ticks.
        """
        reference = self.direction_queue[-1] if self.direction_queue else self.direction
        if new_direction == reference or new_direction == (-reference[0], -reference[1]):
            return
        if len(self.direction_queue) < 3:
            self.direction_queue.append(new_direction)
    def move(self):
        """Advance the snake one cell in its current direction."""
        if self.direction_queue:
            self.direction = self.direction_queue.pop(0)
        head_x, head_y = self.head
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
        return new_head
    def grow(self, amount=1):
        """Schedule the snake to grow by `amount` cells on future moves."""
        self.grow_pending += amount
    def hits_self(self):
        """True if the head overlaps any body segment."""
        return self.head in self.body[1:]
    def hits_boundary(self):
        """True if the head is outside the playfield."""
        x, y = self.head
        return not (0 <= x < self.grid_width and 0 <= y < self.grid_height)
    def occupies(self, position):
        """True if any segment of the snake occupies `position`."""
        return position in self.body
    def draw(self, surface):
        """Render every segment as a coloured rectangle."""
        for index, (x, y) in enumerate(self.body):
            rect = pygame.Rect(
                x * settings.GRID_SIZE,
                y * settings.GRID_SIZE,
                settings.GRID_SIZE,
                settings.GRID_SIZE,
            )
            if index == 0:
                color = settings.COLOR_SNAKE_HEAD
            else:
                color = settings.COLOR_SNAKE_BODY if index % 2 else settings.COLOR_SNAKE_BODY_ALT
            pygame.draw.rect(surface, color, rect)
            # small inner border for a nicer look
            pygame.draw.rect(surface, settings.COLOR_BACKGROUND, rect.inflate(-2, -2), 1)