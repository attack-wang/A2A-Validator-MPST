'''
snake.py
Snake entity for the Classic Snake game.
...
'''
from collections import deque
from settings import START_DIRECTION
class Snake:
    def __init__(self, start_position, initial_length=3, start_direction=START_DIRECTION):
        self.initial_position = start_position
        self.initial_length = max(1, initial_length)
        self.initial_direction = start_direction
        self.reset()
    def reset(self):
        x, y = self.initial_position
        dx, dy = self.initial_direction
        self.body = deque((x - dx * i, y - dy * i) for i in range(self.initial_length))
        self.direction = self.initial_direction
        self.pending_direction = self.initial_direction
        self.growth_pending = 0
    def change_direction(self, new_direction):
        if new_direction == self.direction or new_direction == self.pending_direction:
            return False
        if (new_direction[0] == -self.direction[0] and new_direction[1] == -self.direction[1]):
            return False
        self.pending_direction = new_direction
        return True
    def move(self):
        self.direction = self.pending_direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.appendleft(new_head)
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.body.pop()
        return new_head
    def grow(self, amount=1):
        self.growth_pending += amount
    def check_self_collision(self):
        head = self.body[0]
        return any(segment == head for i, segment in enumerate(self.body) if i > 0)
    def occupies(self, cell):
        return cell in self.body
    @property
    def head(self):
        return self.body[0]
    @property
    def length(self):
        return len(self.body)