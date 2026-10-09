'''
Module: main.py
Entry point for the Connect Four application. It starts a game session,
lets the two players play until a win or a draw is reached, and offers
to restart with a clean board afterwards. Ctrl+C exits gracefully, and
a closed or exhausted input stream (EOFError, e.g. in a non-interactive
test harness) now also terminates the session cleanly with a friendly
goodbye message instead of crashing with a raw traceback.
'''
from game import Game
def main():
    """Run Connect Four sessions in a loop until the players choose to quit."""
    while True:
        game = Game()
        game.play()
        try:
            again = input("Play again? (y/n): ").strip().lower()
        except EOFError:
            # stdin ended after a finished game; exit gracefully, no traceback.
            print("\nInput stream closed. Thanks for playing Connect Four. Goodbye!")
            break
        if again != 'y':
            print("Thanks for playing Connect Four. Goodbye!")
            break
if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Catches EOFError re-raised from Player.get_move when stdin is
        # exhausted, and Ctrl+C during interactive play.
        print("\nGame ended. Goodbye!")