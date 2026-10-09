import re


def parse_pos(s):
    s = s.strip().lower()
    if len(s) == 2 and 'a' <= s[0] <= 'h' and '1' <= s[1] <= '8':
        return (8 - int(s[1]), ord(s[0]) - 97)
    return None


def pos_name(p):
    return chr(97 + p[1]) + str(8 - p[0])


def dirs_of(p):
    if p.isupper():
        return ((1, -1), (1, 1), (-1, -1), (-1, 1))
    return ((1, -1), (1, 1)) if p == 'r' else ((-1, -1), (-1, 1))


def caps_from(b, r, c):
    p = b[r][c]
    out = []
    for dr, dc in dirs_of(p):
        tr, tc = r + 2 * dr, c + 2 * dc
        if 0 <= tr < 8 and 0 <= tc < 8:
            mid = b[r + dr][c + dc]
            if mid != '.' and mid.lower() != p.lower() and b[tr][tc] == '.':
                out.append((tr, tc))
    return out


def moves_from(b, r, c):
    out = []
    for dr, dc in dirs_of(b[r][c]):
        tr, tc = r + dr, c + dc
        if 0 <= tr < 8 and 0 <= tc < 8 and b[tr][tc] == '.':
            out.append((tr, tc))
    return out


def collect(b, pl, cap):
    res = {}
    for r in range(8):
        for c in range(8):
            if b[r][c].lower() == pl:
                m = caps_from(b, r, c) if cap else moves_from(b, r, c)
                if m:
                    res[(r, c)] = m
    return res


def promote(p, tr):
    if p == 'r' and tr == 7:
        return 'R', True
    if p == 'b' and tr == 0:
        return 'B', True
    return p, False


def show(b):
    print('  a b c d e f g h')
    for r in range(8):
        cells = [b[r][c] if b[r][c] != '.' else ('.' if (r + c) % 2 else ' ')
                 for c in range(8)]
        print(str(8 - r) + ' ' + ' '.join(cells))
    print()


def new_board():
    b = [['.'] * 8 for _ in range(8)]
    for r in list(range(3)) + list(range(5, 8)):
        for c in range(8):
            if (r + c) % 2:
                b[r][c] = 'r' if r < 3 else 'b'
    return b


def ask(prompt):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return 'q'


def main():
    b = new_board()
    pl = 'r'
    names = {'r': 'Red', 'b': 'Black'}
    other = {'r': 'b', 'b': 'r'}
    print('Checkers (Draughts) - Red moves first. Captures are mandatory.')
    print('Men move/capture forward only; kings (R/B) move/capture both ways.')
    print('Enter moves as from-to squares, e.g. b6-a5. Type q to quit.')
    while True:
        show(b)
        if not any(b[r][c].lower() == pl for r in range(8) for c in range(8)):
            print(names[other[pl]] + ' wins - ' + names[pl] + ' has no pieces.')
            return
        chain = None
        while True:
            caps = {chain: caps_from(b, *chain)} if chain else collect(b, pl, True)
            must = bool(caps)
            allowed = caps if must else collect(b, pl, False)
            if not allowed:
                print(names[other[pl]] + ' wins - ' + names[pl] + ' has no legal moves.')
                return
            msg = names[pl] + "'s turn"
            if chain:
                msg += ' - keep jumping with ' + pos_name(chain)
            elif must:
                msg += ' - capture is mandatory'
            print(msg)
            line = ask('Move (from-to, e.g. b6-a5): ').strip().lower()
            if line in ('q', 'quit', 'exit'):
                print('Game aborted.')
                return
            parts = [x for x in re.split(r'to|[\s\-]+', line) if x]
            if len(parts) != 2:
                print('Bad input. Use two squares like b6-a5.')
                continue
            frm, to = parse_pos(parts[0]), parse_pos(parts[1])
            if not frm or not to or frm not in allowed or to not in allowed[frm]:
                print('Illegal move' + (' - you must capture.' if must else '.'))
                continue
            fr, fc = frm
            tr, tc = to
            p = b[fr][fc]
            b[fr][fc] = '.'
            if must:
                b[(fr + tr) // 2][(fc + tc) // 2] = '.'
            p, kinged = promote(p, tr)
            b[tr][tc] = p
            if must and not kinged and caps_from(b, tr, tc):
                chain = to
                show(b)
                continue
            break
        pl = other[pl]


if __name__ == '__main__':
    main()