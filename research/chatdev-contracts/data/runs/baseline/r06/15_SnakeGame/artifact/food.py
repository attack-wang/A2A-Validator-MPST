'''
food.py
Defines the Food entity: random placement on free grid cells and rendering.
'''
import random
import pygame
import settings
class Food:
    """Represents a single food item on the board."""
    def __init__(self, snake_body):
        """Place the food at a random free cell, avoiding the snake."""
        self.randomize_position(snake_body)
    def randomize_position(self, snake_body):
        """Choose a random grid cell that is not occupied by the snake."""
        occupied = set(snake_body)
        free_cells = [
            (x, y)
            for x in range(settings.GRID_WIDTH)
            for y in range(settings.GRID_HEIGHT)
            if (x, y) not in occupied
        ]
        # If there is no free cell the board is full (win condition).
        self.position = random.choice(free_cells) if free_cells else None
    def draw(self, surface):
        """Render the food item onto the given surface."""
        if self.position is None:
            return
        x, y = self.position
        rect = pygame.Rect(
            x * settings.GRID_SIZE + 2,
            y * settings.GRID_SIZE + 2,
            settings.GRID_SIZE - 4,
            settings.GRID_SIZE - 4,
        )
        pygame.draw.rect(surface, settings.COLOR_FOOD, rect, border_radius=4)