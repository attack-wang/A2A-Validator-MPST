'''
main.py
Entry point for the interactive storytelling game. Creates the Game and
starts the main loop; catches keyboard interrupts gracefully.
'''
from game import Game
def main():
    """Instantiate and run the game."""
    game = Game()
    try:
        game.start()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye.")
if __name__ == "__main__":
    main()