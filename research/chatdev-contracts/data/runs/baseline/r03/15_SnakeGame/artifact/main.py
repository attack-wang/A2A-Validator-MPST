'''
main.py
Entry point for the Snake game. Initializes pygame and
orchestrates the flow: menu -> game -> game over screen.
'''
import sys
import pygame
import settings
import ui
from game import Game
def main():
    """Initialize pygame and run the main application loop."""
    pygame.init()
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Snake - ChatDev Edition")
    clock = pygame.time.Clock()
    while True:
        # 1. Main menu: choose difficulty
        difficulty = ui.show_menu(screen, clock)
        if difficulty is None:
            break
        # 2. Run a game session
        game = Game(difficulty)
        result = game.run(screen)
        if result == "menu":
            continue  # Player pressed ESC, back to menu
        # 3. Game over / victory screen
        while True:
            action = ui.show_game_over(screen, clock, game.score, game.victory)
            if action == "restart":
                game = Game(difficulty)
                result = game.run(screen)
                if result == "menu":
                    break
            elif action == "menu":
                break
            else:  # quit
                pygame.quit()
                sys.exit()
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()