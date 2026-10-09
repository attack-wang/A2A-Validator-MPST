'''
gui.py
Tkinter graphical interface for the Sudoku application.
Draws the 9x9 grid, handles player input, highlights conflicts in
real time, and offers New Game / Check / Hint / Reveal / Clear actions.
'''
import tkinter as tk
from tkinter import messagebox, ttk
from sudoku_board import SudokuBoard
from sudoku_generator import SudokuGenerator
CELL_FONT = ("Arial", 18, "bold")
LABEL_FONT = ("Arial", 12)
STATUS_FONT = ("Arial", 11)
# Color palette
BG_COLOR = "#f7f5f0"         # window background
GRID_BG_COLOR = "#333333"    # grid line color (shown through cell gaps)
FIXED_COLOR = "#e0e0e0"      # background of pre-filled clue cells
USER_COLOR = "#ffffff"       # background of editable cells
CONFLICT_COLOR = "#f4a6a6"   # background of rule-violating cells
HINT_COLOR = "#fff3b0"       # background of the hinted cell
class SudokuGUI:
    """Tkinter front-end that drives a SudokuBoard."""
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        self.board = None
        self.cells = {}           # (row, col) -> tk.StringVar
        self.entry_widgets = {}   # (row, col) -> tk.Entry
        self._updating = False    # guard against trace feedback loops
        self._focused_cell = (0, 0)
        self._solved_announced = False
        self.status_var = tk.StringVar(value="Welcome! Start a new game.")
        self._build_top_bar()
        self._build_grid()
        self._build_controls()
        self._build_status_bar()
        self.new_game("Medium")
    # ------------------------------------------------------------------
    # Widget construction
    # ------------------------------------------------------------------
    def _build_top_bar(self):
        """Difficulty selector and New Game button."""
        top = tk.Frame(self.root, bg=BG_COLOR)
        top.pack(pady=(10, 4))
        tk.Label(top, text="Difficulty:", bg=BG_COLOR,
                 font=LABEL_FONT).pack(side=tk.LEFT, padx=(0, 4))
        self.difficulty_var = tk.StringVar(value="Medium")
        combo = ttk.Combobox(top, textvariable=self.difficulty_var,
                             values=list(SudokuGenerator.DIFFICULTY_LEVELS.keys()),
                             state="readonly", width=8, font=LABEL_FONT)
        combo.pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(top, text="New Game", font=LABEL_FONT,
                  command=self.new_game).pack(side=tk.LEFT, padx=3)
    def _build_grid(self):
        """Create the 9x9 Entry grid with 3x3 box separators."""
        grid_frame = tk.Frame(self.root, bg=GRID_BG_COLOR, bd=2,
                              relief="ridge")
        grid_frame.pack(padx=10, pady=6)
        for r in range(9):
            for c in range(9):
                var = tk.StringVar(value="")
                var.trace_add("write",
                              lambda name, idx, mode, rc=(r, c):
                              self._on_cell_changed(rc))
                entry = tk.Entry(grid_frame, textvariable=var, width=2,
                                 font=CELL_FONT, justify="center",
                                 relief="flat", highlightthickness=1,
                                 highlightbackground="#b0b0b0",
                                 highlightcolor="#3b7dd8")
                # Thicker gaps act as the 3x3 box separators
                pad_top = 3 if r in (3, 6) else 1
                pad_bottom = 3 if r in (2, 5) else 1
                pad_left = 3 if c in (3, 6) else 1
                pad_right = 3 if c in (2, 5) else 1
                entry.grid(row=r, column=c,
                           padx=(pad_left, pad_right),
                           pady=(pad_top, pad_bottom),
                           ipadx=8, ipady=6)
                entry.bind("<FocusIn>",
                           lambda event, rc=(r, c): self._on_focus(rc))
                # Arrow-key navigation between cells
                for key, (dr, dc) in (("Up", (-1, 0)), ("Down", (1, 0)),
                                      ("Left", (0, -1)), ("Right", (0, 1))):
                    entry.bind("<%s>" % key,
                               lambda event, rc=(r, c), dr=dr, dc=dc:
                               self._move_focus(rc, dr, dc))
                self.cells[(r, c)] = var
                self.entry_widgets[(r, c)] = entry
    def _build_controls(self):
        """Action buttons: Check / Hint / Clear / Reveal."""
        bar = tk.Frame(self.root, bg=BG_COLOR)
        bar.pack(pady=4)
        tk.Button(bar, text="Check Mistakes", font=LABEL_FONT,
                  command=self.check_mistakes).pack(side=tk.LEFT, padx=3)
        tk.Button(bar, text="Hint", font=LABEL_FONT,
                  command=self.use_hint).pack(side=tk.LEFT, padx=3)
        tk.Button(bar, text="Clear Entries", font=LABEL_FONT,
                  command=self.clear_entries).pack(side=tk.LEFT, padx=3)
        tk.Button(bar, text="Reveal Solution", font=LABEL_FONT,
                  command=self.reveal_solution).pack(side=tk.LEFT, padx=3)
    def _build_status_bar(self):
        """One-line status message under the buttons."""
        tk.Label(self.root, textvariable=self.status_var, bg=BG_COLOR,
                 font=STATUS_FONT, fg="#333333").pack(pady=(2, 8), fill=tk.X)
    # ------------------------------------------------------------------
    # Game actions
    # ------------------------------------------------------------------
    def new_game(self, difficulty=None):
        """Generate a fresh puzzle and reset the whole view."""
        if difficulty is None:
            difficulty = self.difficulty_var.get()
        generator = SudokuGenerator(difficulty)
        puzzle, solution = generator.generate()
        self.board = SudokuBoard(puzzle, solution)
        self._solved_announced = False
        self._focused_cell = (0, 0)
        self._refresh_display()
        self.status_var.set("New %s puzzle started. Good luck!" % difficulty)
    def check_mistakes(self):
        """Report wrong entries and rule conflicts to the player."""
        if self.board is None:
            return
        self._check_completion()
        mistakes = self.board.find_mistakes()
        conflicts = self.board.find_conflicts()
        if self.board.is_solved():
            return  # completion message already shown
        if not mistakes and not conflicts:
            if self.board.is_board_full():
                self.status_var.set("Everything looks correct!")
            else:
                self.status_var.set("No mistakes so far — keep going!")
        else:
            plural = "y" if len(mistakes) == 1 else "ies"
            plural2 = "" if len(conflicts) == 1 else "s"
            self.status_var.set(
                "%d wrong entr%s and %d conflicting cell%s found. "
                "They are highlighted in red." %
                (len(mistakes), plural, len(conflicts), plural2))
    def use_hint(self):
        """Fill one random empty/incorrect cell with the correct digit."""
        if self.board is None:
            return
        hint = self.board.get_hint()
        if hint is None:
            self.status_var.set("No hints available — the board is complete.")
            return
        row, col, value = hint
        self.board.set_value(row, col, value)
        self._refresh_display()
        # Flash the hinted cell so the player can spot it
        self.entry_widgets[(row, col)].configure(bg=HINT_COLOR)
        self.status_var.set("Hint: row %d, column %d should be %d."
                            % (row + 1, col + 1, value))
        self._check_completion()
    def clear_entries(self):
        """Erase all player entries, keeping the original clues."""
        if self.board is None:
            return
        self.board.clear_user_entries()
        self._refresh_display()
        self.status_var.set("All player entries cleared.")
    def reveal_solution(self):
        """Show the full solution after a confirmation dialog."""
        if self.board is None:
            return
        if messagebox.askyesno("Reveal Solution",
                               "Reveal the full solution?\n"
                               "This ends the current puzzle."):
            self.board.reveal_solution()
            self._refresh_display()
            self._solved_announced = True
            self.status_var.set("Solution revealed. "
                                "Start a New Game to play again.")
    # ------------------------------------------------------------------
    # Input handling
    # ------------------------------------------------------------------
    def _on_focus(self, cell):
        """Remember which cell the player is editing."""
        self._focused_cell = cell
    def _move_focus(self, cell, delta_row, delta_col):
        """Move keyboard focus with the arrow keys."""
        row = min(8, max(0, cell[0] + delta_row))
        col = min(8, max(0, cell[1] + delta_col))
        self.entry_widgets[(row, col)].focus_set()
    def _on_cell_changed(self, cell):
        """Sanitize input, store it on the board and refresh highlights."""
        if self._updating or self.board is None:
            return
        row, col = cell
        var = self.cells[cell]
        raw = var.get()
        # Keep only the last digit typed; anything else clears the cell
        digit = ""
        for ch in raw:
            if ch in "123456789":
                digit = ch
        self._updating = True
        var.set(digit)
        self._updating = False
        if digit:
            self.board.set_value(row, col, int(digit))
        else:
            self.board.clear_cell(row, col)
        self._refresh_highlights()
        self._check_completion()
    # ------------------------------------------------------------------
    # Display refresh
    # ------------------------------------------------------------------
    def _refresh_display(self):
        """Sync every cell's text, state and color with the board."""
        self._updating = True
        for r in range(9):
            for c in range(9):
                value = self.board.get_value(r, c)
                self.cells[(r, c)].set("" if value == 0 else str(value))
                entry = self.entry_widgets[(r, c)]
                if self.board.is_fixed_cell(r, c):
                    entry.configure(state="readonly",
                                    readonlybackground=FIXED_COLOR)
                else:
                    entry.configure(state="normal", bg=USER_COLOR)
        self._updating = False
        self._refresh_highlights()
    def _refresh_highlights(self):
        """Color rule-violating cells red in real time."""
        conflicts = self.board.find_conflicts()
        for r in range(9):
            for c in range(9):
                entry = self.entry_widgets[(r, c)]
                if self.board.is_fixed_cell(r, c):
                    bg = FIXED_COLOR
                elif (r, c) in conflicts:
                    bg = CONFLICT_COLOR
                else:
                    bg = USER_COLOR
                entry.configure(bg=bg, readonlybackground=bg)
    def _check_completion(self):
        """Congratulate the player exactly once when the puzzle is solved."""
        if self.board.is_solved() and not self._solved_announced:
            self._solved_announced = True
            self._refresh_highlights()
            messagebox.showinfo("Sudoku",
                                "Congratulations! You solved the puzzle!")
            self.status_var.set("Puzzle complete! "
                                "Choose New Game to play again.")