'''
main.py
Entry point: initialises pygame, loads fonts, runs the main game loop
and dispatches keyboard events (W/A/S/D movement, R restart).
'''
import sys
import pygame
import settings
import renderer
from game import Game
def _load_fonts():
    '''Load the four fonts used across the game (title, normal, small, tile).'''
    title_font = pygame.font.SysFont("consolas", settings.FONT_SIZE_TITLE, bold=True)
    normal_font = pygame.font.SysFont("consolas", settings.FONT_SIZE_NORMAL)
    small_font = pygame.font.SysFont("consolas", settings.FONT_SIZE_SMALL)
    tile_font = pygame.font.SysFont("consolas", settings.FONT_SIZE_TILE, bold=True)
    return (title_font, normal_font, small_font, tile_font)
def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH,
                                      settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Tower of the Sorcerer - Roguelike")
    clock = pygame.time.Clock()
    fonts = _load_fonts()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    game.handle_key(event.key)
        renderer.draw(screen, game, fonts)
        clock.tick(30)
    pygame.quit()
    sys.exit(0)
if __name__ == "__main__":
    main()