"""Trivia quiz program entry point.

Usage:
    python main.py                       # built-in question bank
    python main.py --bank my_bank.json   # custom JSON question bank
    python main.py --shuffle             # randomize question order
    python main.py --show-answers        # display correct answers after the quiz
"""

import argparse
import sys

from question_bank import load_bank
from quiz import Question, Quiz


def build_parser():
    parser = argparse.ArgumentParser(description="Interactive trivia quiz with scoring.")
    parser.add_argument("--bank", metavar="FILE",
                        help="path to a JSON question bank (defaults to the built-in bank)")
    parser.add_argument("--shuffle", action="store_true",
                        help="shuffle question order")
    parser.add_argument("--show-answers", action="store_true",
                        help="display correct answers after the quiz")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        raw_bank = load_bank(args.bank)
    except (OSError, ValueError) as exc:
        print("Error loading question bank: %s" % exc)
        return 1
    try:
        questions = [Question.from_dict(entry) for entry in raw_bank]
    except (KeyError, ValueError) as exc:
        print("Error in question bank data: %s" % exc)
        return 1
    if not questions:
        print("The question bank is empty; nothing to quiz.")
        return 1
    quiz = Quiz(questions, shuffle=args.shuffle)
    try:
        quiz.run()
    finally:
        if args.show_answers:
            quiz.review()
    return 0


if __name__ == "__main__":
    sys.exit(main())