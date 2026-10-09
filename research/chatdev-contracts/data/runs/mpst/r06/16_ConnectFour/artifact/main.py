'''
main.py
Entry point of the Connect Four application. It creates a Game instance,
runs the match, and offers a rematch until the players decide to quit.
Input-stream failures (EOFError) and user interrupts (KeyboardInterrupt)
are caught at the top level so the program always exits gracefully.
'''
from game import Game
def main():
    """Start Connect Four and loop over rematches until the user quits."""
    print("=" * 40)
    print("           CONNECT FOUR")
    print("=" * 40)
    while True:
        game = Game()
        try:
            game.play()
        except (EOFError, KeyboardInterrupt):
            print("\nGame aborted. Thanks for playing Connect Four. Goodbye!")
            break
        try:
            again = input("Play again? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nThanks for playing Connect Four. Goodbye!")
            break
        # Accept both 'y' and 'yes' for a friendlier rematch experience.
        if again not in ('y', 'yes'):
            print("Thanks for playing Connect Four. Goodbye!")
            break
if __name__ == '__main__':
    main()