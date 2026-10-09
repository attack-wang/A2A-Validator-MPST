"""Entry point for the Tower of the Sorcerer-inspired roguelike."""
import pygame
from game import Game
def main():
    game = Game()
    game.run()
    pygame.quit()
if __name__ == "__main__":
    main()