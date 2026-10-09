def _simulate(game, move):
    from game import apply_move
    board_copy = game.board.copy()
    apply_move(board_copy, move)
    return board_copy