'''
food.py
Defines the Food class, which handles food placement on the board,
avoiding positions occupied by the snake, and renders food as a circle.
'''
import random
import pygame
class Food:
    """Represents a food item placed at a random free cell on the board."""
    def __init__(self, grid_size, snake_body):
        """Initialize food at a random position not occupied by the snake."""
        self.grid_size = grid_size
        self.position = (0, 0)
        self.randomize_position(snake_body)
    def randomize_position(self, snake_body):
        """Place food at a random free cell; return False if none remain."""
        free_cells = [
            (x, y)
            for x in range(self.grid_size)
            for y in range(self.grid_size)
            if (x, y) not in snake_body
        ]
        if not free_cells:
            return False
        self.position = random.choice(free_cells)
        return True
    def get_position(self):
        """Return the grid coordinates of the food."""
        return self.position
    def draw(self, surface, cell_size, color):
        """Render the food as a circle onto the given pygame surface."""
        x, y = self.position
        center = (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2)
        radius = cell_size // 2 - 3
        pygame.draw.circle(surface, color, center, radius)