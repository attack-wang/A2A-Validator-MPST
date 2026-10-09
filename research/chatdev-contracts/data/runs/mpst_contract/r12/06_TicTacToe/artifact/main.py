"""Entry point for the two-player console tic-tac-toe game."""

from game import TicTacToe
from ui import announce, play_again, print_board, prompt_move


def run_game():
    """Play one full round. Returns True if completed, False if the user quit."""
    game = TicTacToe()
    print("\nNew round! Player X goes first.")
    print("Cells are numbered 1-9, left to right, top to bottom.")
    while True:
        print_board(game.board)
        move = prompt_move(game.current, game.available_moves())
        if move is None:
            print("Round ended by player.")
            return False
        game.make_move(move)
        result = game.check_winner()
        if result:
            print_board(game.board)
            announce(result)
            return True
        game.switch_player()


def main():
    print("Welcome to Tic-Tac-Toe!")
    while run_game():
        if not play_again():
            break
    print("Thanks for playing!")


if __name__ == "__main__":
    main()