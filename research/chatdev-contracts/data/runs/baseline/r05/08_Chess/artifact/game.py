def san_for_move(move, legal_moves):
    """Build the SAN string for a move, given the full list of legal moves
    in the current position (for disambiguation)."""
    if move.is_castle_kingside:
        base = 'O-O'
    elif move.is_castle_queenside:
        base = 'O-O-O'
    else:
        piece = move.piece
        letter = '' if piece.kind == 'P' else piece.kind
        disambig = ''
        if piece.kind != 'P':
            others = [m for m in legal_moves
                      if m.piece is not None and m.piece.kind == piece.kind
                      and m.to_sq == move.to_sq and m.from_sq != move.from_sq]
            if others:
                same_file = any(m.from_sq[0] == move.from_sq[0] for m in others)
                same_rank = any(m.from_sq[1] == move.from_sq[1] for m in others)
                if not same_file:
                    disambig = chr(ord('a') + move.from_sq[0])
                elif not same_rank:
                    disambig = str(move.from_sq[1] + 1)
                else:
                    disambig = square_name(move.from_sq)
        capture = move.captured is not None
        if piece.kind == 'P':
            base = (chr(ord('a') + move.from_sq[0]) + ('x' if capture else '')
                    + square_name(move.to_sq))
        else:
            base = letter + disambig + ('x' if capture else '') + square_name(move.to_sq)
        if move.promotion:
            base += '=' + move.promotion
    return base