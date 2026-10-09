def main():
    pygame.init()
    screen = ...
    game = Game()
    renderer = Renderer(screen, game)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if QUIT: running=False
            elif KEYDOWN:
                key mapping: w/K_UP -> (0,-1), a -> (-1,0), s -> (0,1), d -> (1,0)
                r -> restart on game over
                ESC -> quit
                game.handle_move(dx,dy)
        renderer.draw()
        clock.tick(FPS)
    pygame.quit()