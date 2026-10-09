'''
main.py
Entry point for the ChatDev Trivia Quiz application.
Parses command-line options, loads the configurable question bank
(JSON), and hands control to the Quiz engine.
Usage examples:
    python main.py
    python main.py --bank my_questions.json --shuffle --limit 5
    python main.py --bank questions.json --no-feedback --no-review
'''
import argparse
import random
import sys
from question_bank import QuestionBank
from quiz import Quiz
def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="ChatDev Trivia Quiz - multiple-choice and short-answer quiz game."
    )
    parser.add_argument(
        "-b", "--bank", default="questions.json",
        help="Path to the JSON question bank file (default: questions.json).",
    )
    parser.add_argument(
        "-s", "--shuffle", action="store_true",
        help="Shuffle the question order.",
    )
    parser.add_argument(
        "-n", "--limit", type=int, default=None,
        help="Limit the quiz to the first N questions.",
    )
    parser.add_argument(
        "--no-feedback", action="store_true",
        help="Hide per-question right/wrong feedback until the end.",
    )
    parser.add_argument(
        "--no-review", action="store_true",
        help="Do not display the correct answers after the quiz.",
    )
    return parser.parse_args(argv)
def main(argv=None):
    args = parse_args(argv)
    try:
        bank = QuestionBank.from_json_file(args.bank)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        return 1
    except ValueError as exc:
        print(f"Error: {exc}")
        return 1
    questions = bank.get_questions()
    if args.shuffle:
        random.shuffle(questions)
    if args.limit is not None and args.limit > 0:
        questions = questions[: args.limit]
    if not questions:
        print("Error: the question bank is empty after applying options.")
        return 1
    quiz = Quiz(
        questions,
        immediate_feedback=not args.no_feedback,
        show_answers_at_end=not args.no_review,
    )
    try:
        quiz.run()
    except (EOFError, KeyboardInterrupt):
        print("\nQuiz interrupted. Goodbye!")
    return 0
if __name__ == "__main__":
    sys.exit(main())