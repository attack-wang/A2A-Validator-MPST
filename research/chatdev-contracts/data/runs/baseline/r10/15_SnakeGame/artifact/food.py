'''
food.py
Food item for the Classic Snake game.
Food spawns on a random free grid cell (never on top of the snake).
'''
import random
class Food:
    """A single food item placed somewhere on the grid."""
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = (0, 0)
    def respawn(self, occupied_cells):
        """
        Move the food to a random cell not listed in `occupied_cells`.
        Returns True on success, or False when no free cell remains
        (i.e. the snake fills the whole board — a win condition).
        """
        occupied = set(occupied_cells)
        free_cells = [
            (x, y)
            for x in range(self.grid_width)
            for y in range(self.grid_height)
            if (x, y) not in occupied
        ]
        if not free_cells:
            return False
        self.position = random.choice(free_cells)
        return True