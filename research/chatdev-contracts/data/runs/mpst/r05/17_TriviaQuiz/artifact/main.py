'''
main.py
Entry point for the trivia quiz program. Parses command-line options,
loads a JSON question bank, and starts the interactive quiz session.
Usage:
    python main.py sample_questions.json
    python main.py sample_questions.json --topic Science --shuffle --limit 5 --show-answers
'''
import argparse
import sys
from question_bank import QuestionBank
from quiz import Quiz
def parse_args(argv=None):
    """Parse command-line arguments for the quiz."""
    parser = argparse.ArgumentParser(
        description="Run an interactive trivia quiz from a JSON question bank."
    )
    parser.add_argument(
        "bank",
        help="Path to the JSON question-bank file.",
    )
    parser.add_argument(
        "--topic",
        default=None,
        help="Only ask questions from this topic.",
    )
    parser.add_argument(
        "--shuffle",
        action="store_true",
        help="Shuffle the question order.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Ask at most N questions.",
    )
    parser.add_argument(
        "--show-answers",
        action="store_true",
        help="Display the correct answers after the quiz.",
    )
    return parser.parse_args(argv)
def main(argv=None):
    """Load the question bank and run the interactive quiz."""
    args = parse_args(argv)
    try:
        bank = QuestionBank.from_json(args.bank)
        questions = bank.select(
            topic=args.topic, shuffle=args.shuffle, limit=args.limit
        )
        if not questions:
            if args.topic:
                print(
                    f"No questions found for topic {args.topic!r}.",
                    file=sys.stderr,
                )
            else:
                print("The question bank contains no questions.", file=sys.stderr)
            return 1
        quiz = Quiz(
            bank,
            questions=questions,
            show_answers_after=args.show_answers,
        )
        quiz.run()
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0
if __name__ == "__main__":
    sys.exit(main())