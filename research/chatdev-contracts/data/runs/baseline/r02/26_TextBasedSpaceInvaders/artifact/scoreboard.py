'''scoreboard.py — on-screen display of score, high score and remaining lives.'''
import pygame
class Scoreboard:
    '''Render the HUD: current score, high score and ship icons for lives.'''
    def __init__(self, game):
        '''Prepare the initial score images.'''
        self.screen = game.screen
        self.settings = game.settings
        self.stats = game.stats
        self.ship_image = pygame.transform.scale(
            game.ship.image, (game.ship.rect.width // 2, game.ship.rect.height // 2)
        )
        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 30)
        self.prep_score()
        self.prep_high_score()
        self.prep_lives()
    def prep_score(self):
        '''Turn the current score into a rendered image at the top left.'''
        rounded_score = round(self.stats.score, -1)
        score_str = f"Score: {rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.topleft = (15, 10)
    def prep_high_score(self):
        '''Turn the high score into a rendered image centered at the top.'''
        rounded_high = round(self.stats.high_score, -1)
        high_str = f"High Score: {rounded_high:,}"
        self.high_score_image = self.font.render(high_str, True, self.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = (self.settings.screen_width // 2, 10)
    def prep_lives(self):
        '''Build the row of small ship icons representing remaining lives.'''
        count = max(0, self.stats.ships_left)
        height = self.ship_image.get_height()
        if count == 0:
            self.lives_image = pygame.Surface((1, height), pygame.SRCALPHA)
        else:
            width = self.ship_image.get_width() * count + 10 * (count - 1)
            lives_surf = pygame.Surface((width, height), pygame.SRCALPHA)
            x = 0
            for _ in range(count):
                lives_surf.blit(self.ship_image, (x, 0))
                x += self.ship_image.get_width() + 10
            self.lives_image = lives_surf
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.topright = (self.settings.screen_width - 15, 10)
    def check_high_score(self):
        '''Update the high score if the current score beats it.'''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
    def draw(self):
        '''Draw score, high score and lives onto the screen.'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.lives_image, self.lives_rect)