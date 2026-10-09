'''
Food item: random placement on the board avoiding the snake's body.
'''
import random
import settings
class Food:
    '''Represents a food item on the grid.'''
    def __init__(self, snake_body=None):
        self.position = (0, 0)
        self.randomize_position(snake_body or [])
    def randomize_position(self, snake_body):
        '''Place the food on a random free cell (not occupied by the snake).'''
        occupied = set(snake_body)
        free_cells = [
            (x, y)
            for x in range(settings.GRID_WIDTH)
            for y in range(settings.GRID_HEIGHT)
            if (x, y) not in occupied
        ]
        if free_cells:
            self.position = random.choice(free_cells)
        else:
            # Board completely filled - no valid spot (player has won)
            self.position = None
    @property
    def eaten(self):
        '''True when no free cell remains for food placement.'''
        return self.position is None