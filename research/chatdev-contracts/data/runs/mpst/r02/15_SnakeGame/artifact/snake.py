'''
Snake class: represents the player-controlled snake, handling movement,
growth, direction changes, and collision detection.
'''
import pygame
from settings import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, HUD_HEIGHT,
    COLOR_BACKGROUND, COLOR_SNAKE_HEAD, COLOR_SNAKE_BODY,
    MAX_DIRECTION_QUEUE,
)
class Snake:
    def __init__(self):
        # Start in the middle with 3 segments moving right
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.positions = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = (1, 0)  # moving right
        self.direction_queue = []  # buffered direction changes
        self.grow_pending = 0
    def get_head_position(self):
        return self.positions[0]
    def change_direction(self, new_direction):
        # Validate against the most recent effective direction: the last
        # queued turn if one is pending, otherwise the current direction.
        last = self.direction_queue[-1] if self.direction_queue else self.direction
        # Reject reversals (would hit the neck), duplicates, and cap the
        # queue so stale inputs cannot accumulate.
        if (new_direction[0] * -1, new_direction[1] * -1) != last and new_direction != last:
            if len(self.direction_queue) < MAX_DIRECTION_QUEUE:
                self.direction_queue.append(new_direction)
    def update(self):
        # Apply one buffered direction per tick, then advance the head
        # one cell. No wrapping: leaving the grid is a boundary collision.
        if self.direction_queue:
            self.direction = self.direction_queue.pop(0)
        head_x, head_y = self.get_head_position()
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.positions.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()
    def grow(self):
        self.grow_pending += 1
    def check_boundary_collision(self):
        head_x, head_y = self.get_head_position()
        return head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT
    def check_self_collision(self):
        # The tail cell is vacated on the same tick unless growing,
        # so only compare against the rest of the body.
        return self.get_head_position() in self.positions[1:]
    def draw(self, surface):
        for i, (x, y) in enumerate(self.positions):
            rect = pygame.Rect(x * GRID_SIZE, HUD_HEIGHT + y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, COLOR_BACKGROUND, rect, 1)  # segment outline
        self._draw_eyes(surface)
    def _draw_eyes(self, surface):
        # Draw eyes on the head, offset based on the current direction
        head_x, head_y = self.get_head_position()
        cx = head_x * GRID_SIZE + GRID_SIZE // 2
        cy = HUD_HEIGHT + head_y * GRID_SIZE + GRID_SIZE // 2
        dx, dy = self.direction
        # Perpendicular offset for the two eyes
        px, py = -dy, dx
        offset_along = GRID_SIZE // 4
        offset_side = GRID_SIZE // 4
        eye1 = (cx + dx * offset_along + px * offset_side, cy + dy * offset_along + py * offset_side)
        eye2 = (cx + dx * offset_along - px * offset_side, cy + dy * offset_along - py * offset_side)
        radius = 2
        for eye in (eye1, eye2):
            pygame.draw.circle(surface, (255, 255, 255), eye, radius)
            pygame.draw.circle(surface, (0, 0, 0), eye, 1)