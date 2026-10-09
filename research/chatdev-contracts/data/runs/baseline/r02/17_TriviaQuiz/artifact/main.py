'''
main.py
Entry point for the trivia quiz program.
Loads a question bank, configures the quiz (via command-line options
and/or interactive prompts) and runs the QuizGame.
Fixes applied:
  1. Defined the previously missing main() function (root cause of the
     NameError: name 'main' is not defined crash).
  2. Added the missing "import sys" so sys.exit(0) in the KeyboardInterrupt
     handler works correctly.
  3. Restored the interactive configuration helpers (_prompt_yes_no,
     _prompt_nonempty, _prompt_int) and command-line parsing (parse_args)
     that were fragmented out of the original file.
'''
import argparse
import os
import sys
from question_bank import QuestionBank
from quiz_game import QuizGame
def _prompt_yes_no(prompt, default=False):
    """Ask a yes/no question; empty input returns the default."""
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        raw = input(prompt + suffix).strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw == "":
            return default
        if raw in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")
def _prompt_nonempty(prompt, default=None):
    """Prompt until a non-empty string is entered (or default is used)."""
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        if default is not None:
            return default
        print("Input cannot be empty.")
def _prompt_int(prompt, default):
    """Prompt for a positive integer, falling back to default on bad input."""
    raw = input(prompt).strip()
    if not raw:
        return default
    try:
        value = int(raw)
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        print(f"Invalid number '{raw}', using default ({default}).")
        return default
def parse_args(argv=None):
    """Parse command-line options (all optional)."""
    parser = argparse.ArgumentParser(
        description="Interactive trivia quiz with configurable question banks.")
    parser.add_argument("-f", "--file", default=None,
                        help="Path to a JSON question bank (default: questions.json)")
    parser.add_argument("-t", "--topic", default=None,
                        help="Only ask questions of this topic")
    parser.add_argument("-n", "--num", type=int, default=None,
                        help="Maximum number of questions to ask")
    parser.add_argument("--shuffle", action="store_true",
                        help="Shuffle question order")
    parser.add_argument("--shuffle-choices", action="store_true",
                        help="Shuffle multiple-choice option order at runtime")
    parser.add_argument("--show-answers", action="store_true",
                        help="Show the answer review automatically at the end")
    return parser.parse_args(argv)
def main():
    """Load the question bank, configure the quiz and run the game."""
    args = parse_args()
    # ---- Question bank file ------------------------------------------
    filepath = args.file or _prompt_nonempty(
        "Question bank file (blank for questions.json): ",
        default="questions.json")
    if not os.path.exists(filepath):
        print(f"Error: question bank file not found: '{filepath}'")
        sys.exit(1)
    print(f"Loading question bank from '{filepath}' ...")
    try:
        bank = QuestionBank.from_json(filepath)
    except (ValueError, OSError) as exc:
        print(f"Error loading question bank: {exc}")
        sys.exit(1)
    if len(bank) == 0:
        print("Error: the question bank is empty.")
        sys.exit(1)
    # ---- Interactive configuration for options not given -------------
    topic = args.topic
    if topic is None:
        print(f"Available topics: {', '.join(bank.get_topics())}")
        topic = input("Topic to practice (blank for all): ").strip() or None
    count = args.num
    if count is None:
        count = _prompt_int(
            f"Number of questions (1-{len(bank)}, blank for all): ",
            default=len(bank))
    shuffle = args.shuffle or _prompt_yes_no("Shuffle question order?")
    shuffle_choices = args.shuffle_choices or _prompt_yes_no(
        "Shuffle multiple-choice options?")
    show_answers = args.show_answers or _prompt_yes_no(
        "Show correct answers after the quiz?")
    # ---- Build and run the quiz ---------------------------------------
    questions = bank.get_questions(topic=topic, count=count, shuffle=shuffle)
    if not questions:
        print(f"Error: no questions found for topic '{topic}'.")
        sys.exit(1)
    game = QuizGame(questions, shuffle_choices=shuffle_choices)
    game.start(show_answers_after=show_answers)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted. Goodbye!")
        sys.exit(0)