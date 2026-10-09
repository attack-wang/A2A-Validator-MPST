'''
Food class representing the edible item on the board.
'''
import random
class Food:
    '''Represents a food item placed at a random free cell on the board.'''
    def __init__(self, grid_width, grid_height, snake_body=None):
        '''Initialize food and immediately place it on a free cell.'''
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = None
        self.respawn(snake_body or [])
    def respawn(self, snake_body):
        '''Move the food to a random cell not occupied by the snake.'''
        free_cells = [
            (x, y)
            for x in range(self.grid_width)
            for y in range(self.grid_height)
            if (x, y) not in snake_body
        ]
        self.position = random.choice(free_cells) if free_cells else None