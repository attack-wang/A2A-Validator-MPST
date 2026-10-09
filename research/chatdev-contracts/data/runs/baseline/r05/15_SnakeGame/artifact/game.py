'''
game.py
Core Snake game logic, independent of any GUI toolkit: tick updates,
collision detection, scoring, and difficulty handling.
'''
import config
from snake import Snake
from food import Food
class Game:
    '''
    Holds the full state of one game session: the snake, the food,
    the score, and the game-over / win flags. Each call to tick()
    advances the simulation by exactly one grid step.
    '''
    def __init__(self, difficulty_name="Medium"):
        self.difficulty_name = difficulty_name
        self.set_difficulty(difficulty_name)
        self.reset()
    def set_difficulty(self, difficulty_name):
        '''Apply a difficulty preset (falls back to Medium if unknown).'''
        if difficulty_name not in config.DIFFICULTIES:
            difficulty_name = "Medium"
        self.difficulty_name = difficulty_name
        self.ticks_per_second = config.DIFFICULTIES[difficulty_name]["speed"]
        self.points_per_food = config.DIFFICULTIES[difficulty_name]["points"]
    def reset(self):
        '''Start a fresh session with the currently selected difficulty.'''
        start_x = config.GRID_WIDTH // 2
        start_y = config.GRID_HEIGHT // 2
        self.snake = Snake(start_x, start_y)
        self.food = Food()
        self.food.respawn(self.snake.get_body())
        self.score = 0
        self.food_eaten = 0
        self.game_over = False
        self.death_reason = ""
        self.won = False
    def handle_direction_input(self, direction):
        '''Forward a steering request from the GUI to the snake.'''
        if not self.game_over:
            self.snake.set_direction(direction)
    def tick(self):
        '''
        Advance the game by one step: move the snake, check collisions,
        handle eating, and update the score.
        '''
        if self.game_over:
            return
        next_head = self.snake.peek_next_head()
        # Boundary collision.
        hx, hy = next_head
        if not (0 <= hx < config.GRID_WIDTH and 0 <= hy < config.GRID_HEIGHT):
            self._end_game("You hit the boundary!")
            return
        # Will the snake grow this tick (i.e., is food at the next head)?
        grow = (next_head == self.food.get_position())
        # Self collision: the head may enter the tail cell only if the
        # tail is moving away this tick (i.e., not growing).
        body = self.snake.get_body()
        if not grow and next_head == body[-1]:
            pass  # tail vacates this cell, allowed
        elif next_head in body[:-1] or (grow and next_head == body[-1]):
            self._end_game("You collided with yourself!")
            return
        # Move the snake.
        self.snake.advance(grow=grow)
        # Eating.
        if grow:
            self.food_eaten += 1
            self.score += self.points_per_food
            self.food.respawn(self.snake.get_body())
            if self.food.get_position() is None:
                self.won = True
                self._end_game("You filled the whole board!")
    def get_score(self):
        '''Return the current score.'''
        return self.score
    def get_food_eaten(self):
        '''Return how many food items have been eaten.'''
        return self.food_eaten
    def is_game_over(self):
        '''Return True when the session has ended (win or loss).'''
        return self.game_over
    def get_death_reason(self):
        '''Return the human-readable reason the game ended.'''
        return self.death_reason
    def _end_game(self, reason):
        '''Flag the session as finished with the given reason.'''
        self.game_over = True
        self.death_reason = reason