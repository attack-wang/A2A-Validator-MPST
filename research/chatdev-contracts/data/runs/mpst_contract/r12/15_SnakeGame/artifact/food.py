import random

from settings import COLS, ROWS


class Food:
    def __init__(self, snake):
        self.pos = None
        self.respawn(snake)

    def respawn(self, snake):
        occupied = set(snake.body)
        free = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in occupied]
        self.pos = random.choice(free) if free else None