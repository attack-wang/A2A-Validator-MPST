"""Reversi (Othello) console game entry point."""

from reversi import Reversi, BLACK


def parse_move(text):
    """Accept 'row col' (1-8) or algebraic notation like 'd3'. Return (row, col) or None."""
    text = text.strip().lower().replace(',', ' ')
    if not text:
        return None
    parts = text.split()
    if len(parts) == 2 and all(p.isdigit() for p in parts):
        r, c = int(parts[0]) - 1, int(parts[1]) - 1
        return (r, c) if 0 <= r < 8 and 0 <= c < 8 else None
    if len(parts) == 1 and len(parts[0]) == 2 \
            and parts[0][0] in 'abcdefgh' and parts[0][1] in '12345678':
        return int(parts[0][1]) - 1, ord(parts[0][0]) - ord('a')
    return None


def render(game):
    lines = ['  ' + ' '.join('abcdefgh')]
    for r in range(8):
        lines.append(f'{r + 1} ' + ' '.join(game.board[r]))
    b, w = game.score()
    lines.append(f'Score - Black (B): {b}  White (W): {w}')
    return '\n'.join(lines)


def main():
    game = Reversi()
    print('Reversi (Othello). Moves: "row col" (1-8) or "d3". Type "q" to quit.')
    while True:
        print('\n' + render(game))
        if game.game_over():
            b, w = game.score()
            result = 'Black wins!' if b > w else 'White wins!' if w > b else 'Draw!'
            print(f'Game over. Final score - Black: {b}, White: {w}. {result}')
            break
        if not game.valid_moves():
            print(f'No valid moves for {game.current}. Turn passes.')
            game.pass_turn()
            continue
        name = 'Black' if game.current == BLACK else 'White'
        try:
            entry = input(f"{name} ({game.current}) move: ").strip()
        except (EOFError, KeyboardInterrupt):
            print('\nGame aborted.')
            break
        if entry.lower() in ('q', 'quit', 'exit'):
            print('Game aborted.')
            break
        move = parse_move(entry)
        if move is None:
            print('Invalid input. Use "row col" (1-8) or "d3".')
            continue
        if not game.apply_move(*move):
            print('Invalid move: that cell is occupied or flips no discs.')
            continue
        b, w = game.score()
        print(f'Move applied. Score - Black: {b}, White: {w}')
        game.pass_turn()


if __name__ == '__main__':
    main()