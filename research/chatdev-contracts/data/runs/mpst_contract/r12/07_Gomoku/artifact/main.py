"""Console Gomoku: two players alternate placing stones on a 15x15 board."""

from game import Board, BLACK, WHITE, EMPTY


def stone_symbol(player):
    return {BLACK: "X", WHITE: "O", EMPTY: "."}[player]


def render(board):
    header = "   " + " ".join(f"{c:2d}" for c in range(board.size))
    lines = [header]
    for r, row in enumerate(board.grid):
        cells = " ".join(f"{stone_symbol(cell):>2}" for cell in row)
        lines.append(f"{r:2d} {cells}")
    return "\n".join(lines)


def read_move(player_name):
    raw = input(f"{player_name}, enter row and column (e.g. '7 7'): ").strip()
    parts = raw.replace(",", " ").split()
    if len(parts) != 2:
        raise ValueError("Enter exactly two numbers separated by a space.")
    return int(parts[0]), int(parts[1])


def main():
    board = Board()
    players = {BLACK: "Black (X)", WHITE: "White (O)"}
    current = BLACK
    print("Gomoku - first to five in a row wins. Coordinates are 0-14.")
    while True:
        print("\n" + render(board))
        try:
            row, col = read_move(players[current])
        except EOFError:
            print("\nInput stream closed - ending the game.")
            return
        except KeyboardInterrupt:
            print("\nGame interrupted - ending the game.")
            return
        except ValueError as exc:
            print(f"Invalid input: {exc}")
            continue
        if not board.place(row, col, current):
            print("That cell is unavailable. Try again.")
            continue
        winner = board.check_win(row, col)
        if winner:
            print("\n" + render(board))
            print(f"{players[winner]} wins with five in a row!")
            break
        if board.is_full():
            print("\n" + render(board))
            print("The board is full - it's a draw.")
            break
        current = WHITE if current == BLACK else BLACK


if __name__ == "__main__":
    main()