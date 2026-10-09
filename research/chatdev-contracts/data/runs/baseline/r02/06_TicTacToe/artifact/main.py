'''
main.py
Entry point for the Tic-Tac-Toe game.
This module wires everything together: it greets the user, collects the
two players' names, builds the Game object, and keeps starting matches
until the players decide to quit. All interactive prompts use the
centralized safe_input() helper so the program exits gracefully (no
traceback, exit code 0) when standard input is closed or exhausted, and
the entry point additionally catches KeyboardInterrupt/EOFError as a
final safety net.
'''
from game import Game
from player import Player
from io_utils import safe_input
def get_player_info(symbol):
    """Ask for a player's name and return a Player with the given symbol."""
    name = safe_input(f"Enter name for Player {symbol}: ").strip()
    if not name:
        name = f"Player {symbol}"
    return Player(name, symbol)
def main():
    """Set up the players and run matches until the users choose to stop."""
    print("=" * 45)
    print("                 TIC-TAC-TOE")
    print("        Two players | 3x3 grid | X and O")
    print("=" * 45)
    player_x = get_player_info('X')
    player_o = get_player_info('O')
    while True:
        game = Game(player_x, player_o)
        game.play()
        if not game.rematch():
            print("\nThanks for playing Tic-Tac-Toe. Goodbye!")
            break
if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Safety net: any input path that still reaches EOF or Ctrl+C
        # terminates cleanly instead of showing a raw traceback.
        print("\n\nGame ended. Thanks for playing Tic-Tac-Toe. Goodbye!")