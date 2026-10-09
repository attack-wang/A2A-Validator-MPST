"""Trivia quiz program entry point.

Usage:
    python main.py [--bank FILE] [--topic TOPIC] [--count N]
                   [--shuffle] [--show-answers]
"""
import argparse
import sys

from bank import DEFAULT_BANK, load_bank
from quiz import Quiz


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Trivia quiz with multiple-choice and short-answer questions.")
    parser.add_argument("--bank", metavar="FILE",
                        help="Path to a JSON question bank (default: built-in bank).")
    parser.add_argument("--topic", metavar="TOPIC",
                        help="Only ask questions from this topic.")
    parser.add_argument("--count", type=int, metavar="N",
                        help="Maximum number of questions to ask.")
    parser.add_argument("--shuffle", action="store_true",
                        help="Shuffle the question order.")
    parser.add_argument("--show-answers", action="store_true",
                        help="Display correct answers in a review after the quiz.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        questions = load_bank(args.bank) if args.bank else DEFAULT_BANK
    except (OSError, ValueError) as exc:
        print(f"Error loading question bank: {exc}", file=sys.stderr)
        return 1

    if args.topic:
        wanted = args.topic.strip().lower()
        questions = [q for q in questions
                     if str(q.get("topic", "General")).lower() == wanted]
    if not questions:
        print("No questions match the selected options.", file=sys.stderr)
        return 1
    if args.count and args.count > 0:
        questions = questions[:args.count]

    Quiz(questions, shuffle=args.shuffle, show_answers=args.show_answers).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())