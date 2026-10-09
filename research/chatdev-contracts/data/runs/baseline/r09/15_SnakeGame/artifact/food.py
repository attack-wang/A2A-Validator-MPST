'''
food.py
Defines the Food item for the Classic Snake game.
Food spawns on a random free grid cell (a cell not occupied by the snake)
and is re-randomized every time it is eaten.
'''
import random
import pygame
import settings
class Food:
    '''A single food item placed on a random free cell of the board.'''
    def __init__(self, snake_body):
        '''Spawn the food on a cell that is not occupied by `snake_body`.'''
        self.position = None
        self.randomize_position(snake_body)
    def randomize_position(self, snake_body):
        '''
        Move the food to a random cell not occupied by the snake.
        If the snake fills the whole board (win condition) the position is
        set to None and the food is simply not drawn anymore.
        '''
        occupied = set(snake_body)
        free_cells = [
            (x, y)
            for x in range(settings.GRID_WIDTH)
            for y in range(settings.GRID_HEIGHT)
            if (x, y) not in occupied
        ]
        self.position = random.choice(free_cells) if free_cells else None
    def draw(self, surface):
        '''Render the food as a red cell with a small inner highlight.'''
        if self.position is None:
            return
        x, y = self.position
        rect = pygame.Rect(
            x * settings.GRID_SIZE,
            y * settings.GRID_SIZE,
            settings.GRID_SIZE,
            settings.GRID_SIZE,
        )
        pygame.draw.rect(surface, settings.COLOR_FOOD, rect)
        inner = rect.inflate(-settings.GRID_SIZE // 2, -settings.GRID_SIZE // 2)
        pygame.draw.rect(surface, settings.COLOR_HIGHLIGHT, inner)