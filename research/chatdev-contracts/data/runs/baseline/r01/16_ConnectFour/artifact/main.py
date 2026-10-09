'''
main.py
Entry point for the Connect Four game. Sets up the two players, the
board, and the game controller, then starts the match. Supports
playing multiple rounds in one session. All interactive prompts are
EOF-safe: when stdin is closed or exhausted (e.g., in non-interactive
or automated environments), the program degrades gracefully instead
of crashing with an unhandled EOFError.
'''
from board import Board
from player import Player
from game import Game
def safe_input(prompt):
    """Read a line from stdin, returning None on EOF or interruption."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return None
def get_player_name(default_name, disc):
    """Ask for a player's name, falling back to a default when blank or on EOF."""
    response = safe_input("Enter name for {} (plays '{}'): ".format(default_name, disc))
    if response is None:
        # Input stream closed/exhausted: use the default name and keep going.
        print()
        return default_name
    name = response.strip()
    return name if name else default_name
def ask_play_again():
    """Ask whether to play another round; returns False on EOF or refusal."""
    response = safe_input("Play again? (y/n): ")
    if response is None:
        print()
        return False
    return response.strip().lower() == 'y'
def main():
    """Create the game components and run matches until the user quits."""
    print("=== Connect Four ===")
    player1 = Player(get_player_name("Player 1", "X"), "X")
    player2 = Player(get_player_name("Player 2", "O"), "O")
    while True:
        board = Board()
        game = Game(board, player1, player2)
        game.play()
        if not ask_play_again():
            print("Thanks for playing Connect Four! Goodbye.")
            break
if __name__ == "__main__":
    main()