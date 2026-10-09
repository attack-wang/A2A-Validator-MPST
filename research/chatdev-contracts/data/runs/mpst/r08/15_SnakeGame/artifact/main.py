'''
main.py
Entry point for the Classic Snake game. Initializes pygame, shows the
difficulty menu, then runs game sessions until the user quits.
'''
import pygame
import settings as cfg
from menu import Menu
from game import Game
def main():
    '''Application entry point: menu -> game -> menu loop.'''
    pygame.init()
    screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
    pygame.display.set_caption("Classic Snake")
    running = True
    best_score = 0  # carried across sessions within this run
    while running:
        menu = Menu(screen)
        difficulty = menu.run()
        if difficulty is None:
            running = False
            break
        game = Game(screen, difficulty, high_score=best_score)
        action = game.run()
        best_score = max(best_score, game.best_score)
        if action == "quit":
            running = False
    pygame.quit()
if __name__ == "__main__":
    main()