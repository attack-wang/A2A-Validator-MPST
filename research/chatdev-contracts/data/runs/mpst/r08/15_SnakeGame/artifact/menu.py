'''
menu.py
Pre-game difficulty selection menu rendered with pygame. The player navigates
with the UP/DOWN (or W/S) keys and confirms with ENTER/SPACE. ESC quits.
'''
import pygame
import settings as cfg
class Menu:
    '''Interactive difficulty selection screen.'''
    def __init__(self, screen):
        self.screen = screen
        self.options = list(cfg.DIFFICULTY_SETTINGS.keys())
        self.selected_index = self.options.index(cfg.DEFAULT_DIFFICULTY)
        self.font_title = pygame.font.SysFont(None, 64, bold=True)
        self.font_option = pygame.font.SysFont(None, cfg.FONT_SIZE_MENU)
        self.font_hint = pygame.font.SysFont(None, cfg.FONT_SIZE_MESSAGE)
        self.clock = pygame.time.Clock()  # FIX: create once, not every frame
    def run(self):
        '''Display the menu loop. Returns the chosen difficulty name, or
        None if the user closes the window / presses ESC.'''
        while True:
            choice = self._handle_events()
            if choice == "quit":
                return None
            if choice == "confirm":
                return self.options[self.selected_index]
            self._render()
            pygame.display.flip()
            # Menu doesn't need high FPS; cap to keep CPU usage low.
            self.clock.tick(30)
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE,):
                    return "quit"
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    return "confirm"
        return None
    def _render(self):
        self.screen.fill(cfg.COLOR_BACKGROUND)
        title = self.font_title.render("CLASSIC SNAKE", True, cfg.COLOR_SNAKE_HEAD)
        title_rect = title.get_rect(center=(cfg.SCREEN_WIDTH // 2, 110))
        self.screen.blit(title, title_rect)
        subtitle = self.font_hint.render("Select difficulty", True, cfg.COLOR_TEXT_DIM)
        subtitle_rect = subtitle.get_rect(center=(cfg.SCREEN_WIDTH // 2, 170))
        self.screen.blit(subtitle, subtitle_rect)
        base_y = 250
        spacing = 60
        for i, option in enumerate(self.options):
            speed = cfg.DIFFICULTY_SETTINGS[option]
            label = f"{option}  ({speed} moves/sec)"
            color = cfg.COLOR_MENU_HIGHLIGHT if i == self.selected_index else cfg.COLOR_TEXT
            text = self.font_option.render(label, True, color)
            text_rect = text.get_rect(center=(cfg.SCREEN_WIDTH // 2, base_y + i * spacing))
            self.screen.blit(text, text_rect)
            if i == self.selected_index:
                arrow_l = self.font_option.render(">", True, cfg.COLOR_MENU_HIGHLIGHT)
                self.screen.blit(arrow_l, (text_rect.left - 30, text_rect.top))
                arrow_r = self.font_option.render("<", True, cfg.COLOR_MENU_HIGHLIGHT)
                self.screen.blit(arrow_r, (text_rect.right + 10, text_rect.top))
        hint = self.font_hint.render(
            "UP/DOWN to choose  |  ENTER to start  |  ESC to quit",
            True, cfg.COLOR_TEXT_DIM,
        )
        hint_rect = hint.get_rect(center=(cfg.SCREEN_WIDTH // 2, cfg.SCREEN_HEIGHT - 60))
        self.screen.blit(hint, hint_rect)