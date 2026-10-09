import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    game = Game(screen)
    game.run(clock)
    pygame.quit()

if __name__ == "__main__":
    main()