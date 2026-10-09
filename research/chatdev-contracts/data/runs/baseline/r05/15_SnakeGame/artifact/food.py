'''
food.py
Defines the Food entity that spawns at random free cells on the grid.
'''
import random
import config
class Food:
    '''
    Represents a single food item placed on a random free grid cell.
    '''
    def __init__(self, grid_width=config.GRID_WIDTH, grid_height=config.GRID_HEIGHT):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = None
        self.respawn([])
    def respawn(self, snake_body):
        '''
        Place the food on a random cell that is not occupied by the snake.
        If the snake fills the entire grid (win condition) no free cell
        exists and the position is set to None.
        '''
        free_cells = [
            (x, y)
            for x in range(self.grid_width)
            for y in range(self.grid_height)
            if (x, y) not in snake_body
        ]
        if not free_cells:
            self.position = None
        else:
            self.position = random.choice(free_cells)
    def get_position(self):
        '''Return the food cell (x, y), or None if the grid is full.'''
        return self.position