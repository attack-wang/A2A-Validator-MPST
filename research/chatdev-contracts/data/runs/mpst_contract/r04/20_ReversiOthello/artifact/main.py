from game import Board, BLACK, WHITE
import ui


def other(player):
    return WHITE if player == BLACK else BLACK


def main():
    board = Board()
    player = BLACK
    consecutive_passes = 0
    while True:
        moves = board.valid_moves(player)
        ui.render(board, moves)
        if not moves:
            if board.is_full() or consecutive_passes >= 1:
                break
            consecutive_passes += 1
            print(f'\n{player} has no valid move and must pass.')
            player = other(player)
            continue
        consecutive_passes = 0
        try:
            text = input(f'\n{player} move (e.g. d3, q to quit): ')
        except (EOFError, KeyboardInterrupt):
            print('\nGame aborted.')
            return
        if text.strip().lower() in ('q', 'quit', 'exit'):
            print('Game aborted.')
            return
        pos = ui.parse_move(text)
        if pos is None or pos not in moves:
            print('Invalid move. Choose a square marked with *.')
            continue
        flipped = board.apply_move(pos[0], pos[1], player)
        print(f'{player} played {ui.COLS[pos[1]]}{pos[0] + 1}, flipped {len(flipped)} disc(s).')
        player = other(player)
    black, white = board.score()
    ui.render(board, set())
    print(f'\nGame over. Final score -> Black: {black}  White: {white}')
    if black > white:
        print('Black wins!')
    elif white > black:
        print('White wins!')
    else:
        print("It's a draw!")


if __name__ == '__main__':
    main()