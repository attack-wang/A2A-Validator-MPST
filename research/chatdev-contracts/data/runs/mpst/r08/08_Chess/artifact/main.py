'''
main.py
Entry point: two-player terminal chess. Prints the board after every move,
reads SAN moves from the terminal, enforces check/checkmate/stalemate and
supports castling, en passant and pawn promotion.
Run with: python main.py
'''
from board import Board, Move
from san import parse_san
def choose_promotion(promo_moves):
    while True:
        choice = input('Promote pawn to (Q/R/B/N): ').strip().upper()
        if choice in ('Q', 'R', 'B', 'N'):
            break
        print('Please enter Q, R, B, or N.')
    for mv in promo_moves:
        if mv.promotion == choice:
            return mv
    return promo_moves[0]
def main():
    board = Board()
    turn = 'w'
    names = {'w': 'White', 'b': 'Black'}
    move_no = 1
    print('=== Terminal Chess (two players) ===')
    print("Enter moves in SAN, e.g. e4, Nf3, exd5, O-O, e8=Q. Type 'quit' to resign.")
    while True:
        legal = board.legal_moves(turn)
        if not legal:
            print(board.render())
            if board.in_check(turn):
                print(f'Checkmate! {names[board.opponent(turn)]} wins.')
            else:
                print('Stalemate! The game is a draw.')
            break
        print()
        print(board.render())
        prompt = f'{move_no}. {names[turn]}'
        if board.in_check(turn):
            prompt += ' (CHECK)'
        try:
            text = input(f'{prompt} to move: ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print('Game aborted.')
            break
        if text.lower() in ('quit', 'exit', 'resign'):
            print(f'{names[turn]} resigns. {names[board.opponent(turn)]} wins.')
            break
        result, error = parse_san(board, turn, text, legal)
        if error:
            print(error)
            continue
        if isinstance(result, tuple) and result[0] == 'PROMOTE':
            move = choose_promotion(result[1])
        else:
            move = result
        board.make_move(move)
        note = ''
        if board.in_check(board.opponent(turn)):
            note = '  (Check!)'
        print(f'{names[turn]} plays {move.san()}.{note}')
        if turn == 'b':
            move_no += 1
        turn = board.opponent(turn)
if __name__ == '__main__':
    main()