import argparse
import sys

from bank import get_questions
from quiz import Quiz


def main():
    parser = argparse.ArgumentParser(description="Trivia quiz with configurable question banks.")
    parser.add_argument("--bank", metavar="FILE",
                        help="Path to a JSON question bank file (uses built-in bank if omitted).")
    parser.add_argument("--review", action="store_true",
                        help="Always display correct answers after the quiz.")
    parser.add_argument("--shuffle", action="store_true", help="Shuffle question order.")
    args = parser.parse_args()

    try:
        questions = get_questions(args.bank)
    except (OSError, ValueError) as exc:
        sys.exit(f"Error loading question bank: {exc}")

    Quiz(questions, show_review=args.review, shuffle=args.shuffle).run()


if __name__ == "__main__":
    main()