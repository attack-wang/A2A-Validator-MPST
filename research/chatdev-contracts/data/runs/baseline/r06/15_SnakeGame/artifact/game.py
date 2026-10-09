'''
game.py
Core game logic: main loop, input handling, state updates,
collision checks, scoring and rendering for a single Snake round.
'''
import pygame
import settings
from snake import Snake
from food import Food
import ui
EXIT_TO_MENU = "menu"
EXIT_QUIT = "quit"
class Game:
    """Runs one full round of Snake at a given difficulty."""
    def __init__(self, screen, clock, difficulty_name, high_score=0):
        """Initialise entities and timing. Reuses the shared screen/clock from main.py."""
        self.screen = screen
        self.clock = clock
        self.difficulty_name = difficulty_name
        config = settings.DIFFICULTIES[difficulty_name]
        self.speed = config["speed"]                # moves per second
        self.score_multiplier = config["score_multiplier"]
        pygame.display.set_caption(f"Snake — {difficulty_name}")
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.high_score = max(high_score, 0)
        self.game_over = False
        self.paused = False
        self.running = True
        self.move_timer = 0.0          # fixed-step accumulator, initialised
        self.exit_action = EXIT_TO_MENU
    def run(self):
        """Main loop. Returns 'menu' or 'quit' to satisfy main.py's contract."""
        while self.running:
            delta_time = self.clock.tick(settings.FPS) / 1000.0
            self.handle_events()
            if not self.paused and not self.game_over:
                self.update(delta_time)
            self.draw()
        return self.exit_action
    def handle_events(self):
        """Process keyboard and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.exit_action = EXIT_QUIT      # X button truly quits
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
    def handle_keydown(self, key):
        """Map key presses to direction changes or game controls."""
        if self.game_over:
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.reset_round()
            elif key == pygame.K_ESCAPE:
                self.running = False
                self.exit_action = EXIT_TO_MENU
            return
        if key in (pygame.K_UP, pygame.K_w):
            self.snake.turn(settings.UP)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.turn(settings.DOWN)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.turn(settings.LEFT)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.turn(settings.RIGHT)
        elif key == pygame.K_p:
            self.paused = not self.paused
        elif key == pygame.K_ESCAPE:
            self.running = False
            self.exit_action = EXIT_TO_MENU
    def reset_round(self):
        """Restart the round at the same difficulty."""
        self.snake.reset()
        self.food.randomize_position(self.snake.body)
        self.score = 0
        self.move_timer = 0.0
        self.game_over = False
        self.paused = False
    def update(self, delta_time):
        """Advance game state using a fixed-step accumulator."""
        self.move_timer += delta_time
        step = 1.0 / self.speed
        while self.move_timer >= step:
            self.move_timer -= step
            self.step()
    def step(self):
        """Perform one atomic snake move and all resulting checks."""
        self.snake.update()
        if self.snake.check_boundary_collision() or self.snake.check_self_collision():
            self.game_over = True
            self.high_score = max(self.high_score, self.score)
            return
        if self.food.position is not None and \
                self.snake.get_head_position() == self.food.position:
            self.score += self.score_multiplier
            self.snake.grow()
            self.food.randomize_position(self.snake.body)
            if self.food.position is None:      # board full → win condition
                self.game_over = True
                self.high_score = max(self.high_score, self.score)
    def draw(self):
        """Render board, entities, HUD and overlays."""
        self.screen.fill(settings.COLOR_BACKGROUND)
        ui.draw_grid(self.screen)
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        ui.draw_border(self.screen)
        ui.draw_score(self.screen, self.score, self.high_score, self.difficulty_name)
        if self.paused:
            ui.draw_center_message(self.screen, ["PAUSED", "Press P to resume"])
        elif self.game_over:
            ui.draw_center_message(self.screen, [
                "GAME OVER",
                f"Score: {self.score}   Best: {self.high_score}",
                "Enter: play again   ESC: main menu",
            ])
        pygame.display.flip()