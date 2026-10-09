"""Trivia quiz entry point. Supports custom JSON question banks and answer review."""
import argparse

from question_bank import DEFAULT_QUESTIONS
from quiz import Quiz, load_bank, questions_from_dicts


def build_parser():
    parser = argparse.ArgumentParser(description="Trivia quiz program")
    parser.add_argument("-b", "--bank", help="Path to a JSON question bank file")
    parser.add_argument("-s", "--shuffle", action="store_true", help="Shuffle question order")
    parser.add_argument("-r", "--reveal", action="store_true",
                        help="Always show correct answers after the quiz")
    return parser


def load_questions(bank_path):
    if bank_path:
        return load_bank(bank_path)
    return questions_from_dicts(DEFAULT_QUESTIONS)


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        questions = load_questions(args.bank)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Failed to load question bank: {exc}")
        return 1
    if not questions:
        print("The question bank is empty.")
        return 1

    print(f"Trivia Quiz - {len(questions)} questions loaded."
          + (" (shuffled)" if args.shuffle else ""))
    quiz = Quiz(questions, shuffle=args.shuffle)
    try:
        correct, total = quiz.run()
    except (EOFError, KeyboardInterrupt):
        print("\nQuiz interrupted.")
        correct, total = quiz.score()

    if total:
        percent = 100.0 * correct / total
        print(f"\nFinal score: {correct} out of {total} correct ({percent:.0f}%).")

    reveal = args.reveal
    if not reveal and total:
        try:
            answer = input("Show correct answers after the quiz? [y/N]: ")
        except (EOFError, KeyboardInterrupt):
            answer = ""
        reveal = answer.strip().lower() in ("y", "yes")
    if reveal:
        quiz.review()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())