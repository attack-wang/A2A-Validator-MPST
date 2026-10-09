'''
food.py
Defines the Food entity for the Classic Snake game.
A food item occupies a single grid cell. Placement is randomized over all
cells that are not currently occupied by the snake, guaranteeing the food is
always reachable and never spawns inside the snake's body.
'''
import random
import settings
class Food:
    '''A single food item placed on a free cell of the board.'''
    def __init__(self, snake_body=None):
        '''Place the initial food item, avoiding the snake's body cells.'''
        self.position = (0, 0)
        self.randomize_position(snake_body if snake_body is not None else [])
    def randomize_position(self, snake_body):
        '''
        Move the food to a uniformly random unoccupied cell.
        Returns True if a free cell was found, False when the snake fills
        the whole board (i.e. the player has won).
        '''
        occupied = set(snake_body)
        free_cells = [
            (x, y)
            for x in range(settings.GRID_WIDTH)
            for y in range(settings.GRID_HEIGHT)
            if (x, y) not in occupied
        ]
        if not free_cells:
            return False
        self.position = random.choice(free_cells)
        return True