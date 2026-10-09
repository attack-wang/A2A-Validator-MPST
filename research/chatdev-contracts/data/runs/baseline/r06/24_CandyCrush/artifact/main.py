import sys
import pygame
import constants as c
from game import Game
from renderer import Renderer
def main():
    pygame.init()
    screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
    pygame.display.set_caption("Candy Match")
    clock = pygame.time.Clock()
    game = Game()
    renderer = Renderer(screen)
    running = True
    while running:
        dt = clock.tick(c.FPS) / 1000.0
        dt = min(dt, 0.05)  # clamp to avoid huge jumps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    game.reset()
                elif event.key == pygame.K_h:
                    game.request_hint()
        game.update(dt)
        renderer.draw(game)
        pygame.display.flip()
    pygame.quit()
    sys.exit(0)
if __name__ == "__main__":
    main()