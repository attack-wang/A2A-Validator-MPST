"""Console UI helpers: display and input."""
SEPARATOR = "=" * 62
def print_separator():
    print(SEPARATOR)
def header(title):
    print_separator()
    print(title.center(len(SEPARATOR)))
    print_separator()
def announce(msg):
    print(f"  {msg}")
def show_player_status(player, board):
    space = board.get_space(player.position)
    props = ", ".join(p.name for p in player.properties) or "none"
    print(f"  {player.name}: ${player.money} | at {space.name} | "
          f"properties: {props} | jail cards: {player.get_out_of_jail_cards}")
def show_board(board, players):
    token_map = {}
    for p in players:
        token_map.setdefault(p.position, []).append(p.name)
    for space in board.spaces:
        line = f"[{space.index:2d}] {space.name:<24}"
        if space.kind == "property":
            owner = space.owner.name if space.owner else "unowned"
            line += f"${space.price:<4} rent ${space.rent:<3} owner: {owner:<12}"
        here = ", ".join(token_map.get(space.index, []))
        if here:
            line += f" * {here}"
        print(line)
def prompt(message):
    return input(message)
def prompt_yes_no(message):
    while True:
        answer = input(message).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please answer 'y' or 'n'.")
def prompt_choice(message, options):
    while True:
        answer = input(message).strip().lower()
        if answer in options:
            return answer
        print(f"  Please choose one of: {', '.join(options)}")