"""Trivia Quiz Program - entry point.

Usage:
    python main.py [--bank path/to/bank.json] [--shuffle] [--show-answers]
"""
import argparse
import sys

from question_bank import get_questions
from quiz import Quiz


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Trivia quiz with scoring and an optional answer review.")
    parser.add_argument("--bank", default=None,
                        help="Path to a JSON question bank (a list of question "
                             "objects). Omit to use the built-in default bank.")
    parser.add_argument("--shuffle", action="store_true",
                        help="Shuffle the question order.")
    parser.add_argument("--show-answers", action="store_true",
                        help="Display correct answers after the quiz.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        questions = get_questions(args.bank)
    except (OSError, ValueError, KeyError) as exc:
        print(f"Failed to load question bank: {exc}")
        return 1
    if not questions:
        print("Question bank is empty.")
        return 1

    quiz = Quiz(questions, shuffle=args.shuffle)
    quiz.run()
    quiz.report(show_answers=args.show_answers)
    return 0


if __name__ == "__main__":
    sys.exit(main())