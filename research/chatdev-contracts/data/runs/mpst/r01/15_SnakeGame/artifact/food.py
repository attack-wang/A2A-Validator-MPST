'''
food.py
Defines the Food class, which spawns food items on random free cells
of the board while avoiding cells occupied by the snake's body.
'''
import random
import pygame
from config import (
    GRID_WIDTH,
    GRID_HEIGHT,
    CELL_SIZE,
    COLOR_FOOD,
    COLOR_FOOD_OUTLINE,
)
class Food:
    """A food item placed on a random cell not occupied by the snake."""
    def __init__(self, snake_body):
        """Spawn the food on a free cell, given the snake's current body."""
        self.position = self.randomize_position(snake_body)
    def randomize_position(self, snake_body):
        """
        Pick a uniformly random cell that is not occupied by the snake.
        Returns an (x, y) tuple, or None if the board has no free cell.
        """
        occupied = set(snake_body)
        free_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in occupied
        ]
        if not free_cells:
            return None
        return random.choice(free_cells)
    def draw(self, surface):
        """Render the food as a circle centered in its cell."""
        if self.position is None:
            return
        x, y = self.position
        center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
        radius = CELL_SIZE // 2 - 2
        pygame.draw.circle(surface, COLOR_FOOD, center, radius)
        pygame.draw.circle(surface, COLOR_FOOD_OUTLINE, center, radius, 1)