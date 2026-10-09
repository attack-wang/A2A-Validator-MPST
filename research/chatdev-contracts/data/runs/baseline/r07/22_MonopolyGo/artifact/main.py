'''
main.py
Entry point for the simplified Monopoly Go! game.
Creates the Game instance and starts the main loop. Run with:
    python main.py
'''
from game import Game
def main():
    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
if __name__ == "__main__":
    main()