'''
config.py
Configuration handling for the trivia quiz application.
Defines:
- QuizConfig: holds all runtime settings for a quiz session.
- parse_arguments: builds the CLI parser and returns a QuizConfig.
Settings:
- bank_path: path to the JSON question bank file.
- shuffle: whether to shuffle question order.
- show_answers: whether to automatically display correct answers after the quiz.
'''
import argparse
class QuizConfig:
    """Container for runtime configuration of a quiz session."""
    DEFAULT_BANK_PATH = "question_bank.json"
    def __init__(self, bank_path=DEFAULT_BANK_PATH, shuffle=False, show_answers=False):
        self.bank_path = bank_path
        self.shuffle = shuffle
        self.show_answers = show_answers
def parse_arguments(argv=None):
    """Parse command-line arguments and return a QuizConfig instance."""
    parser = argparse.ArgumentParser(
        prog="trivia_quiz",
        description="A configurable trivia quiz with multiple-choice and "
                    "short-answer questions.",
    )
    parser.add_argument(
        "-b", "--bank",
        default=QuizConfig.DEFAULT_BANK_PATH,
        help="Path to the JSON question bank file (default: %(default)s)",
    )
    parser.add_argument(
        "-s", "--shuffle",
        action="store_true",
        help="Shuffle the order of questions before starting.",
    )
    parser.add_argument(
        "-a", "--show-answers",
        dest="show_answers",
        action="store_true",
        help="Automatically display the correct answers after the quiz "
             "finishes (otherwise you will be asked).",
    )
    args = parser.parse_args(argv)
    return QuizConfig(
        bank_path=args.bank,
        shuffle=args.shuffle,
        show_answers=args.show_answers,
    )