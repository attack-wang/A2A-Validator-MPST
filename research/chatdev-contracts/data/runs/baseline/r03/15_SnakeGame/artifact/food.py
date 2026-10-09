'''
food.py
Defines the Food entity for the Snake game.
Food spawns at a random free cell on the board (never on top of
the snake). If no free cell remains, the position is set to None,
which the Game interprets as a victory condition (the snake has
filled the entire board).
'''
import random
import settings
class Food:
    """A food item that the snake eats to grow and score."""
    def __init__(self):
        self.position = None
    def randomize_position(self, snake_body):
        """
        Place the food on a random cell not occupied by the snake.
        Returns True if a position was found, False when the board
        is completely full (victory condition).
        """
        occupied = set(snake_body)
        free_cells = [
            (x, y)
            for x in range(settings.GRID_WIDTH)
            for y in range(settings.GRID_HEIGHT)
            if (x, y) not in occupied
        ]
        if not free_cells:
            self.position = None
            return False
        self.position = random.choice(free_cells)
        return True
    def get_position(self):
        """Return the food's (x, y) grid position (may be None)."""
        return self.position