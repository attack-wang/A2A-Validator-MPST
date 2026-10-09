'''
console_ui.py
Console fallback interface: lets two players play tic-tac-toe in a terminal
when the graphical interface is unavailable (no tkinter or no display).
'''
from game import Game
def _print_board(grid):
    """Render the 3x3 grid with row/column guides to the terminal."""
    print()
    print("    0   1   2")
    for r in range(3):
        row_cells = " | ".join(grid[r][c] for c in range(3))
        print(f"  {r}  {row_cells}")
        if r < 2:
            print("   ---+---+---")
    print()
def _read_move(player):
    """
    Prompt the current player for a move until a valid 'row col' pair is
    entered. Returns (row, col), or None when the player chooses to quit.
    """
    while True:
        raw = input(
            f"{player.name} ({player.symbol}), enter your move as 'row col' "
            f"(e.g. '1 2'), or 'q' to quit: "
        ).strip().lower()
        if raw in ("q", "quit", "exit"):
            return None
        parts = raw.replace(",", " ").split()
        if len(parts) != 2:
            print("Please enter exactly two numbers, for example: 1 2")
            continue
        try:
            row, col = int(parts[0]), int(parts[1])
        except ValueError:
            print("Rows and columns must be whole numbers between 0 and 2.")
            continue
        if not (0 <= row < 3 and 0 <= col < 3):
            print("Row and column must each be 0, 1, or 2.")
            continue
        return row, col
def run_console_game():
    """Run the interactive turn-based tic-tac-toe loop in the terminal."""
    print("=" * 46)
    print("         TIC-TAC-TOE — Console Edition")
    print("=" * 46)
    print("Coordinates are row then column, both 0-indexed.")
    print("Example: the top-right corner is entered as '0 2'.\n")
    name1 = input("Player 1 name (plays X) [Player 1]: ").strip()[:20] or "Player 1"
    name2 = input("Player 2 name (plays O) [Player 2]: ").strip()[:20] or "Player 2"
    game = Game(name1, name2)
    while True:
        _print_board(game.board.grid)
        print(game.get_status())
        print(game.get_score_text())
        move = _read_move(game.current_player)
        if move is None:
            print("\nGame ended by player. " + game.get_score_text())
            break
        row, col = move
        if not game.make_move(row, col):
            print("That cell is already taken — choose another one.")
            continue
        if game.game_over:
            _print_board(game.board.grid)
            print("*** " + game.get_status() + " ***")
            print(game.get_score_text())
            again = input("\nPlay another round? (y/n): ").strip().lower()
            if again in ("y", "yes"):
                game.reset()
            else:
                print("\nThanks for playing! " + game.get_score_text())
                break