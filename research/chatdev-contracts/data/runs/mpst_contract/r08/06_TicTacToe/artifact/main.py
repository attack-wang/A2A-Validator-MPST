from game import TicTacToe
from ui import ConsoleUI


def main():
    ui = ConsoleUI()
    game = TicTacToe()
    ui.show_welcome()
    while True:
        ui.render(game)
        row, col = ui.get_move(game.current_player)
        if not game.place(row, col):
            ui.show_invalid()
            continue
        winner = game.check_winner()
        if winner or game.is_full():
            ui.render(game)
            ui.show_result(winner)
            break
        game.switch_player()


if __name__ == "__main__":
    main()