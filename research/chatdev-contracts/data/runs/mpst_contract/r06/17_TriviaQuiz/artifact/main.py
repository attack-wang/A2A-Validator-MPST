"""Trivia Quiz - entry point.

Usage:
    python main.py [--bank FILE] [--show-answers] [--shuffle]
"""
import argparse

from bank import load_bank
from quiz import Quiz


def parse_args():
    p = argparse.ArgumentParser(
        description="Trivia quiz with multiple-choice and short-answer questions."
    )
    p.add_argument("--bank", metavar="FILE",
                   help="Path to a JSON question bank file (uses built-in bank if omitted).")
    p.add_argument("--show-answers", action="store_true",
                   help="Always display correct answers in the post-quiz review.")
    p.add_argument("--shuffle", action="store_true", help="Shuffle question order.")
    return p.parse_args()


def main():
    args = parse_args()
    try:
        questions = load_bank(args.bank)
    except (OSError, ValueError) as exc:
        print(f"Error loading question bank: {exc}")
        return 1
    quiz = Quiz(questions, shuffle=args.shuffle)
    quiz.run()
    print("\n" + quiz.summary())
    show = args.show_answers
    if not show:
        try:
            show = input("Display correct answers? (y/n): ").strip().lower() in ("y", "yes")
        except (EOFError, KeyboardInterrupt):
            show = False
    if show:
        print("\n" + quiz.review())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())