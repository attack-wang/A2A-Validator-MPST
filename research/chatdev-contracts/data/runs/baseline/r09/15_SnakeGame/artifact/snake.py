'''
snake.py
Defines the Snake entity for the Classic Snake game.
The snake keeps a list of grid positions (head first), a current direction
and a queue of pending direction changes so that fast successive key
presses are handled correctly. Growth is deferred by one step so the tail
keeps moving exactly like in the classic game.
'''
from collections import deque
import pygame  # FIX: pygame was used in draw() but never imported (NameError crash)
import settings
class Snake:
    '''Player-controlled snake: movement, growth and self-collision.'''
    def __init__(self):
        '''Create the snake in its default state.'''
        self.reset()
    def reset(self):
        '''Reset position, direction and length back to the initial state.'''
        center_x = settings.GRID_WIDTH // 2
        center_y = settings.GRID_HEIGHT // 2
        # Start with a three-segment snake moving to the right.
        self.positions = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
        ]
        self.direction = settings.RIGHT
        self.pending_directions = deque()
        self.grow_pending = 0
    def get_head_position(self):
        '''Return the grid position of the snake's head.'''
        return self.positions[0]
    def get_length(self):
        '''Return the current number of segments.'''
        return len(self.positions)
    def queue_direction(self, new_direction):
        '''
        Queue a direction change requested by the player.
        Reversals (180-degree turns) and duplicates are ignored, and at most
        two changes may wait in the queue so input stays responsive without
        allowing the snake to turn into itself between ticks.
        '''
        reference = self.pending_directions[-1] if self.pending_directions else self.direction
        is_reversal = (new_direction[0] == -reference[0] and new_direction[1] == -reference[1])
        is_duplicate = new_direction == reference
        if not is_reversal and not is_duplicate and len(self.pending_directions) < 2:
            self.pending_directions.append(new_direction)
    def update(self):
        '''
        Advance the snake one cell in its current direction.
        Applies the oldest queued direction change first. If growth is
        pending the tail is kept, otherwise the tail segment is removed.
        '''
        if self.pending_directions:
            self.direction = self.pending_directions.popleft()
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.positions.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()
    def grow(self, amount=1):
        '''Schedule the snake to grow by `amount` segments on the next moves.'''
        self.grow_pending += amount
    def check_self_collision(self):
        '''Return True when the head overlaps any body segment.'''
        return self.get_head_position() in self.positions[1:]
    def occupies(self, position):
        '''Return True when any segment of the snake is on `position`.'''
        return position in self.positions
    def draw(self, surface):
        '''Render every segment, with a distinct color for the head.'''
        for index, (x, y) in enumerate(self.positions):
            rect = pygame.Rect(
                x * settings.GRID_SIZE,
                y * settings.GRID_SIZE,
                settings.GRID_SIZE,
                settings.GRID_SIZE,
            )
            color = settings.COLOR_SNAKE_HEAD if index == 0 else settings.COLOR_SNAKE_BODY
            pygame.draw.rect(surface, color, rect)
            # Thin dark outline gives the classic segmented look.
            pygame.draw.rect(surface, settings.COLOR_BACKGROUND, rect, 1)