'''
food.py
Defines the Food entity: random spawning on the grid while avoiding
cells occupied by the snake's body.
'''
import random
class Food:
    """Represents a single food item on the grid."""
    def __init__(self, grid_width, grid_height):
        """Store grid dimensions; food position is unset until spawned."""
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = None
    def spawn(self, occupied_cells):
        """Place food on a random free cell (not in `occupied_cells`).
        Returns True on success, or False when no free cell remains
        (i.e. the snake fills the whole board).
        """
        occupied = set(occupied_cells)
        free_cells = [
            (x, y)
            for x in range(self.grid_width)
            for y in range(self.grid_height)
            if (x, y) not in occupied
        ]
        if not free_cells:
            self.position = None
            return False
        self.position = random.choice(free_cells)
        return True
    def get_position(self):
        """Return the food's grid position, or None if not spawned."""
        return self.position