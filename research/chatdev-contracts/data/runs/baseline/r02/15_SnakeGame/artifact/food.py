'''
food.py
Defines the Food class: spawns food at random free cells on the board
and renders it.
'''
import random
import pygame
import settings
class Food:
    """A single food item placed on a random free grid cell."""
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = (0, 0)
        self.randomize_position([])
    def randomize_position(self, occupied):
        """Move the food to a random cell not contained in `occupied`.
        Returns True if a free cell was found, False if the board is full
        (i.e. the snake fills the entire playfield and the player wins).
        """
        occupied_set = set(occupied)
        free_cells = [
            (x, y)
            for x in range(self.grid_width)
            for y in range(self.grid_height)
            if (x, y) not in occupied_set
        ]
        if not free_cells:
            return False
        self.position = random.choice(free_cells)
        return True
    def get_position(self):
        return self.position
    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(
            x * settings.GRID_SIZE,
            y * settings.GRID_SIZE,
            settings.GRID_SIZE,
            settings.GRID_SIZE,
        )
        pygame.draw.rect(surface, settings.COLOR_FOOD, rect.inflate(-4, -4), border_radius=4)