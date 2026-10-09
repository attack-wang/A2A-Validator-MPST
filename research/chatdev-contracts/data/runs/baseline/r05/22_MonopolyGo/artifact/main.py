'''
main.py
Entry point for the simplified Monopoly Go! game.
Robust in non-interactive environments: falls back to default players
when stdin is closed (EOF) instead of crashing with EOFError.
Usage: python main.py [name1 name2 ...]
'''
import sys
from game import Game
DEFAULT_NAMES = ["Alice", "Bob"]
MAX_PLAYERS = 6
MIN_PLAYERS = 2
def safe_input(prompt, default=None):
    """input() that returns `default` on EOF/Ctrl-D/Ctrl-Z instead of raising."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return default
def collect_player_names():
    """Collect 2-6 player names from CLI args, stdin, or defaults."""
    # 1) Command-line names — ideal for automated/test runs.
    cli_names = [a.strip() for a in sys.argv[1:] if a.strip()]
    if len(cli_names) >= MIN_PLAYERS:
        return cli_names[:MAX_PLAYERS]
    # 2) Interactive entry, tolerant of EOF.
    print(f"Enter player names ({MIN_PLAYERS}-{MAX_PLAYERS} players). "
          "Press Enter without typing a name to start.")
    names = []
    while len(names) < MAX_PLAYERS:
        raw = safe_input(f"Player {len(names) + 1} name: ")
        if raw is None:  # EOF / Ctrl-C -> stop prompting
            break
        name = raw.strip()
        if name:
            if name in names:
                print("Name already taken — choose another.")
                continue
            names.append(name)
        elif len(names) >= MIN_PLAYERS:
            break
        else:
            print(f"At least {MIN_PLAYERS} players are required.")
    # 3) Graceful fallback when no usable input exists.
    if len(names) < MIN_PLAYERS:
        print("Interactive input unavailable — using default players: "
              + ", ".join(DEFAULT_NAMES))
        names = list(DEFAULT_NAMES)
    return names
if __name__ == "__main__":
    Game(collect_player_names()).play()