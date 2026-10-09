'''
Entry point for the Gomoku game.
Tries to launch the pygame-based graphical version; if pygame is not
installed (ModuleNotFoundError/ImportError) it gracefully falls back to
a fully playable console version so the program always runs instead of
crashing. In GUI mode the loop is frame-rate limited to 60 FPS to avoid
wasting CPU, and pygame resources are always cleaned up on exit via
try/finally.
'''
from game import Game
def main():
    """Run the Gomoku game (GUI when pygame is available, else console)."""
    game = Game(board_size=15)
    try:
        import pygame
        from gui import GUI
    except ImportError:
        # pygame is missing -> run the text-based fallback, do not crash.
        print("pygame is not installed - switching to console mode.")
        print("Tip: run 'pip install pygame' to enable the graphical version.\n")
        from console import ConsoleUI
        ConsoleUI(game).run()
        return
    gui = GUI(game)
    clock = pygame.time.Clock()  # Limits frame rate to avoid CPU hogging
    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    gui.handle_event(event)
            gui.render()
            clock.tick(60)  # Cap at ~60 FPS; enough for smooth interaction
    finally:
        gui.quit()
if __name__ == "__main__":
    main()