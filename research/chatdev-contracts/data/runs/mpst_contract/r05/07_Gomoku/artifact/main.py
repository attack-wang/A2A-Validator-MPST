from game import GomokuGame
from ui import TerminalUI


def main():
    ui = TerminalUI()
    game = GomokuGame()
    ui.show_welcome()
    while True:
        ui.draw(game)
        player = game.current_player()
        move = ui.get_move(player)
        if move is None:
            ui.show_message("Game aborted by player.")
            break
        ok, msg = game.place(move[0], move[1])
        if not ok:
            ui.show_message(msg)
            continue
        winner = game.check_winner()
        if winner:
            ui.draw(game)
            ui.show_message("*** {} ({}) wins with five in a row! ***".format(
                game.name(winner), game.stone(winner)))
            break
        if game.is_full():
            ui.draw(game)
            ui.show_message("Draw! The board is full.")
            break
        game.switch_player()


if __name__ == "__main__":
    main()