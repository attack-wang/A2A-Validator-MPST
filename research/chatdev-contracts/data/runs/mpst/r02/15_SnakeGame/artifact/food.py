'''
Food class: represents the food items the snake eats, handling
random placement on the board and rendering.
'''
import random
import pygame
from settings import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, HUD_HEIGHT, COLOR_FOOD
class Food:
    def __init__(self, snake_positions):
        self.position = (0, 0)
        self.randomize_position(snake_positions)
    def randomize_position(self, snake_positions):
        """Place food on a random grid cell not occupied by the snake."""
        occupied = set(snake_positions)
        free_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in occupied
        ]
        if free_cells:
            self.position = random.choice(free_cells)
        # If no free cell exists the board is full; the victory check in
        # game.update() fires before this method is called, so keeping the
        # current position is a safe fallback that can never hang.
    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, HUD_HEIGHT + y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, COLOR_FOOD, rect)
        # Small highlight to make the food look like an apple
        pygame.draw.circle(surface, (255, 255, 255), (rect.centerx - 3, rect.centery - 3), 2)