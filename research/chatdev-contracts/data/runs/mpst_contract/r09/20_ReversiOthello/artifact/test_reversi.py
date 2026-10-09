"""Sanity tests for the Reversi core. Run: python test_reversi.py"""

from reversi import Reversi, BLACK, WHITE, EMPTY


def run_tests():
    game = Reversi()
    assert game.board[3][3] == WHITE and game.board[4][4] == WHITE
    assert game.board[3][4] == BLACK and game.board[4][3] == BLACK
    assert game.board[0][0] == EMPTY
    assert set(game.valid_moves()) == {(2, 3), (3, 2), (4, 5), (5, 4)}
    assert game.apply_move(2, 3)          # d3
    assert game.board[3][3] == BLACK      # disc flipped
    assert game.current == WHITE
    assert not game.apply_move(0, 0)      # illegal move rejected

    full = Reversi()
    for _ in range(64):
        if full.game_over():
            break
        if not full.valid_moves():
            full.pass_turn()
            continue
        row, col = next(iter(full.valid_moves()))
        assert full.apply_move(row, col)
    black, white = full.score()
    assert 4 <= black + white <= 64
    print('All tests passed.')


if __name__ == '__main__':
    run_tests()