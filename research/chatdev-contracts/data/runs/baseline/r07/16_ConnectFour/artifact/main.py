'''
main.py
Entry point of the Connect Four application. It greets the users,
collects the players' names, builds the Player and Game objects, and
runs matches until the players decide to stop. Every interactive
read goes through the safe_input helper, so a closed or exhausted
standard input stream (as found in automated test environments)
falls back to default names, stops further matches, and shuts the
program down gracefully instead of raising an unhandled EOFError.
'''
from game import Game
from player import Player
from io_utils import safe_input, InputClosed
def prompt_player_name(default_name: str, disc: str) -> str:
    """
    Ask for a player's name, falling back to a sensible default.
    Args:
        default_name: Name used when the user presses Enter or when
            the input stream is unavailable.
        disc: The disc symbol assigned to this player.
    Returns:
        The chosen (or default) player name.
    """
    raw = safe_input(
        f"Enter a name for {default_name} (plays '{disc}', "
        "press Enter to keep the default): "
    )
    if raw is None:
        # stdin closed or interrupted: keep the default name.
        return default_name
    raw = raw.strip()
    return raw if raw else default_name
def ask_play_again() -> bool:
    """
    Ask whether the players want another match. A closed or
    interrupted input stream is treated as a 'no' so the program
    exits cleanly.
    """
    while True:
        answer = safe_input("Play again? (y/n): ")
        if answer is None:
            return False
        answer = answer.strip().lower()
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        print("Please answer with 'y' or 'n'.")
def main() -> None:
    """Set up the players and run Connect Four matches."""
    print("=" * 46)
    print("           CONNECT FOUR - Python Edition")
    print("=" * 46)
    print("Rules: Two players take turns dropping discs into a")
    print("7-column, 6-row grid. The first player to line up four")
    print("of their discs horizontally, vertically, or diagonally")
    print("wins. If the grid fills up with no line of four, the")
    print("game ends in a draw.")
    name_one = prompt_player_name("Player 1", "X")
    name_two = prompt_player_name("Player 2", "O")
    player_one = Player(name_one, "X")
    player_two = Player(name_two, "O")
    game = Game(player_one, player_two)
    try:
        while True:
            try:
                game.play()
            except InputClosed:
                print("\nInput stream closed. Ending the session. "
                      "Goodbye!")
                return
            if not ask_play_again():
                print("Thanks for playing Connect Four. Goodbye!")
                break
            game.reset()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
if __name__ == "__main__":
    main()