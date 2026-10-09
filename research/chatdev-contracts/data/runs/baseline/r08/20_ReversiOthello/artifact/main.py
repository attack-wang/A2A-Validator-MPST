'''
main.py
Entry point for the Reversi (Othello) console application. Optionally
asks for the players' names, creates a Game instance and starts the match.
EOF-safe: falls back to default player names when stdin is unavailable
(automated tests, piped or closed stdin) instead of crashing with EOFError.
'''
from game import Game
def prompt_name(prompt: str, default: str) -> str:
    """Ask for a name; fall back to the default on EOF or empty input."""
    try:
        answer = input(prompt).strip()
    except EOFError:
        # Non-interactive environment (tests, piped stdin): no name can be
        # read, so use the default instead of crashing with EOFError.
        answer = ""
    return answer or default
def main():
    """Set up and run a full two-player Reversi game."""
    print("Player 1 plays Black (X) and moves first.")
    black_name = prompt_name(
        "Enter name for Player 1 (Black) [default 'Player 1']: ", "Player 1")
    white_name = prompt_name(
        "Enter name for Player 2 (White) [default 'Player 2']: ", "Player 2")
    game = Game(black_name, white_name)
    game.run()
if __name__ == "__main__":
    main()