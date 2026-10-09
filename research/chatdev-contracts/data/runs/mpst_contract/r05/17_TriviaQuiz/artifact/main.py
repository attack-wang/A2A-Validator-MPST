import argparse
import random
import sys

from quiz import Quiz, load_bank, questions_from_dicts
from question_banks import DEFAULT_QUESTIONS


def parse_args():
    parser = argparse.ArgumentParser(description="Trivia quiz with configurable question banks.")
    parser.add_argument("--bank", help="Path to a JSON question bank file (defaults to the built-in bank).")
    parser.add_argument("--count", type=int, help="Number of questions to ask.")
    parser.add_argument("--shuffle", action="store_true", help="Shuffle question order.")
    parser.add_argument("--show-answers", action="store_true", help="Show correct answers after the quiz.")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.bank:
        try:
            questions = load_bank(args.bank)
        except (OSError, ValueError, KeyError) as exc:
            sys.exit(f"Could not load question bank '{args.bank}': {exc}")
    else:
        questions = questions_from_dicts(DEFAULT_QUESTIONS)
    if args.shuffle:
        random.shuffle(questions)
    if args.count is not None:
        questions = questions[: max(0, args.count)]
    Quiz(questions, show_answers=args.show_answers).run()


if __name__ == "__main__":
    main()