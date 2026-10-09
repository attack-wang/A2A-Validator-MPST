'''
main.py
Entry point for the Strands word-segmentation puzzle.
Fixes applied per test report:
- Bug #3: run_session() (and dispatch()) now live here instead of game.py,
  removing the NameError on startup and the ui<->game circular import.
- Bug #5: unused Command import removed; __main__ entry guard added.
'''
import argparse
import random
from typing import Optional
from game import StrandsGame
from puzzle import PUZZLE_LIBRARY, Puzzle
from ui import TerminalUI, parse_command
def choose_puzzle(library, request, rng) -> Puzzle:
    if request:
        # by 1-based index
        if request.strip().isdigit():
            idx = int(request) - 1
            if 0 <= idx < len(library):
                return library[idx]
            raise SystemExit(f"Puzzle index out of range: 1..{len(library)}")
        # by theme substring
        matches = [p for p in library if request.lower() in p.theme.lower()]
        if matches:
            return matches[0]
        raise SystemExit(f"No puzzle theme matches '{request}'.")
    return rng.choice(library)
def dispatch(game, ui, command) -> Optional[str]:
    """Handle one parsed command. Returns 'complete'/'quit' or None to continue."""
    verb = command.verb
    if verb in ("select", "toggle", "s", "t", "pick"):
        if not command.numbers:
            ui.show_message("Usage: select <strand number> [<number> ...]")
            return None
        for number in command.numbers:
            ui.show_message(game.toggle_select(number - 1))
        return None
    if verb == "undo" or verb == "u":
        text = game.undo_selection()
        ui.show_message(f"Removed '{text}' from selection." if text else "Selection is already empty.")
        return None
    if verb == "clear" or verb == "c":
        ui.show_message(game.clear_selection())
        return None
    if verb in ("submit", "merge", "go", "x"):
        if not game.selection:
            ui.show_message("Nothing to merge — select strands first (e.g. select 1 2 3).")
            return None
        result = game.submit()
        ui.render_result(result)
        if result.is_valid and game.is_complete():
            return "complete"
        return None
    if verb == "hint" or verb == "h":
        message = game.get_hint()
        ui.show_message(message if message else "No hints left — every merge is found or the board is stuck.")
        return None
    if verb == "status":
        ui.show_puzzle_header(game)
        return None
    if verb in ("found", "list"):
        ui.render_found(game)
        return None
    if verb in ("help", "?"):
        ui.show_help()
        return None
    if verb in ("quit", "exit", "q"):
        return "quit"
    if verb == "":
        return None
    ui.show_message(f"Unknown command '{verb}'. Type 'help' for the command list.")
    return None
def run_session(game: StrandsGame, ui: TerminalUI) -> str:
    """Drive one puzzle from start to completion/quit. Returns 'complete' or 'quit'."""
    ui.show_puzzle_header(game)
    ui.show_help()
    while True:
        ui.render_board(game)
        preview = game.preview()
        ui.render_selection(game, preview)
        ui.render_found(game)
        try:
            line = input("\nStrands> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return "quit"
        outcome = dispatch(game, ui, parse_command(line))
        if outcome in ("complete", "quit"):
            if outcome == "complete":
                ui.show_completion(game)
            return outcome
def main() -> None:
    parser = argparse.ArgumentParser(description="Play the Strands word-segmentation puzzle.")
    parser.add_argument("--puzzle", default="", help="puzzle index (1-based) or theme substring")
    parser.add_argument("--seed", type=int, default=None, help="random seed for strand shuffling")
    args = parser.parse_args()
    rng = random.Random(args.seed)
    ui = TerminalUI()
    while True:
        puzzle = choose_puzzle(PUZZLE_LIBRARY, args.puzzle, rng)
        game = StrandsGame(puzzle, seed=rng.randint(0, 2**31 - 1))
        outcome = run_session(game, ui)
        if outcome == "quit":
            print("Thanks for playing Strands — goodbye!")
            return
        # completed
        try:
            reply = input("Play another puzzle? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if reply not in ("y", "yes"):
            print("Thanks for playing Strands — goodbye!")
            return
        args.puzzle = ""  # after finishing one, pick randomly next time
if __name__ == "__main__":
    main()