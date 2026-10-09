'''
main.py
Entry point for the Classic Snake game. Creates the Game instance and
starts the main loop. Gracefully reports a missing 'pygame' dependency
instead of crashing with a raw traceback.
'''
import sys
def main():
    # Dependency guard: pygame must be installed before the game can run.
    try:
        import pygame
    except ImportError:
        print("ERROR: the 'pygame' module is required but not installed.")
        print("Install it with:  pip install pygame")
        sys.exit(1)
    from game import Game
    game = Game()
    try:
        game.run()
    finally:
        pygame.quit()
if __name__ == "__main__":
    main()