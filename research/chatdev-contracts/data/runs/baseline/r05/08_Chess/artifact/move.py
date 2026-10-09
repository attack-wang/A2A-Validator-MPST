def san_to_move(san, legal_moves):
    """Match a SAN string against the list of legal moves.
    Returns (move, error). move is None on failure."""
    # Strip check/mate suffixes, annotations, and optional 'e.p.' marker
    san = san.strip()
    san = re.sub(r'\s*e\.p\.?', '', san, flags=re.IGNORECASE)
    san = san.rstrip('+#!?')
    m = SAN_PATTERN.match(san)
    if not m:
        return None, f"could not parse '{san}' as standard algebraic notation"
    piece_letter = m.group(1) or 'P'
    from_file = m.group(2)
    from_rank = m.group(3)
    capture = m.group(4) is not None
    target = m.group(5)
    promotion = m.group(6)
    to_sq = parse_square(target)
    candidates = []
    for move in legal_moves:
        if move.to_sq != to_sq:
            continue
        piece = move.piece
        if piece is None or piece.kind != piece_letter:
            continue
        if from_file and chr(ord('a') + move.from_sq[0]) != from_file:
            continue
        if from_rank and str(move.from_sq[1] + 1) != from_rank:
            continue
        if promotion and move.promotion != promotion:
            continue
        if not promotion and move.promotion:
            continue
        candidates.append(move)
    if len(candidates) == 1:
        return candidates[0], None
    if len(candidates) == 0:
        # Special messages for common mistakes
        if piece_letter == 'P' and (to_sq[1] == 7 or to_sq[1] == 0):
            return None, f"Promotion required: use '{san}=Q' (or =R, =B, =N)."
        return None, f"no legal move matches '{san}'"
    return None, f"ambiguous move '{san}'; add a disambiguation file or rank"