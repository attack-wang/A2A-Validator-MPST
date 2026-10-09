'''
Entry point for the Connect Four game.
Builds the board and the two players, then runs full matches in a
rematch loop until the users choose to quit. KeyboardInterrupt (Ctrl+C)
and EOFError (Ctrl+D or a closed input stream) are caught around the
entire match loop — including the rematch prompt — so the game always
exits gracefully instead of crashing with a raw traceback.
'''
from game import Game
from player import Player
def build_players():
    """Create the two default participants with discs 'X' and 'O'."""
    return [Player("Player 1", 'X'), Player("Player 2", 'O')]
def ask_rematch():
    """Return True if the users want to play another match."""
    while True:
        answer = input("\nPlay again? (y/n): ").strip().lower()
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        print("Please answer 'y' or 'n'.")
def main():
    """Start and repeat Connect Four matches until the users quit.
    Both KeyboardInterrupt and EOFError are handled centrally so that
    every input prompt (column choice and rematch question) terminates
    the program with a friendly farewell message.
    """
    try:
        while True:
            game = Game(players=build_players())
            game.play()
            if not ask_rematch():
                print("Thanks for playing Connect Four. Goodbye!")
                return
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
    except EOFError:
        print("\nInput stream closed. Goodbye!")
if __name__ == '__main__':
    main()