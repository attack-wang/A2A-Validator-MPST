import sys
import pygame
import settings
from snake import Snake
from food import Food
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Classic Snake")
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont("consolas", 40, bold=True)
        self.font_medium = pygame.font.SysFont("consolas", 24)
        self.font_small = pygame.font.SysFont("consolas", 18)
        self.difficulty_key = "2"
        self.state = "menu"  # menu | playing | game_over
        self.reset_round()
    def reset_round(self):
        self.snake = Snake(settings.GRID_WIDTH // 2, settings.GRID_HEIGHT // 2)
        self.food = Food(list(self.snake.body))
        self.score = 0
        self.paused = False
        self.move_counter = 0
    def run(self):
        while True:
            if self.state == "menu":
                self.run_menu()
            elif self.state == "playing":
                self.run_playing()
            elif self.state == "game_over":
                self.run_game_over()
    def run_menu(self):
        while self.state == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        self.difficulty_key = "1"
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        self.difficulty_key = "2"
                    elif event.key in (pygame.K_3, pygame.K_KP3):
                        self.difficulty_key = "3"
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                        self.state = "playing"
                        self.reset_round()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            self.render_menu()
            self.clock.tick(settings.MENU_FPS)
    def run_playing(self):
        while self.state == "playing":
            self.handle_events()
            if not self.paused:
                self.move_counter += 1
                fps = settings.DIFFICULTY_LEVELS[self.difficulty_key]["fps"]
                if self.move_counter >= settings.BASE_FPS // fps:
                    self.move_counter = 0
                    self.update()
            self.render()
            self.clock.tick(settings.BASE_FPS)