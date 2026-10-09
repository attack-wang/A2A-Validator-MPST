import random
from datetime import date

GREEN, YELLOW, GREY = "\033[92m", "\033[93m", "\033[90m"
RESET, BOLD, DIM = "\033[0m", "\033[1m", "\033[2m"
LEN, MAX_TRIES = 5, 6

ANSWERS = ("crane slate audio house plant brave light world ocean tiger cloud smile grape lemon "
           "mango peach berry melon onion salad pizza bread toast juice water earth storm frost "
           "beach coast shore cliff ridge ghost snake eagle shark whale zebra panda koala otter "
           "goose heron robin raven mouse horse sheep camel llama moose bison gecko snail chair "
           "table couch shelf clock phone screen cable dream sleep night comet orbit space alien "
           "rocket planet galaxy cosmic nebula meteor pluto lunar solar sunny windy rainy foggy "
           "misty humid happy jolly merry funny silly witty smart loyal honest noble royal music "
           "piano drums flute cello opera choir sport soccer tennis hockey rugby chess poker bingo "
           "token score match round final start begin money coins funds price value worth cheap "
           "trade store fruit olive bloom petal grass spice sugar honey sweet spicy tangy tasty "
           "yummy fresh stale").split()
VALID = set(ANSWERS)


def daily_word():
    return random.Random(date.today().isoformat()).choice(ANSWERS)


def feedback(guess, answer):
    marks = [GREY] * LEN
    left = {}
    for i, ch in enumerate(answer):
        if guess[i] == ch:
            marks[i] = GREEN
        else:
            left[ch] = left.get(ch, 0) + 1
    for i, ch in enumerate(guess):
        if marks[i] == GREEN:
            continue
        if left.get(ch, 0) > 0:
            marks[i] = YELLOW
            left[ch] -= 1
    return marks


def render(guess, marks):
    return " ".join(m + c + RESET for m, c in zip(marks, guess.upper()))


def print_board(board):
    print()
    for g, m in board:
        print("  " + render(g, m))
    for _ in range(MAX_TRIES - len(board)):
        print("  " + DIM + "_ _ _ _ _" + RESET)
    print()


def play(custom=None):
    answer = (custom or daily_word()).lower()
    if len(answer) != LEN or not answer.isalpha():
        print("Custom word must be exactly 5 letters.")
        return
    print(BOLD + "WORDLE" + RESET + " - guess the 5-letter word in " + str(MAX_TRIES) + " tries.")
    print(DIM + "green=right spot  yellow=wrong spot  grey=not in word" + RESET)
    board = []
    for turn in range(1, MAX_TRIES + 1):
        print_board(board)
        while True:
            try:
                guess = input("Turn " + str(turn) + "/" + str(MAX_TRIES) + " > ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nBye! The word was " + answer.upper() + ".")
                return
            if len(guess) == LEN and guess.isalpha() and guess in VALID:
                break
            print("Invalid guess: enter a 5-letter English word from the word list.")
        marks = feedback(guess, answer)
        board.append((guess, marks))
        if guess == answer:
            print_board(board)
            print(BOLD + GREEN + "You won in " + str(turn) + "/" + str(MAX_TRIES) +
                  "! The word was " + answer.upper() + "." + RESET)
            return
    print_board(board)
    print(BOLD + GREY + "You lost. The word was " + answer.upper() + "." + RESET)


if __name__ == "__main__":
    play()