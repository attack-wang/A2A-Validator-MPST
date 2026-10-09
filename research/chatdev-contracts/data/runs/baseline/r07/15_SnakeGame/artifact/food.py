'''
food.py
Food item: random placement on free cells and rendering.
'''
import random
import pygame
from settings import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, RED, DARK_GRAY
class Food:
    '''A single food item placed on a random free grid cell.'''
    def __init__(self, occupied_cells=None):
        '''Place the food on a random cell that is not occupied.'''
        self.color = RED
        self.randomize_position(occupied_cells or [])
    def randomize_position(self, occupied_cells):
        '''Move the food to a random cell outside ``occupied_cells``.'''
        occupied = set(occupied_cells)
        free_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in occupied
        ]
        if free_cells:
            self.position = random.choice(free_cells)
        else:
            self.position = None
    def get_position(self):
        return self.position
    def draw(self, surface):
        '''Render the food as a small apple-like circle.'''
        if self.position is None:
            return
        cx, cy = self.position
        center = (cx * GRID_SIZE + GRID_SIZE // 2, cy * GRID_SIZE + GRID_SIZE // 2)
        radius = GRID_SIZE // 2 - 3
        pygame.draw.circle(surface, self.color, center, radius)
        pygame.draw.line(surface, DARK_GRAY, (center[0], center[1] - radius),
                         (center[0] + 3, center[1] - radius - 3), 2)