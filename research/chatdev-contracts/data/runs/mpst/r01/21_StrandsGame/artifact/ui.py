'''
ui.py
Terminal presentation layer and command parser for the Strands game.
Fixes applied per test report:
- Bug #1: file reassembled from mis-filed fragments (board output had leaked
  into the source, causing IndentationError on import).
- Bug #2: MergeResult/MergeStatus are imported from validator (they are not
  importable from game).
- Bug #4: show_completion() fully implemented (victory banner + stats).
- Bug #5: unused Iterable import removed; HELP_TEXT given real content.
'''
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple
from game import StrandsGame
from validator import MergeResult, MergeStatus
BOARD_COLUMNS = 4
CELL_WIDTH = 14
HELP_TEXT = """\
Commands:
  select <n> [<n>...]   toggle strand(s) into/out of the selection (1-based)
  undo                  remove the last selected strand
  clear                 empty the selection
  submit                attempt to merge the selected strands
  hint                  reveal the first strand of a random unfound merge
  status                show theme and progress
  found                 list merges found so far
  help                  show this help
  quit                  leave the game
"""
@dataclass
class Command:
    verb: str
    numbers: Tuple[int, ...] = ()
def parse_command(line: str) -> Command:
    tokens = line.split()
    if not tokens:
        return Command("")
    verb = tokens[0].lower()
    numbers: List[int] = []
    for token in tokens[1:]:
        try:
            numbers.append(int(token))
        except ValueError:
            continue  # tolerate trailing junk; ignore non-numeric tokens
    return Command(verb, tuple(numbers))
class TerminalUI:
    def __init__(self, columns: int = BOARD_COLUMNS):
        self.columns = columns
    def show_puzzle_header(self, game: StrandsGame) -> None:
        p = game.puzzle
        print("=" * 60)
        print(f"  STRANDS — Theme: {p.theme}")
        print(f"  Merge all {p.target_count} targets from {p.total_strands} strands.")
        print("=" * 60)
    def render_board(self, game: StrandsGame) -> None:
        print("\n--- Strand Board ---")
        cells = []
        for i, strand in enumerate(game.strands):
            label = f"[{i + 1:>2}]"
            if strand.used:
                text = "-" * max(len(strand.text), 3)
            else:
                marker = "*" if strand.hinted else ""
                text = f"{marker}{strand.text}" if marker else strand.text
            cells.append(f"{label} {text}")
        for row_start in range(0, len(cells), self.columns):
            row = cells[row_start:row_start + self.columns]
            print("".join(cell.ljust(CELL_WIDTH) for cell in row))
        print("( * = hinted strand, --- = already merged )")
    def render_selection(self, game: StrandsGame, preview: Optional[MergeResult]) -> None:
        if not game.selection:
            print("\nSelection: (empty) — e.g. type: select 1 2 3")
            return
        texts = [game.strands[i].text for i in game.selection]
        print("\nSelection: " + " + ".join(texts) + f"  ({len(texts)} strand(s))")
        if preview is not None:
            print(f"  preview: {preview.message}")
    def render_found(self, game: StrandsGame) -> None:
        print(f"\n--- Found Merges ({game.progress()}) ---")
        if not game.found:
            print("  (none yet)")
        for record in game.found:
            print(f"  ✔ {record.phrase}")
        print()
    def render_result(self, result: MergeResult) -> None:
        tag = {
            MergeStatus.VALID: "[VALID]",
            MergeStatus.ALREADY_FOUND: "[REPEAT]",
            MergeStatus.PARTIAL: "[PARTIAL]",
            MergeStatus.INVALID: "[INVALID]",
        }[result.status]
        print(f"{tag} {result.message}")
    def show_message(self, message: str) -> None:
        print(message)
    def show_completion(self, game: StrandsGame) -> None:
        elapsed = time.time() - game.started_at
        print("\n" + "=" * 60)
        print("  🎉 PUZZLE COMPLETE — all strands merged!")
        print(f"  Theme: {game.puzzle.theme}")
        print(f"  Merges: {game.progress()}   Attempts: {game.attempts} "
              f"(valid: {game.valid_merges})   Hints: {game.hints_used}   "
              f"Time: {elapsed:.0f}s")
        print("=" * 60)
        for record in game.found:
            print(f"  ✔ {record.phrase}")
    def show_help(self) -> None:
        print(HELP_TEXT)