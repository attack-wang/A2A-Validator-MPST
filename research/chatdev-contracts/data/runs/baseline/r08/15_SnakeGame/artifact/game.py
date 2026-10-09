'''
game.py
Core game orchestration: state machine (menu / playing / paused / game over),
fixed-timestep game loop, input handling, scoring and rendering.
'''
import sys
import pygame
import config
import ui
from snake import Snake
from food import Food
# --- Game states ------------------------------------------------------------
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
# --- Input mapping ----------------------------------------------------------
DIRECTION_KEYS = {
    pygame.K_UP: config.UP,
    pygame.K_DOWN: config.DOWN,
    pygame.K_LEFT: config.LEFT,
    pygame.K_RIGHT: config.RIGHT,
    pygame.K_w: config.UP,
    pygame.K_s: config.DOWN,
    pygame.K_a: config.LEFT,
    pygame.K_d: config.RIGHT,
}
class Game:
    """Main application class: owns the window, the game loop and all state."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption(config.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.difficulty_order = sorted(config.DIFFICULTIES.keys())
        self.selected_difficulty_index = self.difficulty_order.index(config.DEFAULT_DIFFICULTY)
        self.difficulty_key = config.DEFAULT_DIFFICULTY
        self.high_score = 0
        self.state = STATE_MENU
        self.reset_game()
    # -- setup ---------------------------------------------------------------
    @property
    def difficulty(self):
        return config.DIFFICULTIES[self.difficulty_key]
    def reset_game(self):
        """Create a fresh snake, food and zeroed score for a new round."""
        start_x = config.GRID_WIDTH // 2
        start_y = config.GRID_HEIGHT // 2
        self.snake = Snake(start_x, start_y, initial_length=3)
        self.food = Food(config.GRID_WIDTH, config.GRID_HEIGHT, self.snake)
        self.score = 0
        self.food_count = 0
        self.won = False
        self.new_record = False
        self.accumulator = 0.0
    def start_game(self):
        self.reset_game()
        self.state = STATE_PLAYING
    def end_game(self, win=False):
        self.new_record = self.score > self.high_score
        self.high_score = max(self.high_score, self.score)
        self.won = win
        self.state = STATE_GAME_OVER
    # -- update --------------------------------------------------------------
    def update(self):
        """Advance the simulation by one logic tick."""
        self.snake.next_direction()
        new_head = self.snake.next_head()
        will_grow = (new_head == self.food.position)
        if self.snake.check_boundary(new_head) or \
           self.snake.check_self_collision(new_head, ignore_tail=not will_grow):
            self.end_game()
            return
        self.snake.step(grow=will_grow)
        if will_grow:
            self.score += self.difficulty["points_per_food"]
            self.food_count += 1
            self.food.respawn(self.snake)
            if not self.food.exists:
                self.end_game(win=True)
    # -- events --------------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type != pygame.KEYDOWN:
                continue
            key = event.key
            if self.state == STATE_MENU:
                if key == pygame.K_ESCAPE:
                    return False
                elif key in (pygame.K_UP, pygame.K_w):
                    self.selected_difficulty_index = (self.selected_difficulty_index - 1) % len(self.difficulty_order)
                elif key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_difficulty_index = (self.selected_difficulty_index + 1) % len(self.difficulty_order)
                elif key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.difficulty_key = self.difficulty_order[self.selected_difficulty_index]
                    self.start_game()
                elif pygame.K_1 <= key <= pygame.K_4:
                    idx = key - pygame.K_1
                    if idx < len(self.difficulty_order):
                        self.selected_difficulty_index = idx
                        self.difficulty_key = self.difficulty_order[idx]
                        self.start_game()
            elif self.state == STATE_PLAYING:
                if key in DIRECTION_KEYS:
                    self.snake.queue_direction(DIRECTION_KEYS[key])
                elif key in (pygame.K_p, pygame.K_SPACE):
                    self.state = STATE_PAUSED
                elif key == pygame.K_r:
                    self.start_game()
                elif key == pygame.K_m:
                    self.state = STATE_MENU
                elif key in (pygame.K_ESCAPE, pygame.K_q):
                    return False
            elif self.state == STATE_PAUSED:
                if key in (pygame.K_p, pygame.K_SPACE, pygame.K_RETURN):
                    self.state = STATE_PLAYING
                elif key == pygame.K_r:
                    self.start_game()
                elif key == pygame.K_m:
                    self.state = STATE_MENU
                elif key in (pygame.K_ESCAPE, pygame.K_q):
                    return False
            elif self.state == STATE_GAME_OVER:
                if key == pygame.K_r:
                    self.start_game()
                elif key == pygame.K_m:
                    self.state = STATE_MENU
                elif key in (pygame.K_ESCAPE, pygame.K_q):
                    return False
        return True
    # -- render --------------------------------------------------------------
    def render(self):
        if self.state == STATE_MENU:
            names = [f"{config.DIFFICULTIES[k]['name']}  (speed {config.DIFFICULTIES[k]['speed']})"
                     for k in self.difficulty_order]
            ui.draw_menu(self.screen, names, self.selected_difficulty_index, self.high_score)
            return
        ui.draw_board(self.screen)
        ui.draw_food(self.screen, self.food)
        ui.draw_snake(self.screen, self.snake)
        ui.draw_hud(self.screen, self.score, self.high_score, self.difficulty["name"], self.food_count)
        if self.state == STATE_PAUSED:
            ui.draw_pause(self.screen)
        elif self.state == STATE_GAME_OVER:
            ui.draw_game_over(self.screen, self.score, self.high_score, self.won,
                              self.food_count, self.new_record)
    # -- main loop -------------------------------------------------------------
    def run(self):
        """Fixed-timestep loop: logic ticks at difficulty speed, render at FPS."""
        running = True
        while running:
            dt = self.clock.tick(config.FPS) / 1000.0
            running = self.handle_events()
            if self.state == STATE_PLAYING:
                self.accumulator += dt
                tick_interval = 1.0 / self.difficulty["speed"]
                while self.accumulator >= tick_interval:
                    self.accumulator -= tick_interval
                    self.update()
                    if self.state != STATE_PLAYING:
                        self.accumulator = 0.0
                        break
            self.render()
            pygame.display.flip()
        pygame.quit()