'''
main.py
Entry point: initializes pygame and runs the Gold Miner game loop.
If the 'pygame' package is missing from the environment, the program
exits with a clear, actionable installation hint instead of a raw
ModuleNotFoundError traceback.
'''
import sys
try:
    import pygame
except ImportError:
    sys.stderr.write(
        "\n[Gold Miner] The required package 'pygame' is not installed.\n"
        "             Fix it with:  pip install pygame\n"
        "             Then start the game again:  python main.py\n"
    )
    sys.exit(1)
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from sound import init_sounds
from game import Game
def main():
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    init_sounds()
    game = Game(screen)
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)
        game.update(dt)
        game.draw()
        pygame.display.flip()
    pygame.quit()
if __name__ == '__main__':
    main()