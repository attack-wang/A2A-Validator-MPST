'''
food.py
Food item: random placement on free grid cells, avoiding the snake body.
'''
import random
import config
class Food:
    """A single food item placed on a random free cell of the board."""
    def __init__(self, grid_width, grid_height, snake):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = None
        self.respawn(snake)
    def respawn(self, snake):
        """Place the food on a random cell not occupied by the snake."""
        occupied = set(snake.body)
        free_cells = [
            (x, y)
            for x in range(self.grid_width)
            for y in range(self.grid_height)
            if (x, y) not in occupied
        ]
        self.position = random.choice(free_cells) if free_cells else None
    @property
    def exists(self):
        return self.position is not None