'''
snake.py
Snake entity: body management, directional movement, growth and
collision detection (walls and self-overlap).
'''
import pygame
from settings import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    UP, DOWN, LEFT, RIGHT,
    GREEN, DARK_GREEN, BLACK, WHITE,
)
class Snake:
    '''Player-controlled snake moving on a discrete grid.'''
    def __init__(self, start_length=3):
        '''Create a horizontal snake facing right at the board centre.'''
        self.start_length = max(1, start_length)
        self.color_head = GREEN
        self.color_body = DARK_GREEN
        self.reset()
    def reset(self):
        '''Restore the snake to its initial state (centre of the board).'''
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.positions = [(center_x - i, center_y) for i in range(self.start_length)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow_pending = 0
    # Queries
    def get_head_position(self):
        return self.positions[0]
    def get_length(self):
        return len(self.positions)
    # Commands
    def update_direction(self, direction):
        if direction in (UP, DOWN, LEFT, RIGHT):
            opposite = (-self.direction[0], -self.direction[1])
            if direction != opposite and direction != self.direction:
                self.next_direction = direction
    def grow(self, amount=1):
        self.grow_pending += amount
    def move(self):
        '''Advance one cell; returns False if the snake collides with itself or the wall.'''
        self.direction = self.next_direction
        head_x, head_y = self.get_head_position()
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        # Boundary collision
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            return False
        # Self collision: tail cell vacates this tick unless growing
        occupied = set(self.positions)
        if self.grow_pending == 0:
            occupied.discard(self.positions[-1])
        if new_head in occupied:
            return False
        self.positions.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()
        return True
    # Rendering
    def draw(self, surface):
        for index, (cx, cy) in enumerate(self.positions):
            rect = pygame.Rect(cx * GRID_SIZE, cy * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            color = self.color_head if index == 0 else self.color_body
            pygame.draw.rect(surface, color, rect.inflate(-2, -2), border_radius=4)
        self._draw_eyes(surface)
    def _draw_eyes(self, surface):
        hx, hy = self.get_head_position()
        center = (hx * GRID_SIZE + GRID_SIZE // 2, hy * GRID_SIZE + GRID_SIZE // 2)
        dx, dy = self.direction
        px, py = -dy, dx
        eye_offset = GRID_SIZE // 4
        forward = GRID_SIZE // 5
        for sign in (-1, 1):
            pos = (
                center[0] + dx * forward + px * eye_offset * sign,
                center[1] + dy * forward + py * eye_offset * sign,
            )
            pygame.draw.circle(surface, WHITE, (int(pos[0]), int(pos[1])), 2)