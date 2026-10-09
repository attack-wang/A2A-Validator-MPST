def main():
    board = Board()
    print("=== Terminal Chess (two players) ===")
    print("Enter moves in algebraic notation, e.g. e4, Nf3, exd5, O-O, e8=Q")
    print("Coordinate form (e2e4) is also accepted. Type 'quit' to exit, 'help' for help.")
    while True:
        print()
        print(board.render())
        status = board.game_status()
        name = 'White' if board.turn == 'w' else 'Black'
        if status == 'checkmate':
            winner = 'Black' if board.turn == 'w' else 'White'
            print(f"Checkmate! {winner} wins.")
            break
        if status == 'stalemate':
            print("Stalemate — the game is a draw.")
            break
        if status == 'draw50':
            print("Draw by the fifty-move rule.")
            break
        if status == 'draw_rep':
            print("Draw by threefold repetition.")
            break
        if board.in_check(board.turn):
            print(f"{name} is in check!")
        print(f"{board.fullmove_number}. {name} to move:", end=' ')
        text = input().strip()
        if text.lower() in ('quit', 'exit', 'q'):
            print("Game aborted.")
            break
        if text.lower() in ('help', 'h'):
            print_help()
            continue
        move, promotion = parse_input(board, text)
        if move is None:
            print("Illegal or unrecognised move. Please try again.")
            continue
        if promotion == 'ASK':
            promotion = ask_promotion()
        san = san_for(board, move, promotion if promotion in ('Q','R','B','N') else None)
        board.make_move(move, promotion if promotion in ('Q','R','B','N') else None)
        print(f"Played: {san}")