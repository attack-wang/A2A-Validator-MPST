'''
menu.py
Start menu with difficulty selection, controls help and high score display.
'''
import pygame
import settings
import ui
class Menu:
    """Interactive start menu for choosing a difficulty level."""
    def __init__(self, screen, clock, high_score=0):
        self.screen = screen
        self.clock = clock
        self.high_score = high_score
        self.options = list(settings.DIFFICULTIES.keys())
        self.selected_index = self.options.index(settings.DEFAULT_DIFFICULTY)
        self.running = True
        self.choice = None
    def run(self):
        """Show the menu and return the chosen difficulty (or None)."""
        while self.running:
            self.clock.tick(settings.FPS)
            self.handle_events()
            self.draw()
        return self.choice
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.choice = self.options[self.selected_index]
                    self.running = False
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    def draw(self):
        self.screen.fill(settings.COLOR_BACKGROUND)
        ui.draw_text(self.screen, "S N A K E", 48, settings.COLOR_SNAKE_HEAD, center=(settings.WINDOW_WIDTH // 2, 80), bold=True)
        ui.draw_text(self.screen, "Select difficulty (Up/Down + Enter)", 18, settings.COLOR_TEXT_DIM, center=(settings.WINDOW_WIDTH // 2, 140))
        base_y = 200
        for i, name in enumerate(self.options):
            color = settings.COLOR_MENU_HIGHLIGHT if i == self.selected_index else settings.COLOR_TEXT
            prefix = "> " if i == self.selected_index else "  "
            config = settings.DIFFICULTIES[name]
            label = f"{prefix}{name}  (speed {config['speed']}, x{config['score_multiplier']} points)"
            ui.draw_text(self.screen, label, 24, color, center=(settings.WINDOW_WIDTH // 2, base_y + i * 40), bold=(i == self.selected_index))
        ui.draw_text(self.screen, f"High score: {self.high_score}", 18, settings.COLOR_TEXT_DIM, center=(settings.WINDOW_WIDTH // 2, base_y + len(self.options) * 40 + 20))
        ui.draw_text(self.screen, "Controls: Arrow keys / WASD to move · P to pause · ESC to quit", 15, settings.COLOR_TEXT_DIM, center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 40))
        pygame.display.flip()