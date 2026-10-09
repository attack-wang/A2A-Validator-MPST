'''
main.py
Entry point for the trivia quiz program.
Parses command-line arguments, discovers question banks, runs the
interactive menu/quiz loop and shows results plus the optional review.
'''
import argparse
import sys
from question_bank import discover_banks
from quiz import Quiz
DEFAULT_BANK_DIR = "question_banks"
def parse_args(argv):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Trivia quiz program")
    parser.add_argument(
        "-d", "--bank-dir", default=DEFAULT_BANK_DIR,
        help="Directory containing JSON question banks (default: %(default)s)")
    parser.add_argument(
        "-b", "--bank",
        help="Name of the question bank to use (skips the bank menu)")
    parser.add_argument(
        "-s", "--shuffle", action="store_true",
        help="Shuffle the question order")
    parser.add_argument(
        "-a", "--show-answers", action="store_true",
        help="Always show correct answers after the quiz")
    return parser.parse_args(argv)
def choose_bank(banks, input_func=input, output_func=print):
    """Interactively let the user pick one of the available question banks."""
    if not banks:
        return None
    if len(banks) == 1:
        return banks[0]
    output_func("\nAvailable question banks:")
    for i, bank in enumerate(banks, 1):
        output_func("  %d. %s (%d questions)" % (i, bank.name, len(bank)))
    while True:
        choice = input_func("Select a question bank (1-%d): " % len(banks))
        text = str(choice).strip()
        if text.isdigit():
            index = int(text) - 1
            if 0 <= index < len(banks):
                return banks[index]
        output_func("Please enter a number between 1 and %d." % len(banks))
def find_bank_by_name(banks, name):
    """Return the bank whose name matches `name` (case-insensitive), else None."""
    wanted = str(name).strip().lower()
    for bank in banks:
        if bank.name.lower() == wanted:
            return bank
    return None
def ask_yes_no(prompt, input_func=input, output_func=print):
    """Ask a yes/no question; return True for yes and False for no."""
    while True:
        answer = input_func("%s (y/n): " % prompt)
        text = str(answer).strip().lower()
        if text in ("y", "yes"):
            return True
        if text in ("n", "no"):
            return False
        output_func("Please answer 'y' or 'n'.")
def run_quiz(bank, args):
    """Run one quiz session against `bank`, then show results and review."""
    quiz = Quiz(bank, shuffle=args.shuffle)
    quiz.run()
    quiz.display_results()
    if args.show_answers or ask_yes_no("\nShow the correct answers?"):
        quiz.display_review()
def main(argv=None):
    """Program entry point; returns a process exit code."""
    args = parse_args(argv)
    banks = discover_banks(args.bank_dir)
    if not banks:
        print("No question banks found in %r." % args.bank_dir, file=sys.stderr)
        print("Add JSON question bank files there (see README.md).", file=sys.stderr)
        return 1
    if args.bank:
        bank = find_bank_by_name(banks, args.bank)
        if bank is None:
            print("Question bank %r not found. Available banks:" % args.bank,
                  file=sys.stderr)
            for candidate in banks:
                print("  - %s" % candidate.name, file=sys.stderr)
            return 1
        while True:
            run_quiz(bank, args)
            if not ask_yes_no("\nPlay again with this question bank?"):
                break
    else:
        while True:
            bank = choose_bank(banks)
            if bank is None:
                break
            while True:
                run_quiz(bank, args)
                if not ask_yes_no("\nPlay again with this question bank?"):
                    break
            if not ask_yes_no("Return to the question bank menu?"):
                break
    print("Thanks for playing!")
    return 0
if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        print("\nThanks for playing!")
        sys.exit(0)