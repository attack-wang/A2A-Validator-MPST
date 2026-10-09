'''
main.py
Command-line entry point for the trivia quiz program.
Parses command-line options, discovers/loads a JSON question bank, builds a
QuizConfig and runs a QuizSession.  Supported options include:
  --bank PATH        load a specific bank file
  --bank-dir DIR     directory to scan for bank files (default: banks)
  --list-banks       list available banks and exit
  --topics ...       restrict the quiz to the given topic(s)
  --num N            limit the number of questions
  --no-shuffle       keep the original question order
  --shuffle-choices  randomise the order of multiple-choice options
  --show-answers / --hide-answers   review correct answers after the quiz
  --immediate-feedback              reveal correctness after each answer
  --seed N           deterministic shuffling for reproducible runs
'''
import argparse
import json
import os
import random
import sys
from question_bank import QuestionBank
from config import QuizConfig
from quiz import QuizSession
DEFAULT_BANK_DIR = "banks"
def parse_args(argv=None):
    """Parse command-line arguments into an argparse.Namespace."""
    parser = argparse.ArgumentParser(
        description="Trivia quiz with configurable question banks."
    )
    parser.add_argument("--bank", metavar="PATH",
                        help="Path to a question bank JSON file.")
    parser.add_argument("--bank-dir", metavar="DIR", default=DEFAULT_BANK_DIR,
                        help=f"Directory scanned for bank files (default: {DEFAULT_BANK_DIR}).")
    parser.add_argument("--list-banks", action="store_true",
                        help="List available question banks and exit.")
    parser.add_argument("--topics", nargs="+", metavar="TOPIC", default=None,
                        help="Only ask questions on these topic(s).")
    parser.add_argument("--num", type=int, default=None, metavar="N",
                        help="Maximum number of questions to ask.")
    parser.add_argument("--no-shuffle", action="store_true",
                        help="Ask questions in bank order instead of random order.")
    parser.add_argument("--shuffle-choices", action="store_true",
                        help="Randomise the display order of multiple-choice options.")
    parser.add_argument("--show-answers", dest="show_answers",
                        action="store_true", default=True,
                        help="Show correct answers in the end-of-quiz review (default).")
    parser.add_argument("--hide-answers", dest="show_answers",
                        action="store_false",
                        help="Hide correct answers in the end-of-quiz review.")
    parser.add_argument("--immediate-feedback", action="store_true",
                        help="Tell the user immediately whether each answer is correct.")
    parser.add_argument("--seed", type=int, default=None, metavar="N",
                        help="Random seed for reproducible question/choice shuffling.")
    return parser.parse_args(argv)
def discover_banks(bank_dir):
    """Return sorted paths of *.json bank files inside `bank_dir`."""
    if not os.path.isdir(bank_dir):
        return []
    return [
        os.path.join(bank_dir, name)
        for name in sorted(os.listdir(bank_dir))
        if name.lower().endswith(".json")
    ]
def choose_bank(args, input_func, print_func):
    """Decide which bank file to load (CLI flag > interactive choice > single file)."""
    if args.bank:
        return args.bank
    files = discover_banks(args.bank_dir)
    if not files:
        print_func(f'No question banks found in "{args.bank_dir}". '
                   "Use --bank to point at a JSON file directly.")
        return None
    if len(files) == 1:
        return files[0]
    print_func("Available question banks:")
    for position, path in enumerate(files, start=1):
        print_func(f"  {position}. {path}")
    while True:
        raw = input_func(f"Select a bank [1-{len(files)}] (Enter = 1): ").strip()
        if not raw:
            return files[0]
        if raw.isdigit() and 1 <= int(raw) <= len(files):
            return files[int(raw) - 1]
        print_func("Invalid selection, please try again.")
def choose_topics(bank, args, input_func, print_func):
    """Resolve which topics to quiz on (CLI flag > interactive choice > all)."""
    available = bank.topics()
    if args.topics:
        wanted = [t.strip() for t in args.topics if t.strip()]
        known = {t.lower() for t in available}
        unknown = [t for t in wanted if t.lower() not in known]
        if unknown:
            print_func(f"Warning: unknown topic(s) {', '.join(unknown)}; "
                       f"available topics: {', '.join(available)}")
        return wanted
    if len(available) <= 1:
        return None
    print_func(f"Available topics: {', '.join(available)}")
    raw = input_func("Topics to practise (comma-separated, Enter = all): ").strip()
    if not raw or raw.lower() in ("all", "*"):
        return None
    return [t.strip() for t in raw.split(",") if t.strip()]
def main(argv=None):
    """Program entry point; returns a process exit code."""
    args = parse_args(argv)
    if args.seed is not None:
        random.seed(args.seed)
    if args.list_banks:
        files = discover_banks(args.bank_dir)
        if files:
            print("Available question banks:")
            for path in files:
                print(f"  - {path}")
        else:
            print(f'No question banks found in "{args.bank_dir}".')
        return 0
    bank_path = choose_bank(args, input, print)
    if not bank_path:
        return 1
    try:
        bank = QuestionBank.from_json_file(bank_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Could not load question bank '{bank_path}': {exc}")
        return 1
    print(f"Loaded bank '{bank.name}' with {len(bank.questions)} questions.")
    topics = choose_topics(bank, args, input, print)
    count = args.num
    if count is not None and count <= 0:
        print("--num must be a positive integer.")
        return 1
    config = QuizConfig(
        show_answers_after=args.show_answers,
        shuffle_questions=not args.no_shuffle,
        shuffle_choices=args.shuffle_choices,
        num_questions=count,
        topics=topics,
        immediate_feedback=args.immediate_feedback,
    )
    session = QuizSession(bank, config)
    session.run()
    return 0
if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        print("\nQuiz aborted.")
        sys.exit(130)