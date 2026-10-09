"""Entry point for the Reversi (Othello) console game."""

from board import Board
from game import Game
import ui


def main():
    game = Game()
    print('Welcome to Reversi (Othello)! X = Black, O = White, * = valid move.')
    print('Enter moves as row+column, e.g. 3d. Enter q to quit.')
    while not game.over():
        moves = ui.show_status(game)
        if not moves:
            name = 'Black' if game.current == Board.BLACK else 'White'
            print(f'No valid moves for {name}; turn passes.')
            game.switch_turn()
            continue
        move = ui.read_move(moves)
        if move is None:
            print('Game aborted.')
            return
        game.step(*move)
    black, white = game.board.score()
    print(ui.render(game.board, {}))
    print(f'Final score - Black (X): {black}  White (O): {white}')
    if black > white:
        print('Black wins!')
    elif white > black:
        print('White wins!')
    else:
        print("It's a draw!")


if __name__ == '__main__':
    main()