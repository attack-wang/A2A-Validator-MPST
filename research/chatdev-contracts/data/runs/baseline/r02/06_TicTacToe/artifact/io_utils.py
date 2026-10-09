'''
io_utils.py
Input utility module for the Tic-Tac-Toe game.
Provides safe_input(), a centralized wrapper around built-in input() that
handles a closed or exhausted standard input stream (EOFError) gracefully.
All interactive prompts in the game (main.py, player.py, game.py) route
through this helper, so the program always terminates cleanly with a
friendly goodbye message and exit code 0 when stdin is unavailable
(e.g., automated test harnesses, piped input, or Ctrl+D / Ctrl+Z+Enter),
instead of crashing with an unhandled EOFError traceback.
'''
def safe_input(prompt: str = "") -> str:
    """Read a line from stdin; exit cleanly on EOF instead of crashing.
    Wraps built-in input() so that an EOFError (closed or exhausted stdin)
    terminates the game gracefully with a friendly message and exit code 0.
    KeyboardInterrupt is deliberately NOT caught here so the entry-point
    handler in main.py can report interruptions uniformly.
    """
    try:
        return input(prompt)
    except EOFError:
        print("\nInput stream closed. Ending the game.")
        print("Thanks for playing Tic-Tac-Toe. Goodbye!")
        raise SystemExit(0)