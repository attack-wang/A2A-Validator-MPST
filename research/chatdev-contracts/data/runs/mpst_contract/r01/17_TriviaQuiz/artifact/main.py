"""Trivia quiz entry point.

Usage:
    python main.py                      # built-in bank (questions.py)
    python main.py --bank mybank.json   # custom JSON question bank
    python main.py --shuffle --limit 5 --show-answers
"""

import argparse
import sys

from quiz import Quiz, Question, load_bank
from questions import QUESTION_BANK


def build_parser():
    parser = argparse.ArgumentParser(description="Configurable trivia quiz game.")
    parser.add_argument("--bank", metavar="FILE.json",
                        help="Path to a JSON question bank (list of question objects).")
    parser.add_argument("--shuffle", action="store_true", help="Shuffle question order.")
    parser.add_argument("--limit", type=int, metavar="N",
                        help="Ask only the first N questions.")
    parser.add_argument("--show-answers", action="store_true",
                        help="Display correct answers in the review after the quiz.")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.bank:
            questions = load_bank(args.bank)
        else:
            questions = [Question.from_dict(item) for item in QUESTION_BANK]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("Failed to load question bank: %s" % exc)
        return 1
    if not questions:
        print("Question bank is empty.")
        return 1
    Quiz(questions, shuffle=args.shuffle, limit=args.limit,
         show_answers=args.show_answers).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())