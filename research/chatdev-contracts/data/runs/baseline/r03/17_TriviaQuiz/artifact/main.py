'''
Main entry point for the Trivia Quiz application.
Launches the command-line interface and handles top-level
interruptions (Ctrl+C) gracefully.
'''
import sys
from quiz_cli import QuizCLI
def main():
    '''Create the CLI and run the quiz session.'''
    cli = QuizCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted. Goodbye!")
        sys.exit(0)
if __name__ == "__main__":
    main()