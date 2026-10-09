'''
game_controller.py
Glue between the Sudoku rules (SudokuBoard), the puzzle factory
(SudokuGenerator) and the tkinter user interface (SudokuGUI).
The controller owns the current game state and exposes the operations the
GUI triggers: starting a new game, entering/clearing values, checking for
mistakes, requesting hints and revealing the solution.
'''
import tkinter.messagebox as messagebox
from sudoku_board import SudokuBoard
from sudoku_generator import SudokuGenerator
from gui import SudokuGUI
class GameController:
    """Coordinates game state and reacts to user actions from the GUI."""
    def __init__(self):
        self.generator = SudokuGenerator()
        self.board = SudokuBoard()
        self.solution = None
        self.difficulty = "medium"
        self.game_over = False
        self.gui = SudokuGUI(self)
        self.start_new_game("medium")
    # ------------------------------------------------------------------ #
    # lifecycle
    # ------------------------------------------------------------------ #
    def run(self):
        """Hand control over to the tkinter main loop."""
        self.gui.run()
    def start_new_game(self, difficulty):
        """Generate a fresh puzzle of the requested difficulty."""
        self.difficulty = difficulty
        self.game_over = False
        puzzle, solution = self.generator.generate_puzzle(difficulty)
        self.board = SudokuBoard(puzzle)
        self.solution = solution
        self.gui.update_board_display()
        self.gui.set_status(f"New {difficulty} puzzle started — {self._count_clues()} clues given. Good luck!")
    # ------------------------------------------------------------------ #
    # player actions
    # ------------------------------------------------------------------ #
    def handle_input(self, row, col, value):
        """
        Store the player's digit (1-9) in an editable cell, or clear the cell
        when value == 0. Refreshes the view, refreshes conflict highlighting
        and checks the win condition.
        """
        if self.game_over:
            return
        if self.board.is_fixed(row, col):
            self.gui.set_status("That cell is a fixed clue and cannot be changed.")
            return
        changed = self.board.set_cell(row, col, value)
        if not changed:
            return
        self.gui.update_board_display()
        if self.gui.auto_check_enabled():
            self._refresh_conflict_highlight()
        if self.board.is_complete():
            self.game_over = True
            self.gui.celebrate_victory()
    def clear_cell(self, row, col):
        """Erase the player's value from one cell."""
        if self.game_over:
            return
        if self.board.clear_cell(row, col):
            self.gui.update_board_display()
            if self.gui.auto_check_enabled():
                self._refresh_conflict_highlight()
    def clear_all_entries(self):
        """Erase every value the player has entered (clues are kept)."""
        if self.game_over:
            return
        self.board.clear_all_player_entries()
        self.gui.update_board_display()
        self.gui.set_status("All player entries cleared.")
    def check_mistakes(self):
        """
        Explicit mistake check requested by the player. Highlights every
        conflicting cell and reports the result in the status bar.
        """
        conflicts = self.board.find_conflicts()
        self.gui.highlight_conflicts(conflicts)
        if self.board.is_complete():
            self.game_over = True
            self.gui.celebrate_victory()
        elif conflicts:
            self.gui.set_status(f"Mistakes found: {len(conflicts)} conflicting cell(s) are highlighted in red.")
        else:
            filled = self._count_filled()
            self.gui.set_status(f"No mistakes so far — {filled}/81 cells filled. Keep going!")
        return conflicts
    def give_hint(self):
        """Fill one empty or wrong cell with the correct solution value."""
        if self.game_over:
            return
        candidates = [
            (r, c)
            for r in range(SudokuBoard.SIZE)
            for c in range(SudokuBoard.SIZE)
            if not self.board.is_fixed(r, c) and self.board.get_cell(r, c) != self.solution[r][c]
        ]
        if not candidates:
            self.gui.set_status("No hint available — every editable cell is already correct.")
            return
        row, col = self.generator.rng.choice(candidates)
        self.board.set_cell(row, col, self.solution[row][col])
        self.gui.update_board_display()
        self.gui.set_status(f"Hint: the correct value at row {row + 1}, column {col + 1} was filled in.")
        if self.board.is_complete():
            self.game_over = True
            self.gui.celebrate_victory()
    def reveal_solution(self):
        """Fill the whole board with the stored solution (ends the game)."""
        if self.solution is None:
            return
        for row in range(SudokuBoard.SIZE):
            for col in range(SudokuBoard.SIZE):
                self.board.set_cell(row, col, self.solution[row][col])
        self.game_over = True
        self.gui.update_board_display()
        self.gui.set_status("Solution revealed. Start a new game to play again.")
    # ------------------------------------------------------------------ #
    # helpers
    # ------------------------------------------------------------------ #
    def _refresh_conflict_highlight(self):
        """Re-apply conflict highlighting based on the current board."""
        self.gui.highlight_conflicts(self.board.find_conflicts())
    def _count_filled(self):
        """Number of cells that currently hold a value."""
        return sum(
            1
            for row in range(SudokuBoard.SIZE)
            for col in range(SudokuBoard.SIZE)
            if self.board.get_cell(row, col) != SudokuBoard.EMPTY
        )
    def _count_clues(self):
        """Number of fixed clue cells on the board."""
        return sum(
            1
            for row in range(SudokuBoard.SIZE)
            for col in range(SudokuBoard.SIZE)
            if self.board.is_fixed(row, col)
        )