'''
main.py
Entry point of the Connect Four application. Builds a Game and starts
the interactive match; after each finished game it offers a rematch
until the user chooses to quit.
'''
from game import Game
def main():
    """Start Connect Four and keep offering rematches until the user quits."""
    while True:
        game = Game()
        game.play()
        answer = input("Play again? (y/n): ").strip().lower()
        if answer != 'y':
            print("Thanks for playing Connect Four. Goodbye!")
            break
if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted. Goodbye!")