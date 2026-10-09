import sys
import pygame
from game import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 640))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    game = Game(screen)
    while True:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)
        game.update(dt)
        game.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()