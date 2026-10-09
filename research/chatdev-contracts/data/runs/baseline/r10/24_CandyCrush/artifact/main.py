def main():
    pygame.init()
    screen = ...
    clock = ...
    game = Game()
    renderer = Renderer(screen)
    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            QUIT → running=False
            KEYDOWN: R → restart; H → hint; ESC → quit
            MOUSEBUTTONDOWN/UP/MOTION → game.handle_event
        game.update(dt)
        renderer.draw(game)
        pygame.display.flip()
    pygame.quit()