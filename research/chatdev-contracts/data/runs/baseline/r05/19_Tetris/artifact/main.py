def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Game()
    renderer = Renderer(screen)
    running = True
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                game.handle_keydown(event.key)  # returns maybe quit signal
        game.update(dt)
        renderer.draw(game)
        pygame.display.flip()
    pygame.quit()