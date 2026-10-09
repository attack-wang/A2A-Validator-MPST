'''
food.py
Food item: random placement on free grid cells.
'''
import random
import settings
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize([])
    def randomize(self, occupied_cells):
        """Place food on a random cell not occupied by the snake."""
        free_cells = [
            (x, y)
            for x in range(settings.GRID_WIDTH)
            for y in range(settings.GRID_HEIGHT)
            if (x, y) not in occupied_cells
        ]
        if free_cells:
            self.position = random.choice(free_cells)
        else:
            self.position = None  # board full -> win condition
    def get_position(self):
        """Return the current food cell, or None if the board is full."""
        return self.position