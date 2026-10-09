'''
game_controller.py
Defines the GameController class, which coordinates the Sudoku game flow.
It owns the board and puzzle generator, processes player input, runs
mistake checks, detects completion, and drives the graphical interface.
'''
from sudoku_board import SudokuBoard
from puzzle_generator import PuzzleGenerator
from game_ui import GameUI
class GameController:
    """Coordinates the Sudoku game flow between board logic and the UI."""
    def __init__(self):
        self.board = SudokuBoard()
        self.generator = PuzzleGenerator()
        self.ui = GameUI(self)
        self.solution = None
        self.selected = None  # (row, col) or None
        self.conflicts = set()
        self.mistakes_found = 0
        self.game_over = False
    def new_game(self, difficulty):
        """Generate a fresh puzzle and reset all game state."""
        puzzle, solution, given = self.generator.generate_puzzle(difficulty)
        self.board.reset()
        for r in range(9):
            for c in range(9):
                if given[r][c]:
                    self.board.set_given(r, c, puzzle[r][c])
        self.solution = solution
        self.selected = None
        self.conflicts = set()
        self.mistakes_found = 0
        self.game_over = False
        self.ui.render(self.board, self.selected, self.conflicts,
                       f"New {difficulty} puzzle started. Good luck!")
    def select_cell(self, row, col):
        """Select a cell for input (givens can be selected but not edited)."""
        if self.game_over:
            return
        self.selected = (row, col)
        self._refresh(f"Selected cell R{row + 1}C{col + 1}.")
    def enter_value(self, value):
        """Place the player's digit in the selected cell and re-check."""
        if self.game_over or self.selected is None:
            return
        row, col = self.selected
        if self.board.is_given(row, col):
            self.ui.show_status("That cell is pre-filled and cannot be changed.")
            return
        self.board.set_value(row, col, value)
        self.conflicts = self.board.find_conflicts()  # live mistake highlighting
        if value != 0 and self.board.is_solved():
            self.game_over = True
            self.conflicts = set()
            self.ui.render(self.board, self.selected, self.conflicts,
                           "Puzzle solved! Well done.")
            self.ui.show_completion()
        else:
            self._refresh(f"Placed {value} in R{row + 1}C{col + 1}." if value else
                          f"Cleared R{row + 1}C{col + 1}.")
    def clear_selected(self):
        """Erase the player's value from the selected cell."""
        if self.game_over or self.selected is None:
            return
        row, col = self.selected
        if self.board.is_given(row, col):
            self.ui.show_status("That cell is pre-filled and cannot be changed.")
            return
        if self.board.clear_cell(row, col):
            self.conflicts = self.board.find_conflicts()
            self._refresh(f"Cleared R{row + 1}C{col + 1}.")
    def move_selection(self, drow, dcol):
        """Move the selection one cell in the given direction."""
        if self.game_over:
            return
        if self.selected is None:
            self.selected = (0, 0)
        else:
            row = min(max(self.selected[0] + drow, 0), 8)
            col = min(max(self.selected[1] + dcol, 0), 8)
            self.selected = (row, col)
        self._refresh(f"Selected cell R{self.selected[0] + 1}C{self.selected[1] + 1}.")
    def check_mistakes(self):
        """Run an explicit mistake check and report the result."""
        self.conflicts = self.board.find_conflicts()
        count = len(self.conflicts)
        if count == 0:
            message = "No mistakes so far. Keep going!"
        else:
            message = f"Found {count} conflicting cell(s), highlighted in red."
        self._refresh(message)
    def give_hint(self):
        """Fill the selected (or a random empty) cell with the correct value."""
        if self.game_over:
            return
        if self.solution is None:
            return
        target = None
        if self.selected is not None:
            row, col = self.selected
            if self.board.get_value(row, col) != self.solution[row][col]:
                target = (row, col)
        if target is None:
            empties = [(r, c) for r in range(9) for c in range(9)
                       if self.board.get_value(r, c) != self.solution[r][c]]
            if not empties:
                self.ui.show_status("Nothing left to hint — the board matches the solution!")
                return
            target = self.generator.rng.choice(empties)
        row, col = target
        self.board.set_value(row, col, self.solution[row][col])
        self.conflicts = self.board.find_conflicts()
        if self.board.is_solved():
            self.game_over = True
            self.conflicts = set()
            self.ui.render(self.board, self.selected, self.conflicts,
                           "Puzzle solved! Well done.")
            self.ui.show_completion()
        else:
            self._refresh(f"Hint: {self.solution[row][col]} placed in R{row + 1}C{col + 1}.")
    def _refresh(self, message=""):
        """Re-render the board with current state and a status message."""
        self.ui.render(self.board, self.selected, self.conflicts, message)
    def run(self):
        """Start a default game and launch the UI event loop."""
        self.new_game("Medium")
        self.ui.run()