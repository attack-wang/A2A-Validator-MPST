'''
Core game logic: states, input, collisions, scoring and the main loop.
'''
import pygame
import settings
from bird import Bird
from pipemanager import PipeManager
from renderer import Renderer
import highscore
MENU, PLAYING, GAME_OVER = "menu", "playing", "game_over"
class Game:
    '''Main application: owns the game loop, state machine and entities.'''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        self.bird = Bird(settings.BIRD_X, settings.SCREEN_HEIGHT // 2)
        self.pipe_manager = PipeManager()
        self.high_score = highscore.load_high_score()
        self.state = MENU
        self.score = 0
        self.flash_timer = 0
        self.game_over_timer = 0
        self.new_high_score = False
    def reset(self):
        '''Restore all entities and counters for a fresh run.'''
        self.bird.reset()
        self.pipe_manager.reset()
        self.score = 0
        self.new_high_score = False
    def start(self):
        '''Begin a new run from the menu or game-over screen.'''
        self.reset()
        self.state = PLAYING
        self.bird.flap()
    def handle_input(self):
        '''Process events; return False when the game should exit.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key in (pygame.K_SPACE, pygame.K_UP):
                    self._primary_action()
                elif event.key == pygame.K_r and self.state == GAME_OVER:
                    self.start()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._primary_action()
        return True
    def _primary_action(self):
        '''Dispatch SPACE/click to the current state's primary action.'''
        if self.state == MENU:
            self.start()
        elif self.state == PLAYING:
            self.bird.flap()
        elif self.state == GAME_OVER and self.game_over_timer <= 0:
            self.start()
    def update(self):
        '''Advance the simulation one frame according to the state.'''
        if self.state == PLAYING:
            self.bird.update()
            self.pipe_manager.update(self.score)
            self.check_scoring()
            self.check_collisions()
        elif self.state == GAME_OVER:
            ground_y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
            if self.bird.y < ground_y - settings.BIRD_RADIUS:
                self.bird.update()
                if self.bird.y >= ground_y - settings.BIRD_RADIUS:
                    self.bird.y = ground_y - settings.BIRD_RADIUS
                    self.bird.velocity = 0
            if self.game_over_timer > 0:
                self.game_over_timer -= 1
        if self.flash_timer > 0:
            self.flash_timer -= 1
        if self.state == PLAYING:
            scroll = self.pipe_manager.current_speed(self.score)
        elif self.state == MENU:
            scroll = 1.0
        else:
            scroll = 0.0
        self.renderer.update_background(scroll)
    def check_scoring(self):
        '''Award one point for each pipe the bird has fully passed.'''
        for pipe in self.pipe_manager.pipes:
            if not pipe.scored and pipe.x + settings.PIPE_WIDTH < self.bird.x:
                pipe.scored = True
                self.score += 1
    def check_collisions(self):
        '''Handle ground/ceiling bounds and pipe hits; may trigger game over.'''
        ground_y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        if self.bird.rect.bottom >= ground_y:
            self.bird.y = ground_y - settings.BIRD_RADIUS
            self.game_over()
            return
        if self.bird.rect.top <= 0:
            self.bird.y = settings.BIRD_RADIUS
            self.bird.velocity = 0
        bird_rect = self.bird.rect
        for pipe in self.pipe_manager.pipes:
            if pipe.collides(bird_rect):
                self.game_over()
                return
    def game_over(self):
        '''Switch to the game-over state and persist a new high score.'''
        self.state = GAME_OVER
        self.game_over_timer = 20
        self.flash_timer = 8
        self.bird.alive = False
        self.new_high_score = self.score > self.high_score
        if self.new_high_score:
            self.high_score = self.score
            highscore.save_high_score(self.high_score)
    def run(self):
        '''Main loop: input, update, render at the configured FPS.'''
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.renderer.draw(self)
            pygame.display.flip()
            self.clock.tick(settings.FPS)
        pygame.quit()