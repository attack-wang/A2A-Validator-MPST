"""Trivia quiz entry point: run the quiz, track score, optionally review answers."""

import argparse
import sys

from question_bank import load_bank
from quiz import Quiz


def build_parser():
    parser = argparse.ArgumentParser(
        description="Trivia quiz with multiple-choice and short-answer questions.")
    parser.add_argument("--bank", metavar="FILE",
                        help="Path to a JSON question bank (a list of question objects "
                             "or {'questions': [...]}); omit to use the built-in bank")
    parser.add_argument("--shuffle", action="store_true",
                        help="Shuffle the question order")
    parser.add_argument("--show-answers", action="store_true",
                        help="Display correct answers after the quiz")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        questions = load_bank(args.bank)
    except (OSError, ValueError) as exc:
        print(f"Error loading question bank: {exc}", file=sys.stderr)
        return 1
    if not questions:
        print("The question bank is empty.", file=sys.stderr)
        return 1
    quiz = Quiz(questions, shuffle=args.shuffle)
    try:
        quiz.run()
    except (EOFError, KeyboardInterrupt):
        print("\nQuiz interrupted.")
    print(quiz.summary())
    if args.show_answers:
        quiz.review()
    return 0


if __name__ == "__main__":
    sys.exit(main())