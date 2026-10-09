def parse_args(argv): argparse with --random, --no-color, --stats, --word (hidden? maybe not), --help
def print_banner(colors)
def print_instructions(colors)
def get_guess(game, colors) -> validated input loop:
    prompt "Enter guess #n: "
    strip, upper
    if len != 5 -> "Please enter exactly 5 letters."
    if not alpha -> "Only letters A-Z."
    if not is_valid_guess -> "Not in word list."
    return guess
def main():
    args
    colors = supports_color() and not args.no_color
    if args.stats: print summary; return
    answer = get_random_word() if args.random else get_daily_word()
    game = WordleGame(answer)
    banner + instructions
    while not game.is_finished():
        show board? show prompt
        guess = get_guess(...)
        states = game.submit_guess(guess)
        print board + keyboard
        if game.is_won: win message; stats record; break
    if not game.is_won: reveal answer
    print summary stats
    return 0/1 exit code? 0 always fine.
if __name__ == "__main__": sys.exit(main())