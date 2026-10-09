#!/usr/bin/env python3
"""Checkers (Draughts): two-player console game with standard rules."""

def new_board():
    b = [['.' for _ in range(8)] for _ in range(8)]
    for r in range(8):
        for c in range(8):
            if (r + c) % 2 == 1:
                if r < 3:
                    b[r][c] = 'b'
                elif r > 4:
                    b[r][c] = 'r'
    return b

def parse_sq(s):
    s = s.strip().lower()
    if len(s) == 2 and 'a' <= s[0] <= 'h' and '1' <= s[1] <= '8':
        return (8 - int(s[1]), ord(s[0]) - 97)
    return None

def fmt_sq(r, c):
    return chr(97 + c) + str(8 - r)

def print_board(b):
    print()
    print('    a b c d e f g h')
    for r in range(8):
        print('  %d %s %d' % (8 - r, ' '.join(b[r]), 8 - r))
    print('    a b c d e f g h')
    print("Red = r/R (bottom, moves up) | Black = b/B (top, moves down)")

def dirs(p):
    if p.isupper():
        return ((-1, -1), (-1, 1), (1, -1), (1, 1))
    return ((-1, -1), (-1, 1)) if p == 'r' else ((1, -1), (1, 1))

def ok(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def jumps(b, r, c):
    p = b[r][c]
    out = []
    for dr, dc in dirs(p):
        mr, mc, tr, tc = r + dr, c + dc, r + 2 * dr, c + 2 * dc
        if ok(tr, tc) and b[tr][tc] == '.' and b[mr][mc] != '.' \
                and b[mr][mc].lower() != p.lower():
            out.append((tr, tc))
    return out

def slides(b, r, c):
    p = b[r][c]
    return [(r + dr, c + dc) for dr, dc in dirs(p)
            if ok(r + dr, c + dc) and b[r + dr][c + dc] == '.']

def any_move(b, pl):
    for r in range(8):
        for c in range(8):
            if b[r][c].lower() == pl and (slides(b, r, c) or jumps(b, r, c)):
                return True
    return False

def any_jump(b, pl):
    for r in range(8):
        for c in range(8):
            if b[r][c].lower() == pl and jumps(b, r, c):
                return True
    return False

def apply(b, fr, fc, tr, tc):
    p = b[fr][fc]
    b[fr][fc] = '.'
    if abs(tr - fr) == 2:
        b[(fr + tr) // 2][(fc + tc) // 2] = '.'
    if p == 'r' and tr == 0:
        p = 'R'
    elif p == 'b' and tr == 7:
        p = 'B'
    b[tr][tc] = p
    return p

def main():
    b = new_board()
    player = 'r'
    chain = None
    print("Checkers (Draughts) - 8x8 board, two players.")
    print("Move notation: from-to, e.g. 'c3-d4' or capture 'c3-e5'.")
    print("Commands: 'board' redraws, 'quit' exits. Captures are mandatory;")
    print("multi-jumps continue with the same piece until no jump remains.")
    while True:
        if not any_move(b, player):
            print_board(b)
            print(("Black" if player == 'r' else "Red") + " wins - " +
                  ("Red" if player == 'r' else "Black") + " has no moves or pieces!")
            break
        print_board(b)
        name = 'Red' if player == 'r' else 'Black'
        must = any_jump(b, player)
        hint = " (capture required)" if must else ""
        if chain:
            hint = " (must keep jumping from %s)" % fmt_sq(*chain)
        try:
            raw = input(name + "'s move" + hint + ": ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGame ended.")
            break
        if raw in ('quit', 'exit', 'q'):
            print("Game ended.")
            break
        if raw == 'board':
            continue
        parts = [p for p in raw.replace('x', '-').replace(',', '-').replace(' ', '-').split('-') if p]
        if len(parts) != 2:
            print("Invalid input. Use from-to like 'c3-d4'.")
            continue
        f, t = parse_sq(parts[0]), parse_sq(parts[1])
        if not f or not t:
            print("Invalid square. Use a-h and 1-8, e.g. 'c3'.")
            continue
        fr, fc = f
        tr, tc = t
        if chain and (fr, fc) != chain:
            print("You must continue jumping from %s." % fmt_sq(*chain))
            continue
        if b[fr][fc] == '.' or b[fr][fc].lower() != player:
            print("That square does not hold your piece.")
            continue
        if b[tr][tc] != '.':
            print("Destination is occupied.")
            continue
        dr, dc = tr - fr, tc - fc
        if dr == 0 or abs(dr) != abs(dc):
            print("Moves must be diagonal.")
            continue
        if abs(dr) == 1:
            if must:
                print("A capture is available; you must jump.")
                continue
            if (tr, tc) not in slides(b, fr, fc):
                print("Illegal step for that piece (men move forward only).")
                continue
            apply(b, fr, fc, tr, tc)
            chain = None
        elif abs(dr) == 2:
            if (tr, tc) not in jumps(b, fr, fc):
                print("Illegal jump (no enemy piece to capture that way).")
                continue
            before = b[fr][fc]
            after = apply(b, fr, fc, tr, tc)
            chain = (tr, tc) if after == before and jumps(b, tr, tc) else None
        else:
            print("Too far: move at most 2 squares diagonally.")
            continue
        if chain is None:
            player = 'b' if player == 'r' else 'r'

if __name__ == '__main__':
    main()