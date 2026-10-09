"""Entry point for the two-player tic-tac-toe game."""

from game import TicTacToe
from ui import ConsoleUI


def main():
    ui = ConsoleUI()
    while True:
        ui.show_welcome()
        ui.play_game(TicTacToe())
        if not ui.ask_replay():
            ui.show_goodbye()
            break


if __name__ == "__main__":
    main()