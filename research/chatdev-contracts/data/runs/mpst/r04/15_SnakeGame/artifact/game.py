'''
Game controller: main loop, rendering, scoring and game-over handling.
'''
import sys
import pygame
import settings
from snake import Snake
from food import Food
class Game:
    '''Runs a full Snake session for a chosen difficulty.'''
    def __init__(self, difficulty_name):
        self.difficulty_name = difficulty_name
        self.speed = settings.DIFFICULTY_LEVELS[difficulty_name]
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT + settings.HUD_HEIGHT)
        )
        pygame.display.set_caption(
            f"Snake - {difficulty_name}"
        )
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 22)
        self.big_font = pygame.font.SysFont("consolas", 36, bold=True)
        self.reset()
    def reset(self):
        '''Initialise a fresh round.'''
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False
        self.move_timer = 0.0
        self.move_interval = 1.0 / self.speed
    def run(self):
        '''Main loop: process input, update state, render, repeat.'''
        while True:
            delta_time = self.clock.tick(60) / 1000.0
            self.handle_events()
            if not self.game_over:
                self.update(delta_time)
            self.render()
            pygame.display.flip()
    def handle_events(self):
        '''Process keyboard and window events.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
    def handle_keydown(self, key):
        '''Map key presses to snake directions or restart actions.'''
        if self.game_over:
            if key == pygame.K_RETURN:
                self.reset()
            elif key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
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
            self.snake.turn(direction_map[key])
    def update(self, delta_time):
        '''Advance game state: move the snake on a fixed interval.'''
        self.move_timer += delta_time
        while self.move_timer >= self.move_interval:
            self.move_timer -= self.move_interval
            self.step()
    def step(self):
        '''Perform one discrete game tick.'''
        self.snake.move()
        if self.snake.hits_boundary() or self.snake.hits_self():
            self.game_over = True
            return
        if self.snake.head == self.food.position:
            self.score += 1
            self.snake.grow()
            self.food.randomize_position(self.snake.body)
            if self.food.eaten:
                # Board is full - victory condition
                self.game_over = True
    def render(self):
        '''Draw HUD, board, snake and food.'''
        self.screen.fill(settings.COLORS["background"])
        self.render_hud()
        self.render_board()
        self.render_food()
        self.render_snake()
        if self.game_over:
            self.render_game_over()
    def render_hud(self):
        '''Draw the score bar above the play field.'''
        hud_rect = pygame.Rect(0, 0, settings.WINDOW_WIDTH, settings.HUD_HEIGHT)
        pygame.draw.rect(self.screen, settings.COLORS["hud_background"], hud_rect)
        score_text = self.font.render(
            f"Score: {self.score}", True, settings.COLORS["text"]
        )
        diff_text = self.font.render(
            f"Difficulty: {self.difficulty_name}", True, settings.COLORS["text"]
        )
        self.screen.blit(score_text, (10, 8))
        self.screen.blit(diff_text, (settings.WINDOW_WIDTH - diff_text.get_width() - 10, 8))
    def render_board(self):
        '''Draw the play field and subtle grid lines.'''
        board_rect = pygame.Rect(
            0, settings.HUD_HEIGHT, settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT
        )
        pygame.draw.rect(self.screen, settings.COLORS["background"], board_rect)
        for x in range(0, settings.WINDOW_WIDTH, settings.CELL_SIZE):
            pygame.draw.line(
                self.screen, settings.COLORS["grid"],
                (x, settings.HUD_HEIGHT), (x, settings.HUD_HEIGHT + settings.WINDOW_HEIGHT)
            )
        for y in range(0, settings.WINDOW_HEIGHT, settings.CELL_SIZE):
            pygame.draw.line(
                self.screen, settings.COLORS["grid"],
                (0, settings.HUD_HEIGHT + y), (settings.WINDOW_WIDTH, settings.HUD_HEIGHT + y)
            )
    def cell_rect(self, position):
        '''Convert a grid position to a pixel rectangle.'''
        x, y = position
        return pygame.Rect(
            x * settings.CELL_SIZE,
            settings.HUD_HEIGHT + y * settings.CELL_SIZE,
            settings.CELL_SIZE,
            settings.CELL_SIZE,
        )
    def render_food(self):
        '''Draw the food item.'''
        if self.food.position is not None:
            rect = self.cell_rect(self.food.position)
            pygame.draw.rect(self.screen, settings.COLORS["food"], rect, border_radius=6)
    def render_snake(self):
        '''Draw every snake segment, highlighting the head.'''
        for i, segment in enumerate(self.snake.body):
            rect = self.cell_rect(segment)
            color = (
                settings.COLORS["snake_head"]
                if i == len(self.snake.body) - 1
                else settings.COLORS["snake_body"]
            )
            pygame.draw.rect(self.screen, color, rect.inflate(-2, -2), border_radius=4)
    def render_game_over(self):
        '''Overlay the game-over message and restart hint.'''
        overlay = pygame.Surface(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, settings.HUD_HEIGHT))
        title = self.big_font.render("GAME OVER", True, settings.COLORS["highlight"])
        score_line = self.font.render(
            f"Final score: {self.score}", True, settings.COLORS["text"]
        )
        hint = self.font.render(
            "Press ENTER to play again - ESC to quit",
            True, settings.COLORS["text"]
        )
        center_x = settings.WINDOW_WIDTH // 2
        center_y = settings.HUD_HEIGHT + settings.WINDOW_HEIGHT // 2
        self.screen.blit(title, (center_x - title.get_width() // 2, center_y - 60))
        self.screen.blit(score_line, (center_x - score_line.get_width() // 2, center_y))
        self.screen.blit(hint, (center_x - hint.get_width() // 2, center_y + 40))