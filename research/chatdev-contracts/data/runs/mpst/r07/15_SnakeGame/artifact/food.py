'''
food.py
Food item: random placement on the board.
'''
import random
import pygame
from settings import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, FOOD_COLOR, FOOD_OUTLINE
class Food:
    """Represents a food item placed at a random free cell."""
    def __init__(self, snake_body):
        """Place the initial food away from the snake."""
        self.position = (0, 0)
        self.randomize_position(snake_body)
    def randomize_position(self, snake_body):
        """Place the food on a random cell not occupied by the snake."""
        free_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in snake_body
        ]
        self.position = random.choice(free_cells) if free_cells else None
    def get_position(self):
        """Return the current food position (None if the board is full)."""
        return self.position
    def draw(self, surface):
        """Render the food as a circle on the given surface."""
        if self.position is None:
            return
        cx = self.position[0] * GRID_SIZE + GRID_SIZE // 2
        cy = self.position[1] * GRID_SIZE + GRID_SIZE // 2
        radius = GRID_SIZE // 2 - 2
        pygame.draw.circle(surface, FOOD_COLOR, (cx, cy), radius)
        pygame.draw.circle(surface, FOOD_OUTLINE, (cx, cy), radius, 2)