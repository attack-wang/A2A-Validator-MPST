"""Trivia quiz program: multiple-choice and short-answer questions with scoring."""

import argparse
import random
import sys

from question_bank import DEFAULT_QUESTIONS, load_bank, parse_bank
from quiz import Quiz


def build_parser():
    parser = argparse.ArgumentParser(description="Trivia quiz game")
    parser.add_argument("--bank", metavar="FILE",
                        help="Path to a JSON question bank file (defaults to built-in bank)")
    parser.add_argument("--show-answers", action="store_true",
                        help="Display correct answers after the quiz")
    parser.add_argument("--shuffle", action="store_true",
                        help="Shuffle the question order")
    parser.add_argument("--limit", type=int, metavar="N",
                        help="Ask at most N questions")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        questions = load_bank(args.bank) if args.bank else parse_bank(DEFAULT_QUESTIONS)
    except (OSError, ValueError) as exc:
        print(f"Error loading question bank: {exc}", file=sys.stderr)
        return 1
    if args.shuffle:
        random.shuffle(questions)
    if args.limit is not None:
        questions = questions[: max(args.limit, 0)]
    if not questions:
        print("Error: no questions to ask.", file=sys.stderr)
        return 1
    Quiz(questions, show_answers=args.show_answers).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())