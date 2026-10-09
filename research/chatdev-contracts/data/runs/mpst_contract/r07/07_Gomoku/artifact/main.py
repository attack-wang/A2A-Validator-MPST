"""Entry point for the Gomoku game."""

from board import Board, BLACK, WHITE
from game import Game
from player import Player
from ui import ConsoleUI


def main():
    ui = ConsoleUI()
    ui.welcome()
    while True:
        black_name, white_name = ui.get_player_names()
        players = [Player(black_name, BLACK), Player(white_name, WHITE)]
        Game(Board(), players, ui).play()
        if not ui.ask_replay():
            ui.farewell()
            break


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\nGame aborted. Goodbye!')