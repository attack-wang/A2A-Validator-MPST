'''
snake.py
Defines the Snake class, which manages the snake's body segments,
current movement direction, queued direction changes, movement,
growth, and self-collision detection.
'''
import pygame
from config import (
    CELL_SIZE,
    COLOR_SNAKE_HEAD,
    COLOR_SNAKE_BODY,
    COLOR_SNAKE_OUTLINE,
)
class Snake:
    """Player-controlled snake composed of grid-aligned segments."""
    def __init__(self, start_position, start_direction, initial_length=3):
        """
        Create a snake whose head starts at `start_position` (x, y) grid
        cell, moving in `start_direction`, with a body that trails
        opposite to the direction of travel.
        """
        self.direction = start_direction
        self.direction_queue = []
        self.grow_pending = 0
        self.body = []
        dx, dy = start_direction
        head_x, head_y = start_position
        for i in range(initial_length):
            self.body.append((head_x - dx * i, head_y - dy * i))
    def change_direction(self, new_direction):
        """
        Queue a direction change. Reversals (180-degree turns) and
        duplicates of the pending direction are ignored so the snake
        can never turn back into itself between moves.
        """
        last = self.direction_queue[-1] if self.direction_queue else self.direction
        opposite = (-last[0], -last[1])
        if new_direction == opposite or new_direction == last:
            return
        if len(self.direction_queue) < 3:
            self.direction_queue.append(new_direction)
    def move(self):
        """
        Advance one cell in the current direction, applying any queued
        turn first. The tail is removed unless growth is pending.
        Returns the new head position as an (x, y) tuple.
        """
        if self.direction_queue:
            self.direction = self.direction_queue.pop(0)
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
        return new_head
    def grow(self, amount=1):
        """Schedule the snake to grow by `amount` segments on future moves."""
        self.grow_pending += amount
    def check_self_collision(self):
        """Return True if the head overlaps any other body segment."""
        return self.body[0] in self.body[1:]
    def get_head_position(self):
        """Return the (x, y) grid cell of the snake's head."""
        return self.body[0]
    def occupies(self, cell):
        """Return True if any segment occupies the given grid cell."""
        return cell in self.body
    def draw(self, surface):
        """Render every segment, highlighting the head."""
        for index, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = COLOR_SNAKE_HEAD if index == 0 else COLOR_SNAKE_BODY
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, COLOR_SNAKE_OUTLINE, rect, 1)