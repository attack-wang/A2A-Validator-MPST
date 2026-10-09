'''
main.py
Entry point for the Trivia Quiz program.
Usage examples:
    python main.py
    python main.py --bank my_questions.json
    python main.py --bank geography.json --topic Geography --shuffle --show-answers
    python main.py --bank science.json --feedback
'''
import argparse
import os
import sys
from question_bank import QuestionBank
from quiz import Quiz
DEFAULT_BANK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "questions.json")
def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Trivia Quiz - answer multiple-choice and short-answer questions and track your score."
    )
    parser.add_argument(
        "--bank", "-b",
        default=DEFAULT_BANK,
        help=f"Path to a JSON question bank file (default: {DEFAULT_BANK}).",
    )
    parser.add_argument(
        "--topic", "-t",
        default=None,
        help="Only ask questions from this topic (case-insensitive).",
    )
    parser.add_argument(
        "--shuffle", "-s",
        action="store_true",
        help="Randomize the question order.",
    )
    parser.add_argument(
        "--show-answers", "-a",
        action="store_true",
        help="Show a full answer review after the quiz.",
    )
    parser.add_argument(
        "--feedback", "-f",
        action="store_true",
        help="Show immediate right/wrong feedback after each answer.",
    )
    return parser.parse_args(argv)
def main(argv=None):
    args = parse_args(argv)
    bank = QuestionBank(args.bank)
    try:
        bank.load()
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error loading question bank:\n{exc}", file=sys.stderr)
        return 1
    if args.topic:
        try:
            bank.filter_by_topic(args.topic)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
    if args.shuffle:
        bank.shuffle()
    quiz = Quiz(bank, show_answers_after=args.show_answers, immediate_feedback=args.feedback)
    quiz.run()
    return 0
if __name__ == "__main__":
    sys.exit(main())