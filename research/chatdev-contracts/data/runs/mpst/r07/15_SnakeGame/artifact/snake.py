'''
snake.py
Snake entity: movement, direction buffering, growth, and rendering.
'''
import pygame
from settings import (GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, RIGHT,
                      HEAD_COLOR, BODY_COLOR, OUTLINE_COLOR)
class Snake:
    """Snake controlled by the player: moves on a grid and grows when eating."""
    def __init__(self):
        """Create the snake with its default starting position."""
        self.reset()
    def reset(self):
        """Place a 3-segment snake at the board center moving right."""
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [
            (start_x - 2, start_y),
            (start_x - 1, start_y),
            (start_x, start_y),
        ]
        self.direction = RIGHT
        self.direction_queue = []
        self.grow_pending = 0
    @property
    def head(self):
        """Return the head segment (last element of body)."""
        return self.body[-1]
    @property
    def length(self):
        """Return the number of segments."""
        return len(self.body)
    def change_direction(self, direction):
        """Queue a direction change, rejecting reversals and duplicates."""
        last = self.direction_queue[-1] if self.direction_queue else self.direction
        if direction == last or direction == (-last[0], -last[1]):
            return
        if len(self.direction_queue) < 2:
            self.direction_queue.append(direction)
    def update(self):
        """Move one cell; return False on wall or self collision."""
        if self.direction_queue:
            self.direction = self.direction_queue.pop(0)
        head_x, head_y = self.head
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            return False  # Wall collision
        body_to_check = self.body if self.grow_pending > 0 else self.body[:-1]
        if new_head in body_to_check:
            return False  # Self collision
        self.body.append(new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop(0)
        return True
    def draw(self, surface):
        """Render every segment; the head uses a brighter color."""
        for i, segment in enumerate(self.body):
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE,
                               GRID_SIZE, GRID_SIZE)
            color = HEAD_COLOR if i == len(self.body) - 1 else BODY_COLOR
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, OUTLINE_COLOR, rect, 1)