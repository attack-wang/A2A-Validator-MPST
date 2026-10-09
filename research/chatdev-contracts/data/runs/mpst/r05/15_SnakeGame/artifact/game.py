'''
game.py
Defines the Game class, which manages the pygame window, the main game
loop, event handling, state updates, rendering, menus, and scoring.
'''
import pygame
import sys
from settings import (
    GRID_SIZE, CELL_SIZE, WINDOW_SIZE, FPS,
    COLOR_BACKGROUND, COLOR_GRID, COLOR_BORDER,
    COLOR_SNAKE_HEAD, COLOR_SNAKE_BODY, COLOR_FOOD,
    COLOR_TEXT, COLOR_TEXT_DIM, COLOR_MENU_HIGHLIGHT,
    DIFFICULTY_LEVELS, DEFAULT_DIFFICULTY,
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL,
    SCORE_PER_FOOD, HUD_HEIGHT,
)
from snake import Snake, UP, DOWN, LEFT, RIGHT
from food import Food
class Game:
    """Manages the full Snake game lifecycle: menu, gameplay, and game over."""
    STATE_MENU = "menu"
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_GAME_OVER = "game_over"
    def __init__(self):
        """Initialize pygame, the window, fonts, and the initial state."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + HUD_HEIGHT))
        pygame.display.set_caption("Classic Snake")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont(None, FONT_SIZE_LARGE, bold=True)
        self.font_medium = pygame.font.SysFont(None, FONT_SIZE_MEDIUM, bold=True)
        self.font_small = pygame.font.SysFont(None, FONT_SIZE_SMALL)
        self.difficulty_index = list(DIFFICULTY_LEVELS.keys()).index(DEFAULT_DIFFICULTY)
        self.difficulty_names = list(DIFFICULTY_LEVELS.keys())
        self.state = self.STATE_MENU
        self.reset_game()
    # ------------------------------------------------------------------
    # Game state management
    # ------------------------------------------------------------------
    def reset_game(self):
        """Reset the snake, food, score, and timers for a fresh game."""
        self.snake = Snake(GRID_SIZE)
        self.food = Food(GRID_SIZE, self.snake.body)
        self.score = 0
        self.move_interval = DIFFICULTY_LEVELS[self.current_difficulty()]
        self.time_since_move = 0
        self.game_over_reason = ""
    def current_difficulty(self):
        """Return the name of the currently selected difficulty."""
        return self.difficulty_names[self.difficulty_index]
    ...