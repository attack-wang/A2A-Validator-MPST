'''
ui.py
Console input/output helpers for the simplified Monopoly Go! game.
EOF-safe: every prompt degrades gracefully to a sensible default when
stdin is closed or exhausted (e.g., automated test runs), so the game
never crashes with EOFError and never loops forever on EOF.
'''
class InputClosed(Exception):
    """Raised when stdin is exhausted (EOF) or interrupted."""
def safe_input(prompt=""):
    """input() that survives closed/empty stdin (e.g., automated test runs)."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        raise InputClosed()
def banner(text):
    """Print a decorative banner around `text`."""
    line = '=' * (len(text) + 8)
    print(f"\n{line}\n   {text}\n{line}")
def show_message(msg):
    """Print a single game message."""
    print(msg)
def turn_header(player, round_no, board):
    """Print the header shown at the start of a player's turn."""
    space = board.get_space(player.position)
    jail = ' [IN JAIL]' if player.in_jail else ''
    print(f"\n--- {player.name}'s turn (Round {round_no}) | "
          f"Money: ${player.money} | Position: {space.name}{jail} ---")
def show_roll(player, dice_pair):
    """Print the dice roll result."""
    print(f"{player.name} rolled {dice_pair[0]} + {dice_pair[1]} = {sum(dice_pair)}")
def show_move(player, space):
    """Print the movement result."""
    print(f"{player.name} moved to {space.name} (space #{player.position}).")
def show_landing(player, space):
    """Print which space the player landed on."""
    print(f"{player.name} landed on {space.name}.")
def show_status(players, board, round_no, pot):
    """Print a summary of every player's money and properties."""
    print(f"\n--- Status after round {round_no} | Free Parking pot: ${pot} ---")
    for p in players:
        props = ', '.join(prop.name for prop in p.properties) or 'none'
        state = ' (BANKRUPT)' if p.bankrupt else (' (IN JAIL)' if p.in_jail else '')
        print(f"  {p.name}: ${p.money}{state} | Properties: {props}")
def prompt_yes_no(question, default=False):
    """Ask a yes/no question; returns True for 'y'. EOF -> `default`."""
    while True:
        try:
            answer = safe_input(f"{question} [y/n]: ").strip().lower()
        except InputClosed:
            return default
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        print("Please answer 'y' or 'n'.")
def prompt_choice(question, options, default=None):
    """Ask the player to choose one of `options` (list of (key, label)); returns the key.
    EOF -> `default` (first option if not given)."""
    default = options[0][0] if default is None else default
    print(question)
    for key, label in options:
        print(f"  [{key}] {label}")
    keys = [key for key, _ in options]
    while True:
        try:
            answer = safe_input("Your choice: ").strip().lower()
        except InputClosed:
            return default
        if answer in keys:
            return answer
        print(f"Please enter one of: {', '.join(keys)}")
def prompt_player_names(default_count=2):
    """Ask how many players (2-4) and their names; returns the list of names.
    EOF -> default count and default names."""
    count = default_count
    try:
        raw = safe_input(f"How many players? (2-4, default {default_count}): ").strip()
        if raw.isdigit() and 2 <= int(raw) <= 4:
            count = int(raw)
    except InputClosed:
        pass
    names = []
    for i in range(count):
        try:
            names.append(safe_input(f"Name of player {i + 1}: ").strip() or f"Player {i + 1}")
        except InputClosed:
            names.append(f"Player {i + 1}")
    return names