from game import Board, BLACK, WHITE


def test_initial_position():
    b = Board()
    assert b.score() == (2, 2)
    assert b.valid_moves(BLACK) == {(2, 3), (3, 2), (4, 5), (5, 4)}
    assert b.valid_moves(WHITE) == {(2, 4), (3, 5), (4, 2), (5, 3)}


def test_flip_and_score():
    b = Board()
    assert b.apply_move(2, 3, BLACK)
    assert b.grid[3][3] == BLACK
    assert b.score() == (4, 1)
    assert not b.apply_move(2, 3, WHITE)
    assert not b.apply_move(0, 0, WHITE)


def test_full_board_detection():
    b = Board()
    b.grid = [[BLACK] * 8 for _ in range(8)]
    assert b.is_full()
    assert b.valid_moves(WHITE) == set()


if __name__ == '__main__':
    test_initial_position()
    test_flip_and_score()
    test_full_board_detection()
    print('All tests passed.')