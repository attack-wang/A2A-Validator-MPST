'''
food.py
Food item that spawns at a random free cell on the board, never overlapping
the snake's body.
'''
import random
class Food:
    '''A single food item placed on a random unoccupied grid cell.'''
    def __init__(self, grid_width, grid_height, snake_body):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = None
        self.randomize_position(snake_body)
    def randomize_position(self, snake_body):
        '''Move the food to a random cell not occupied by the snake.
        If the snake fills the entire board, position becomes None and the
        game should treat this as a victory condition.
        '''
        occupied = set(snake_body)
        free_cells = [
            (x, y)
            for x in range(self.grid_width)
            for y in range(self.grid_height)
            if (x, y) not in occupied
        ]
        if not free_cells:
            self.position = None
        else:
            self.position = random.choice(free_cells)
    @property
    def exists(self):
        return self.position is not None