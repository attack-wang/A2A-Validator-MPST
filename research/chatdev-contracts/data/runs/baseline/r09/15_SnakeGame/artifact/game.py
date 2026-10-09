'''
game.py
Core of the Classic Snake game: window management, the state machine
(menu / playing / paused / game over), input handling, collision checks,
scoring and all rendering.
'''
import sys
import pygame
import settings
from snake import Snake
from food import Food
class Game:
    '''Main application class that owns the game loop.'''
    def __init__(self):
        '''Initialise pygame, the window, fonts and the initial state.'''
        pygame.init()
        self.window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption("Classic Snake - ChatDev")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont("consolas,monospace", 18)
        self.font_medium = pygame.font.SysFont("consolas,monospace", 24, bold=True)
        self.font_large = pygame.font.SysFont("consolas,monospace", 40, bold=True)
        self.difficulty = "medium"
        self.state = "menu"          # menu | playing | paused | game_over
        self.score = 0
        self.food_eaten = 0
        self.snake = Snake()
        self.food = Food(self.snake.positions)
    # ------------------------------------------------------------------
    # State transitions
    # ------------------------------------------------------------------
    def start_game(self, difficulty):
        '''(Re)start a run with the chosen difficulty level.'''
        self.difficulty = difficulty
        self.snake.reset()
        self.food.randomize_position(self.snake.positions)
        self.score = 0
        self.food_eaten = 0
        self.state = "playing"
    def toggle_pause(self):
        '''Switch between playing and paused states.'''
        if self.state == "playing":
            self.state = "paused"
        elif self.state == "paused":
            self.state = "playing"
    def game_over(self):
        '''End the current run.'''
        self.state = "game_over"
    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------
    def handle_events(self):
        '''Process the event queue for the current state.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return
            if event.type != pygame.KEYDOWN:
                continue
            if self.state == "menu":
                self.handle_menu_input(event.key)
            elif self.state in ("playing", "paused"):
                self.handle_play_input(event.key)
            elif self.state == "game_over":
                self.handle_game_over_input(event.key)
    def handle_menu_input(self, key):
        '''Difficulty selection: 1/2/3 starts a run, ESC quits.'''
        if key in (pygame.K_1, pygame.K_KP1):
            self.start_game("easy")
        elif key in (pygame.K_2, pygame.K_KP2):
            self.start_game("medium")
        elif key in (pygame.K_3, pygame.K_KP3):
            self.start_game("hard")
        elif key == pygame.K_ESCAPE:
            self.quit()
    def handle_play_input(self, key):
        '''Directional keys steer the snake, P pauses, ESC quits.'''
        if self.state == "paused":
            if key == pygame.K_p:
                self.toggle_pause()
            elif key == pygame.K_ESCAPE:
                self.quit()
            return
        direction_map = {
            pygame.K_UP: settings.UP,
            pygame.K_w: settings.UP,
            pygame.K_DOWN: settings.DOWN,
            pygame.K_s: settings.DOWN,
            pygame.K_LEFT: settings.LEFT,
            pygame.K_a: settings.LEFT,
            pygame.K_RIGHT: settings.RIGHT,
            pygame.K_d: settings.RIGHT,
        }
        if key in direction_map:
            self.snake.queue_direction(direction_map[key])
        elif key == pygame.K_p:
            self.toggle_pause()
        elif key == pygame.K_ESCAPE:
            self.quit()
    def handle_game_over_input(self, key):
        '''R restarts, M returns to the menu, Q/ESC quits.'''
        if key == pygame.K_r:
            self.start_game(self.difficulty)
        elif key == pygame.K_m:
            self.state = "menu"
        elif key in (pygame.K_q, pygame.K_ESCAPE):
            self.quit()
    def quit(self):
        '''Shut pygame down and exit the process.'''
        pygame.quit()
        sys.exit()
    # ------------------------------------------------------------------
    # Simulation
    # ------------------------------------------------------------------
    def update(self):
        '''Advance the simulation by one tick (only while playing).'''
        if self.state != "playing":
            return
        self.snake.update()
        head_x, head_y = self.snake.get_head_position()
        hit_wall = not (0 <= head_x < settings.GRID_WIDTH and 0 <= head_y < settings.GRID_HEIGHT)
        if hit_wall or self.snake.check_self_collision():
            self.game_over()
            return
        if self.food.position is not None and self.snake.get_head_position() == self.food.position:
            self.snake.grow()
            self.food_eaten += 1
            self.score += settings.DIFFICULTY_LEVELS[self.difficulty]["multiplier"]
            self.food.randomize_position(self.snake.positions)
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def render(self):
        '''Draw the current state to the window.'''
        self.window.fill(settings.COLOR_BACKGROUND)
        if self.state == "menu":
            self.render_menu()
        elif self.state == "playing":
            self.render_board()
            self.food.draw(self.window)
            self.snake.draw(self.window)
            self.render_hud()
        elif self.state == "paused":
            self.render_board()
            self.food.draw(self.window)
            self.snake.draw(self.window)
            self.render_hud()
            self.render_center_text("PAUSED", self.font_large, settings.COLOR_HIGHLIGHT, -40)
            self.render_center_text("Press P to resume", self.font_small, settings.COLOR_TEXT_DIM, 10)
        elif self.state == "game_over":
            self.render_board()
            self.food.draw(self.window)
            self.snake.draw(self.window)
            self.render_hud()
            self.render_game_over()
        pygame.display.update()
    def render_board(self):
        '''Draw the play-field grid and its border.'''
        for x in range(0, settings.WINDOW_WIDTH, settings.GRID_SIZE):
            pygame.draw.line(self.window, settings.COLOR_GRID_LINE, (x, 0), (x, settings.WINDOW_HEIGHT))
        for y in range(0, settings.WINDOW_HEIGHT, settings.GRID_SIZE):
            pygame.draw.line(self.window, settings.COLOR_GRID_LINE, (0, y), (settings.WINDOW_WIDTH, y))
        pygame.draw.rect(
            self.window,
            settings.COLOR_BORDER,
            (0, 0, settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT),
            2,
        )
    def render_hud(self):
        '''Show score, food eaten, difficulty and snake length.'''
        difficulty_label = settings.DIFFICULTY_LEVELS[self.difficulty]["label"]
        score_text = self.font_small.render(f"Score: {self.score}", True, settings.COLOR_TEXT)
        food_text = self.font_small.render(f"Food: {self.food_eaten}", True, settings.COLOR_TEXT)
        length_text = self.font_small.render(f"Length: {self.snake.get_length()}", True, settings.COLOR_TEXT)
        diff_text = self.font_small.render(f"Difficulty: {difficulty_label}", True, settings.COLOR_TEXT)
        self.window.blit(score_text, (10, 8))
        self.window.blit(food_text, (10, 30))
        diff_rect = diff_text.get_rect(topright=(settings.WINDOW_WIDTH - 10, 8))
        self.window.blit(diff_text, diff_rect)
        length_rect = length_text.get_rect(topright=(settings.WINDOW_WIDTH - 10, 30))
        self.window.blit(length_rect, length_rect.topleft)