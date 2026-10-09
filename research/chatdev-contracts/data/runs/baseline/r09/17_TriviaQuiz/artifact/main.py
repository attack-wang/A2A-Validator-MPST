'''
main.py
Entry point: parses CLI args, loads config and question banks, runs the quiz.
'''
import argparse
import os
import sys
from config import QuizConfig, ConfigError
from question_bank import QuestionBank, QuestionBankError
from quiz import Quiz
def resolve_path(path, base_dir):
    """Return `path` if usable, else resolve it relative to `base_dir`."""
    if os.path.isabs(path) or os.path.exists(path):
        return path
    return os.path.join(base_dir, path)
def parse_args(argv=None):
    """Parse command-line options that override config-file settings."""
    parser = argparse.ArgumentParser(description="Interactive trivia quiz program.")
    parser.add_argument("--config", default="config.json", help="Path to JSON config file.")
    parser.add_argument("--count", type=int, default=None, help="Number of questions (0 = all).")
    parser.add_argument("--topics", nargs="*", default=None, help="Restrict to these topics.")
    parser.add_argument("--shuffle", dest="shuffle", action="store_true", default=None, help="Shuffle question order.")
    parser.add_argument("--no-shuffle", dest="shuffle", action="store_false", help="Keep original question order.")
    parser.add_argument("--show-answers", dest="show_answers", action="store_true", default=None, help="Reveal answers after the quiz.")
    parser.add_argument("--no-answers", dest="show_answers", action="store_false", help="Hide answers after the quiz.")
    return parser.parse_args(argv)
def main():
    """Load config and question banks, then run one quiz session."""
    args = parse_args()
    base_dir = os.path.dirname(os.path.abspath(args.config))
    try:
        cfg = QuizConfig.load(args.config)
    except ConfigError as exc:
        print(f"Configuration error: {exc}")
        return 1
    # Apply command-line overrides (only when explicitly provided).
    if args.count is not None:
        cfg.question_count = args.count
    if args.topics:
        cfg.topics = args.topics
    if args.shuffle is not None:
        cfg.shuffle_questions = args.shuffle
    if args.show_answers is not None:
        cfg.show_correct_answers = args.show_answers
    print(cfg.summary())
    bank = QuestionBank()
    try:
        total = bank.load_files([resolve_path(p, base_dir) for p in cfg.question_bank_files])
    except QuestionBankError as exc:
        print(f"Question bank error: {exc}")
        return 1
    if total == 0:
        print("No questions could be loaded — check your question bank files.")
        return 1
    questions = bank.build_quiz(
        count=cfg.question_count, topics=cfg.topics,
        shuffle_questions=cfg.shuffle_questions, shuffle_choices=cfg.shuffle_choices)
    if not questions:
        print("No questions matched the selected topics.")
        return 1
    quiz = Quiz(questions, show_correct_answers=cfg.show_correct_answers)
    try:
        quiz.run()
        return 0
    except (KeyboardInterrupt, EOFError):
        answered = len(quiz.user_answers)
        print(f"\n\nQuiz ended early. Score so far: {quiz.score}/{answered}")
        return 0
if __name__ == "__main__":
    sys.exit(main())