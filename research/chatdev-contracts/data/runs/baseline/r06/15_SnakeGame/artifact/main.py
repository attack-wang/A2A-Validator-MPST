'''
main.py
Entry point: wires up pygame, shows the menu and launches game rounds.
'''
import pygame
import settings
from menu import Menu
from game import Game
def main():
    """Application entry point."""
    pygame.init()
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    high_score = 0
    try:
        while True:
            menu = Menu(screen, clock, high_score)
            difficulty = menu.run()
            if difficulty is None:
                break
            game = Game(screen, clock, difficulty, high_score)
            exit_action = game.run()
            high_score = max(high_score, game.score)
            if exit_action == "quit":
                break
    finally:
        pygame.quit()
if __name__ == "__main__":
    main()