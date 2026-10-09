'''
main.py
Entry point for the Trivia Quiz application. Parses command-line
arguments, loads a configurable JSON question bank, and starts the
interactive quiz session. Stdout is reconfigured to UTF-8 (with
error replacement) so that Unicode content from question banks can
be displayed safely on any console.
'''
import argparse
import sys
from question_bank import QuestionBank
from quiz_game import QuizGame
DEFAULT_BANK_FILE = "questions.json"
def configure_output():
    """Make stdout/stderr tolerant of Unicode on legacy consoles."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):
                pass
def parse_arguments(argv=None):
    ... (same as before)
def main(argv=None):
    """Application entry point: load the bank and run the quiz."""
    configure_output()
    args = parse_arguments(argv)
    bank = QuestionBank()
    try:
        loaded = bank.load_from_file(args.bank)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error loading question bank: {error}")
        return 1
    if loaded == 0:
        print(f"Error: the question bank '{args.bank}' contains no questions.")
        return 1
    if args.list_topics:
        print(f"Topics in '{bank.name}':")
        for topic in bank.get_topics():
            print(f"  - {topic} ({bank.get_question_count(topic)} questions)")
        return 0
    if args.topic and bank.get_question_count(args.topic) == 0:
        print(f"Error: no questions found for topic '{args.topic}'.")
        print("Available topics:")
        for topic in bank.get_topics():
            print(f"  - {topic}")
        return 1
    questions = bank.get_questions(topic=args.topic,
                                   count=args.num_questions,
                                   shuffle=args.shuffle)
    game = QuizGame(bank, show_answers_after=args.show_answers)
    game.start(questions)
    return 0
if __name__ == "__main__":
    sys.exit(main())