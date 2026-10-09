'''
main.py
Entry point for the Trivia Quiz application.
Usage examples:
    python main.py
    python main.py --bank my_questions.json
    python main.py --topics Science,History --count 5
    python main.py --show-answers
    python main.py --hide-answers
Fixes applied in this revision:
    - Shipped a valid questions.json (the previous file contained a literal
      "..." placeholder, which made json.load fail on startup).
    - Ctrl+C / Ctrl+D during the quiz no longer print a traceback.
    - --show-answers / --hide-answers are mutually exclusive; when neither
      is given the user is asked after the quiz whether to review answers.
    - Multiple-choice answers may be given as a zero-based index in JSON.
    - Removed unused import and replaced non-ASCII symbols with ASCII-safe
      text so the program runs on Windows cp1252 consoles.
'''
import argparse
import sys
from question_bank import QuestionBank, QuestionBankError
from quiz import QuizGame
def positive_int(value):
    """Argparse type: reject non-positive --count values."""
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid int value: '{value}'")
    if number <= 0:
        raise argparse.ArgumentTypeError(
            f"count must be a positive integer, got {value}"
        )
    return number
def parse_arguments(argv=None):
    parser = argparse.ArgumentParser(
        description="An interactive trivia quiz with configurable question banks."
    )
    parser.add_argument(
        "--bank", default="questions.json",
        help="Path to the JSON question bank file (default: questions.json)"
    )
    parser.add_argument(
        "--topics", default=None,
        help="Comma-separated list of topics to include (default: all topics)"
    )
    parser.add_argument(
        "--count", type=positive_int, default=None,
        help="Number of questions to ask (default: all matching questions)"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--show-answers", action="store_true",
        help="Always display correct answers after the quiz"
    )
    group.add_argument(
        "--hide-answers", action="store_true",
        help="Never display correct answers after the quiz"
    )
    parser.add_argument(
        "--no-shuffle", action="store_true",
        help="Ask questions in bank order instead of shuffled order"
    )
    return parser.parse_args(argv)
def main(argv=None):
    args = parse_arguments(argv)
    # Load the question bank.
    try:
        bank = QuestionBank.load_from_json(args.bank)
    except QuestionBankError as exc:
        print(f"Error loading question bank: {exc}")
        return 1
    if len(bank) == 0:
        print(f"Error: the question bank '{args.bank}' contains no questions.")
        return 1
    topics = [t.strip() for t in args.topics.split(",")] if args.topics else None
    if topics:
        available = bank.get_topics()
        unknown = [t for t in topics if t.lower() not in {a.lower() for a in available}]
        if unknown:
            print(f"Warning: unknown topic(s) {', '.join(unknown)}.")
            print(f"Available topics: {', '.join(available)}")
    questions = bank.get_questions(
        topics=topics, count=args.count, shuffle=not args.no_shuffle
    )
    if not questions:
        print("Error: no questions matched the selected topic(s).")
        return 1
    # Three-state answer review option:
    #   True  -> always show the review (--show-answers)
    #   False -> never show the review (--hide-answers)
    #   None  -> ask the user after the quiz
    if args.show_answers:
        show_answers = True
    elif args.hide_answers:
        show_answers = False
    else:
        show_answers = None
    game = QuizGame(questions, show_answers_after=show_answers)
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\nQuiz interrupted. No score recorded. Goodbye!")
        return 1
    game.display_results()
    return 0
if __name__ == "__main__":
    sys.exit(main())