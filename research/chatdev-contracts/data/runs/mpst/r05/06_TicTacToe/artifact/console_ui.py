'''
console_ui.py
A lightweight console front-end for the tic-tac-toe game, used when the
game is started with the --console flag or when no graphical display is
available. Players enter moves as "row column" pairs using numbers 1-3,
and may type 'q' at any prompt to quit.
'''
from board import Board
from game_logic import TicTacToeGame
class ConsoleUI:
    """Text-based front-end for a TicTacToeGame instance."""
    def __init__(self, game=None):
        self._game = game if game is not None else TicTacToeGame()
    def run(self):
        """Main loop: keep playing rounds until the user quits."""
        self._print_welcome()
        while True:
            round_finished = self._play_round()
            if not round_finished:
                # User aborted the round with 'q' -> leave the loop entirely.
                break
            if not self._ask_play_again():
                break
            self._game.reset()
        print("Thanks for playing Tic-Tac-Toe! Goodbye.")
    def _print_welcome(self):
        """Print the greeting and input instructions."""
        print("=" * 40)
        print("       TIC-TAC-TOE (two players)")
        print("=" * 40)
        print("Player 1 is X, Player 2 is O. X moves first.")
        print("Enter moves as 'row column' using numbers 1-3,")
        print("e.g. '2 3' places your mark in row 2, column 3.")
        print("Type 'q' at any prompt to quit.\n")
    def _play_round(self):
        """
        Play a single round until somebody wins or the board fills.
        Returns True when the round finished normally, False when the
        user quit mid-round with 'q'.
        """
        self._game.reset()
        while not self._game.game_over:
            self._show_board()
            move = self._prompt_move()
            if move is None:          # user typed 'q'
                print("Game aborted.")
                return False
            row, col = move
            if not self._game.make_move(row, col):
                print("That cell is not free. Try again.\n")
                continue
            print()
        self._show_board()
        self._announce_result()
        return True
    def _show_board(self):
        """Print the board with 1-3 row/column guides for easier input."""
        print("    1   2   3")
        print("  " + "-" * 13)
        for r in range(Board.SIZE):
            cells = [self._game.board.get_cell(r, c) for c in range(Board.SIZE)]
            print("{} | {} | {} | {}".format(r + 1, cells[0], cells[1], cells[2]))
            if r < Board.SIZE - 1:
                print("  " + "-" * 13)
        print()
    def _prompt_move(self):
        """
        Ask the current player for a move.
        Returns a 0-based (row, col) tuple for a valid position, or None
        when the user types 'q' to quit.
        """
        while True:
            raw = input("Player {} - row col (1-3) or 'q': "
                        .format(self._game.current_player)).strip().lower()
            if raw == "q":
                return None
            parts = raw.replace(",", " ").split()
            if len(parts) != 2:
                print("Enter two numbers, e.g. '2 3'.\n")
                continue
            try:
                row, col = int(parts[0]) - 1, int(parts[1]) - 1
            except ValueError:
                print("Rows/columns must be numbers 1-3.\n")
                continue
            if not (0 <= row < Board.SIZE and 0 <= col < Board.SIZE):
                print("Rows and columns must be between 1 and 3.\n")
                continue
            return row, col
    def _announce_result(self):
        """Print the outcome of the finished round."""
        winner = self._game.winner
        if winner is not None:
            print("Player {} wins! Three in a row!\n".format(winner))
        else:
            print("It's a draw! The board is full with no winner.\n")
    def _ask_play_again(self):
        """Ask whether the players want another round; returns True/False."""
        while True:
            answer = input("Play again? (y/n): ").strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print("Please answer 'y' or 'n'.")