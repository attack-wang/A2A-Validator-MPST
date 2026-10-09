'''
snake.py
Defines the Snake class, which manages the snake's body, movement,
direction changes, growth, and self-collision detection.
'''
import pygame
# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
class Snake:
    """Represents the player-controlled snake on the game board."""
    def __init__(self, grid_size, start_position=None):
        """Initialize the snake with a starting body and direction."""
        self.grid_size = grid_size
        if start_position is None:
            start_position = (grid_size // 2, grid_size // 2)
        self.body = [start_position,
                     (start_position[0] - 1, start_position[1]),
                     (start_position[0] - 2, start_position[1])]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow_pending = 0
    def get_head_position(self):
        """Return the grid coordinates of the snake's head."""
        return self.body[0]
    def change_direction(self, new_direction):
        """Queue a direction change, preventing direct 180-degree reversals."""
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite and new_direction != self.direction:
            self.next_direction = new_direction
    def move(self):
        """Advance the snake one cell in its current direction."""
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
        """Schedule the snake to grow by the given number of cells."""
        self.grow_pending += amount
    def check_self_collision(self):
        """Return True if the head collides with any part of the body."""
        head = self.get_head_position()
        return head in self.body[1:]
    def check_boundary_collision(self):
        """Return True if the head is outside the grid boundaries."""
        head = self.get_head_position()
        x, y = head
        return x < 0 or y < 0 or x >= self.grid_size or y >= self.grid_size
    def occupies(self, position):
        """Return True if any part of the snake occupies the given cell."""
        return position in self.body
    def draw(self, surface, cell_size, head_color, body_color):
        """Render the snake onto the given pygame surface."""
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            color = head_color if i == 0 else body_color
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)