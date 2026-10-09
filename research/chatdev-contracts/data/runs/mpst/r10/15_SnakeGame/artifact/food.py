'''
food.py
Food item for the Classic Snake game.
Food spawns at a random free cell (never on the snake). When the
board is full the respawn reports failure so the game can declare
a victory.
'''
import random
class Food:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self._position = None
    def respawn(self, snake):
        occupied = set(snake.body)
        free_cells = [
            (x, y)
            for x in range(self.grid_width)
            for y in range(self.grid_height)
            if (x, y) not in occupied
        ]
        if not free_cells:
            self._position = None
            return False
        self._position = random.choice(free_cells)
        return True
    @property
    def position(self):
        return self._position