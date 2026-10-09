'''
main.py
Command-line entry point for the trivia quiz program.
Loads a configurable JSON question bank, applies user-selected filters
(topic, question count, shuffling) and starts the QuizGame session.
'''
import argparse
import json
import sys
from question_bank import QuestionBank
from quiz_game import QuizGame
def build_arg_parser():
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Trivia quiz program with configurable JSON question banks."
    )
    parser.add_argument("--bank", default="questions.json",
                        help="Path to a JSON question bank (default: questions.json)")
    parser.add_argument("--topic",
                        help="Only ask questions of this topic")
    parser.add_argument("--num-questions", type=int, dest="num_questions",
                        help="Limit the number of questions asked")
    parser.add_argument("--shuffle", action="store_true",
                        help="Shuffle the question order")
    parser.add_argument("--shuffle-options", action="store_true", dest="shuffle_options",
                        help="Shuffle multiple-choice options")
    parser.add_argument("--hide-answers", action="store_true", dest="hide_answers",
                        help="Do not display correct answers after the quiz")
    parser.add_argument("--list-topics", action="store_true", dest="list_topics",
                        help="List the topics in the bank and exit")
    return parser
def main(argv=None):
    """Parse arguments, load the bank and run one quiz session."""
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        bank = QuestionBank.load_from_json(args.bank)
    except FileNotFoundError:
        print(f"Error: question bank file not found: '{args.bank}'")
        print("Tip: pass a different bank with --bank, e.g. --bank science_questions.json")
        return 1
    except json.JSONDecodeError as exc:
        print(f"Error: '{args.bank}' is not valid JSON: {exc}")
        return 1
    except ValueError as exc:
        print(f"Error: invalid question bank '{args.bank}': {exc}")
        return 1
    if args.list_topics:
        print(f"Question bank '{bank.name}' contains the following topics:")
        for topic in bank.topics():
            print(f"  - {topic}")
        return 0
    questions = bank.questions
    if args.topic:
        filtered = bank.filter_by_topic(args.topic)
        if not filtered:
            print(f"No questions found for topic '{args.topic}'.")
            print(f"Available topics: {', '.join(bank.topics())}")
            return 1
        questions = filtered
    if args.num_questions is not None:
        if args.num_questions <= 0:
            print("Error: --num-questions must be a positive integer.")
            return 1
        questions = questions[:args.num_questions]
        if not questions:
            print("Error: no questions available after applying your filters.")
            return 1
    game_bank = QuestionBank(name=bank.name, questions=questions)
    game = QuizGame(
        game_bank,
        shuffle_questions=args.shuffle,
        shuffle_options=args.shuffle_options,
        show_answers=not args.hide_answers,
    )
    try:
        game.run()
    except KeyboardInterrupt:
        print("\nQuiz interrupted. Goodbye!")
        return 130
    return 0
if __name__ == "__main__":
    sys.exit(main())