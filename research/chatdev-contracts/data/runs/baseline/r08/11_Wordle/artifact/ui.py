def print_welcome():
    print(BANNER)
def print_instructions():
    print("Guess the " + colorize("5-letter", BOLD) + " word in " + colorize("6 tries", BOLD) + ".")
    print("After each guess, the letters change color to show how close you were:")
    print("  " + colorize("GREEN", GREEN) + "  = correct letter in the correct position")
    print("  " + colorize("YELLOW", YELLOW) + " = correct letter in the wrong position")
    print("  " + colorize("GREY", GREY) + "   = letter not in the word at all")
    print()
def print_board(game):
    print(colorize("=" * 32, BOLD))
    for guess, colors in zip(game.guesses, game.feedbacks):
        print("  " + render_guess(guess, colors))
    for _ in range(game.attempts_remaining()):
        print("  " + " ".join("_" for _ in range(game.WORD_LENGTH)))
    print(colorize("=" * 32, BOLD))
    print_keyboard(game)
    print()
def letter_statuses(game):
    status = {}
    priority = {GREY: 1, YELLOW: 2, GREEN: 3}
    for guess, colors in zip(game.guesses, game.feedbacks):
        for letter, color in zip(guess, colors):
            if priority[color] > priority.get(status.get(letter, GREY), 0):
                status[letter] = color
    return status
def print_keyboard(game):
    statuses = letter_statuses(game)
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    for row in rows:
        cells = []
        for letter in row:
            color = statuses.get(letter, RESET)
            cells.append(colorize(letter.upper(), color) if color != RESET else letter.upper())
        print("   " + " ".join(cells))