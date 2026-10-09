'''
food.py
Food item that spawns at random free cells of the board.
'''
import random
import settings
class Food:
    """A single food item placed on a random free grid cell."""
    def __init__(self, snake):
        self.position = None
        self.respawn(snake)
    def respawn(self, snake):
        """Move the food to a random cell not occupied by the snake."""
        free_cells = [
            (x, y)
            for x in range(settings.BOARD_WIDTH)
            for y in range(settings.BOARD_HEIGHT)
            if not snake.occupies((x, y))
        ]
        if not free_cells:
            # Board completely filled - player has won!
            self.position = None
            return
        self.position = random.choice(free_cells)