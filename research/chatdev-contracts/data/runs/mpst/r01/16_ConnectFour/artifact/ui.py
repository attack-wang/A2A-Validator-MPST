'''
ui.py
Console presentation helpers for Connect Four: welcome banner,
board printing, generic messages, and player-name collection.
Every stdin read is routed through safe_input(), which catches
EOFError (closed or exhausted stdin, e.g. non-interactive test runs)
and KeyboardInterrupt, so the program degrades gracefully instead of
crashing with an unhandled EOFError traceback.
'''
BANNER = r"""
=========================================================
   ____   ___  ____  ___   _   _____ _____ _____ _____
  |  _ \ / _ \|  _ \|_ _| / \ | ____|_   _| ____|_   _|
  | |_) | | | | |_) || | / _ \|  _|   | | |  _|   | |
  |  __/| |_| |  _ < | |/ ___ \| |___  | | | |___  | |
  |_|    \___/|_| \_\___/_/   \_\_____| |_| |_____| |_|
=========================================================
"""
def safe_input(prompt, default=None):
    """Read one line from stdin without ever raising EOFError.
    Behaviour:
      * Normal case: return the typed line.
      * EOF (stdin closed/empty) with a `default` supplied: print a
        notice and return `default` so the caller can continue.
      * EOF with no `default`: print a friendly message and exit
        cleanly via SystemExit(0) — no traceback.
      * Ctrl+C: print a friendly message and exit cleanly.
    """
    try:
        return input(prompt)
    except EOFError:
        if default is not None:
            print(f"\n[No input available — using default '{default}']")
            return default
        print("\nNo more input available. Exiting.")
        raise SystemExit(0)
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        raise SystemExit(0)
def print_welcome():
    """Print the ASCII banner and explain the game rules."""
    print(BANNER)
    print("=" * 55)
    print("            WELCOME TO CONNECT FOUR!")
    print("  Connect four discs in a row to win: horizontally,")
    print("  vertically, or diagonally. Good luck!")
    print("=" * 55)
def print_message(message):
    """Print a single message line to the console."""
    print(message)
def print_board(board, highlight=None):
    """Render and print the board, optionally highlighting winning cells."""
    print(board.render(highlight=highlight))
def get_player_name(default, disc):
    """Prompt for a player's name; fall back to `default` if left blank.
    Uses safe_input() so a closed/empty stdin falls back to the
    default name instead of crashing with an unhandled EOFError.
    """
    raw = safe_input(
        f"Enter name for {default} ({disc}) "
        f"[press Enter for '{default}']: ",
        default=default,
    )
    return raw.strip() or default