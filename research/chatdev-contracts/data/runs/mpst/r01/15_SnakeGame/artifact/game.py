'''
game.py
Defines the Game class, which manages the game window, main loop,
state transitions (menu, playing, game over), scoring, rendering,
and difficulty selection.
'''
import sys
import pygame
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, HUD_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT,
    GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, FPS,
    COLOR_BACKGROUND, COLOR_GRID, COLOR_BORDER, COLOR_TEXT,
    COLOR_MENU_TITLE, COLOR_MENU_HIGHLIGHT,
    DIFFICULTY_LEVELS, SCORE_PER_FOOD,
    UP, DOWN, LEFT, RIGHT,
)
from snake import Snake
from food import Food
class Game:
    """Main application class: owns the window, loop, and game states."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Classic Snake")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont("consolas", 18)
        self.font_medium = pygame.font.SysFont("consolas", 24, bold=True)
        self.font_large = pygame.font.SysFont("consolas", 40, bold=True)
        self.state = "menu"          # 'menu' | 'playing' | 'game_over'
        self.difficulty_name = "Medium"
        self.move_interval = DIFFICULTY_LEVELS[self.difficulty_name]
        self.reset_game()
    def reset_game(self):
        """Initialize a fresh snake, food, and score for a new round."""
        start = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.snake = Snake(start, RIGHT, initial_length=3)
        self.food = Food(self.snake.body)
        self.score = 0
        self.move_timer = 0.0
    # ----- state transitions -----
    def start_game(self, difficulty_name):
        """Begin a new round with the chosen difficulty."""
        self.difficulty_name = difficulty_name
        self.move_interval = DIFFICULTY_LEVELS[difficulty_name]
        self.reset_game()
        self.state = "playing"
    def game_over(self):
        """Switch to the game-over state."""
        self.state = "game_over"
    # ----- input -----
    def handle_events(self):
        """Process the event queue according to the current state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
    def handle_keydown(self, key):
        """Dispatch key presses to the handler for the current state."""
        if self.state == "menu":
            self.handle_menu_key(key)
        elif self.state == "playing":
            self.handle_playing_key(key)
        elif self.state == "game_over":
            self.handle_game_over_key(key)
    def handle_menu_key(self, key):
        """Difficulty selection: 1/2/3 or Up/Down + Enter."""
        names = list(DIFFICULTY_LEVELS.keys())
        if key in (pygame.K_1, pygame.K_KP1):
            self.start_game(names[0])
        elif key in (pygame.K_2, pygame.K_KP2):
            self.start_game(names[1])
        elif key in (pygame.K_3, pygame.K_KP3):
            self.start_game(names[2])
        elif key in (pygame.K_UP, pygame.K_w):
            idx = names.index(self.difficulty_name)
            self.difficulty_name = names[(idx - 1) % len(names)]
        elif key in (pygame.K_DOWN, pygame.K_s):
            idx = names.index(self.difficulty_name)
            self.difficulty_name = names[(idx + 1) % len(names)]
        elif key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self.start_game(self.difficulty_name)
    def handle_playing_key(self, key):
        """Directional controls plus pause."""
        if key in (pygame.K_UP, pygame.K_w):
            self.snake.change_direction(UP)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.change_direction(DOWN)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.change_direction(LEFT)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.change_direction(RIGHT)
        elif key == pygame.K_p:
            self.paused = not self.paused
    def handle_game_over_key(self, key):
        """Restart with same difficulty or return to menu."""
        if key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self.start_game(self.difficulty_name)
        elif key == pygame.K_m:
            self.state = "menu"
    # ----- update -----
    def update(self, dt_ms):
        """Advance game logic; the board updates once per move interval."""
        if self.state != "playing" or self.paused:
            return
        self.move_timer += dt_ms
        if self.move_timer < self.move_interval:
            return
        self.move_timer = 0.0
        self.perform_move()
    def perform_move(self):
        """Execute one snake move and resolve eating / collisions."""
        self.snake.move()
        head = self.snake.get_head_position()
        # Wall collision
        hx, hy = head
        if hx < 0 or hx >= GRID_WIDTH or hy < 0 or hy >= GRID_HEIGHT:
            self.game_over()
            return
        # Self collision
        if self.snake.check_self_collision():
            self.game_over()
            return
        # Eating
        if self.food.position is not None and head == self.food.position:
            self.score += SCORE_PER_FOOD
            self.snake.grow(1)
            self.food = Food(self.snake.body)
            if self.food.position is None:
                # Snake fills the board: player wins.
                self.game_over()
    # ----- rendering -----
    def render(self):
        """Draw the current state to the screen."""
        self.screen.fill(COLOR_BACKGROUND)
        if self.state == "menu":
            self.render_menu()
        elif self.state == "playing":
            self.render_playing()
        elif self.state == "game_over":
            self.render_game_over()
        pygame.display.flip()
    ...