#!/usr/bin/env python3
"""Mastermind - crack the hidden color code."""

import random
import sys

COLORS = ['R', 'G', 'B', 'Y', 'O', 'P']
COLOR_NAMES = {'R': 'Red', 'G': 'Green', 'B': 'Blue',
               'Y': 'Yellow', 'O': 'Orange', 'P': 'Purple'}
CODE_LENGTH = 4
MAX_TRIES = 10


def generate_code():
    """Random secret code; repeats allowed."""
    return [random.choice(COLORS) for _ in range(CODE_LENGTH)]


def evaluate_guess(code, guess):
    """Return (exact, partial): exact = right color & position,
    partial = right color, wrong position."""
    exact = sum(1 for c, g in zip(code, guess) if c == g)
    code_left, guess_left = {}, {}
    for c, g in zip(code, guess):
        if c != g:
            code_left[c] = code_left.get(c, 0) + 1
            guess_left[g] = guess_left.get(g, 0) + 1
    partial = sum(min(n, guess_left.get(col, 0)) for col, n in code_left.items())
    return exact, partial


def parse_guess(text):
    """'r g b y' -> ['R','G','B','Y'], or None if invalid."""
    text = text.strip().upper().replace(' ', '').replace(',', '')
    if len(text) != CODE_LENGTH or any(ch not in COLORS for ch in text):
        return None
    return list(text)


def render_pegs(exact, partial):
    pegs = '*' * exact + 'o' * partial
    return pegs + '.' * (CODE_LENGTH - len(pegs))


def print_rules():
    print('=' * 50)
    print('             MASTERMIND - Crack the Code!')
    print('=' * 50)
    print('Colors: ' + ', '.join('{}={}'.format(c, COLOR_NAMES[c]) for c in COLORS))
    print('The computer hides a code of {} colors (repeats allowed).'.format(CODE_LENGTH))
    print('You get {} tries. Type {} letters, e.g. RGBY.'.format(MAX_TRIES, CODE_LENGTH))
    print('Feedback per guess: * = exact (right color & spot),')
    print('                    o = partial (right color, wrong spot).')
    print("Type 'quit' to give up. Good luck!")
    print('-' * 50)


def play():
    secret = generate_code()
    history = []
    print_rules()
    for attempt in range(1, MAX_TRIES + 1):
        while True:
            raw = input('Try {}/{} - guess: '.format(attempt, MAX_TRIES)).strip()
            if raw.lower() in ('quit', 'exit', 'q'):
                print('You gave up. The code was: ' + ' '.join(secret))
                return
            guess = parse_guess(raw)
            if guess is None:
                print('  Invalid! Enter exactly {} letters from {}.'.format(
                    CODE_LENGTH, ''.join(COLORS)))
                continue
            break
        exact, partial = evaluate_guess(secret, guess)
        history.append((attempt, guess, exact, partial))
        print('  Attempts so far:')
        for n, g, e, p in history:
            print('   #{}: {}   {}   (exact:{}, partial:{})'.format(
                n, ' '.join(g), render_pegs(e, p), e, p))
        if exact == CODE_LENGTH:
            print('\n*** YOU WIN! *** Cracked the code in {} tries: {}'.format(
                attempt, ' '.join(secret)))
            return
        print()
    print('\n*** YOU LOSE *** - out of {} tries!'.format(MAX_TRIES))
    print('The secret code was: ' + ' '.join(secret))


def main():
    while True:
        play()
        again = input('\nPlay again? (y/n): ').strip().lower()
        if again not in ('y', 'yes'):
            print('Thanks for playing Mastermind. Goodbye!')
            break


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\nGame aborted. Goodbye!')
        sys.exit(0)