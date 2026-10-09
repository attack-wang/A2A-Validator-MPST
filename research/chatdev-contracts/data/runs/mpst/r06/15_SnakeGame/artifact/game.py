'''
game.py
Defines the Game class: encapsulates a single round of Snake, including
input handling, timed snake movement, collision detection, food
consumption, scoring, and rendering of the play-field.
'''
import pygame
from settings import (
    GRID_WIDTH, GRID_HEIGHT, SCORE_PER_FOOD, DIFFICULTIES,
)
from snake import Snake
from food import Food
import ui
class Game:
    """Manages the state and logic of one Snake round."""
    def __init__(self, difficulty_name):
        """Prepare a round for the given difficulty (moves per second).
        The persistent high score is managed by the main loop."""
        self.difficulty_name = difficulty_name
        self.move_interval_ms = 1000.0 / DIFFICULTIES[difficulty_name]
        self.reset()
    def reset(self):
        """(Re)initialize snake, food, score and timers for a new round."""
        self.snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.food = Food(GRID_WIDTH, GRID_HEIGHT)
        self.food.spawn(self.snake.get_body())
        self.score = 0
        self.game_over = False
        self.won = False
        self.time_since_move = 0.0
    def handle_event(self, event):
        """Translate a KEYDOWN event into a direction change."""
        if event.type != pygame.KEYDOWN:
            return
        direction_map = {
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_w: (0, -1),
            pygame.K_s: (0, 1),
            pygame.K_a: (-1, 0),
            pygame.K_d: (1, 0),
        }
        if event.key in direction_map:
            self.snake.update_direction(direction_map[event.key])
    def update(self, delta_ms):
        """Advance the simulation using accumulated time; may step the
        snake multiple times if a frame was slow."""
        if self.game_over:
            return
        self.time_since_move += delta_ms
        while self.time_since_move >= self.move_interval_ms:
            self.time_since_move -= self.move_interval_ms
            self._step()
    def _step(self):
        """Perform one discrete game tick: move, check collisions,
        handle food consumption and scoring."""
        new_head = self.snake.move()
        # Boundary collision
        x, y = new_head
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            self.game_over = True
            return
        # Self collision
        if self.snake.check_self_collision():
            self.game_over = True
            return
        # Food consumption
        if self.food.get_position() is not None and new_head == self.food.get_position():
            self.snake.grow()
            self.score += SCORE_PER_FOOD
            if not self.food.spawn(self.snake.get_body()):
                # No free cell left: the player has filled the board
                self.won = True
                self.game_over = True
    def is_game_over(self):
        """Return True when the round has ended."""
        return self.game_over
    def render(self, screen, font, high_score):
        """Draw the full play-field: board, food, snake, and the score bar
        using the persistent high score managed by the main loop."""
        ui.draw_board(screen)
        ui.draw_food(screen, self.food)
        ui.draw_snake(screen, self.snake)
        ui.draw_score_bar(screen, font, self.score,
                          self.difficulty_name, high_score)