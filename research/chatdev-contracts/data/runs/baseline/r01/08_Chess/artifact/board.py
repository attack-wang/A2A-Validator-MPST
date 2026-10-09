def san_for(self, move, legal):
    if move.castle == 'K':
        base = 'O-O'
    elif move.castle == 'Q':
        base = 'O-O-O'
    else:
        if move.piece_type == 'P':
            base = ''
            if move.is_capture:
                base += square_name(move.from_square)[0] + 'x'
            base += square_name(move.to_square)
            if move.promotion:
                base += '=' + move.promotion
        else:
            letter = move.piece_type
            disamb = ''
            others = [m for m in legal
                      if m.piece_type == move.piece_type
                      and m.color == move.color
                      and m.to_square == move.to_square
                      and m.from_square != move.from_square]
            if others:
                same_file = any(m.from_square[1] == move.from_square[1] for m in others)
                same_rank = any(m.from_square[0] == move.from_square[0] for m in others)
                if not same_file:
                    disamb = square_name(move.from_square)[0]
                elif not same_rank:
                    disamb = square_name(move.from_square)[1]
                else:
                    disamb = square_name(move.from_square)
            base = letter + disamb + ('x' if move.is_capture else '') + square_name(move.to_square)
    # suffix added by caller after applying the move
    return base