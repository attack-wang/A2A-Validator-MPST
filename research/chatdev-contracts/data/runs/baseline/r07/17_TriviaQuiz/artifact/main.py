'''
main.py
Entry point for the trivia quiz application.
Flow:
1. Parse command-line configuration (bank path, shuffle, show-answers).
2. Load and validate the JSON question bank.
3. Run the interactive quiz loop (score tracked automatically).
4. Display the final summary with the total correct answers.
5. Show the correct-answer review automatically (--show-answers) or
   after asking the user.
Robustness:
- QuizAborted (EOF on stdin / user interrupt, e.g. piped or automated runs,
  Ctrl+D / Ctrl+Z / Ctrl+C) is handled gracefully: the quiz stops, partial
  results are shown, and a clean exit code is returned — no raw traceback.
- The review confirmation defaults to "no" when input is unavailable.
'''
import sys
from config import parse_arguments
from questionbank import QuestionBank
from quiz import QuizAborted, QuizGame
def _wants_review():
    """Ask whether to review answers; default to 'no' on EOF or interrupt."""
    try:
        response = input("Would you like to review the correct answers? (y/n): ")
    except EOFError:
        return False
    except KeyboardInterrupt:
        return False
    return response.strip().lower() in ("y", "yes")
def main(argv=None):
    """Run one full quiz session and return a process exit code."""
    config = parse_arguments(argv)
    try:
        bank = QuestionBank.load_from_file(config.bank_path)
    except FileNotFoundError as exc:
        print("Error: %s" % exc)
        return 1
    except ValueError as exc:
        # load_from_file wraps JSON decode errors into ValueError as well,
        # so catching ValueError here covers invalid bank files too.
        print("Error: %s" % exc)
        return 1
    game = QuizGame(bank, shuffle=config.shuffle)
    try:
        game.run()
        game.display_results()
        if config.show_answers:
            game.display_answers()
        elif _wants_review():
            game.display_answers()
    except QuizAborted as exc:
        # EOF or interrupt mid-quiz: stop, report what was answered so far.
        print("\n%s" % exc)
        print("Showing partial results...")
        game.display_results()
        return 130
    except KeyboardInterrupt:
        print("\nQuiz aborted by user.")
        return 130
    return 0
if __name__ == "__main__":
    sys.exit(main())