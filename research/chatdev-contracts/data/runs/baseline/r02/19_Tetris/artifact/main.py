def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Tetris - ChatDev')
    clock = pygame.time.Clock()
    game = Game()
    renderer = Renderer(screen)
    controller = InputController(game)
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                controller.handle_event(event)
        controller.update(dt)
        game.update(dt)
        renderer.draw(game)
    pygame.quit()
    sys.exit()