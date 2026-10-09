'''
snake.py
Defines the Snake entity: body management, movement, turning,
growth, self-collision detection and rendering.
'''
import pygame
import settings
class Snake:
    """Represents the player-controlled snake."""
    def __init__(self):
        """Initialize the snake with a default body and direction."""
        self.reset()
    def reset(self):
        """Reset the snake to its initial state (used on new game)."""
        start_x = settings.GRID_WIDTH // 2
        start_y = settings.GRID_HEIGHT // 2
        # Body is a list of (x, y) grid cells; head is the first element.
        self.body = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y),
        ]
        self.direction = settings.RIGHT
        self.next_direction = settings.RIGHT
        self.grow_pending = 0
    def get_head_position(self):
        """Return the grid coordinates of the snake's head."""
        return self.body[0]
    def turn(self, new_direction):
        """Queue a direction change, ignoring reversals and duplicates."""
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite and new_direction != self.direction:
            self.next_direction = new_direction
    def update(self):
        """Advance the snake one cell in its current direction."""
        self.direction = self.next_direction
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        # Insert new head at the front.
        self.body.insert(0, new_head)
        # Remove tail unless the snake still needs to grow.
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
    def grow(self, amount=1):
        """Schedule the snake to grow by `amount` cells."""
        self.grow_pending += amount
    def check_self_collision(self):
        """Return True if the head collides with any body segment."""
        return self.get_head_position() in self.body[1:]
    def check_boundary_collision(self):
        """Return True if the head is outside the playfield."""
        x, y = self.get_head_position()
        return not (0 <= x < settings.GRID_WIDTH and 0 <= y < settings.GRID_HEIGHT)
    def draw(self, surface):
        """Render every segment of the snake onto the given surface."""
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(
                x * settings.GRID_SIZE,
                y * settings.GRID_SIZE,
                settings.GRID_SIZE,
                settings.GRID_SIZE,
            )
            color = settings.COLOR_SNAKE_HEAD if i == 0 else settings.COLOR_SNAKE_BODY
            pygame.draw.rect(surface, color, rect)
            # Slight inner border for a cleaner look
            pygame.draw.rect(surface, settings.COLOR_BACKGROUND, rect, 1)