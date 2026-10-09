'''
Difficulty selection menu shown before the game starts.
'''
import sys
import pygame
import settings
class Menu:
    '''Interactive menu for choosing a difficulty level.'''
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT + settings.HUD_HEIGHT)
        )
        pygame.display.set_caption("Snake - Select Difficulty")
        self.font = pygame.font.SysFont("consolas", 30, bold=True)
        self.title_font = pygame.font.SysFont("consolas", 44, bold=True)
        self.hint_font = pygame.font.SysFont("consolas", 20)
        self.options = list(settings.DIFFICULTY_LEVELS.keys())
        self.selected_index = 1  # default: Medium
    def show(self):
        '''Display the menu and return the chosen difficulty name.'''
        while True:
            self.handle_events()
            self.render()
            pygame.display.flip()
            # Cap menu frame rate
            pygame.time.Clock().tick(30)
    def handle_events(self):
        '''Navigate with arrows/W-S, confirm with Enter/Space, quit with ESC.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return self.options[self.selected_index]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    def render(self):
        '''Draw the title and difficulty options.'''
        self.screen.fill(settings.COLORS["menu_background"])
        title = self.title_font.render("SNAKE", True, settings.COLORS["snake_head"])
        self.screen.blit(
            title,
            (settings.WINDOW_WIDTH // 2 - title.get_width() // 2, 60)
        )
        subtitle = self.hint_font.render(
            "Select difficulty (Up/Down, Enter to start)",
            True, settings.COLORS["text"]
        )
        self.screen.blit(
            subtitle,
            (settings.WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 120)
        )
        ...