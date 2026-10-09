'''
sudoku_gui.py
Tkinter graphical interface for the classic Sudoku puzzle game.
Features:
* 9x9 clickable grid with visual separation of the 3x3 subgrids
* keyboard input restricted to the digits 1-9
* arrow-key navigation between cells
* real-time mistake highlighting (row / column / subgrid conflicts)
* status bar with progress, conflict count and elapsed time
* "Check" button that reports mistakes / empty cells
* automatic congratulation dialog when the puzzle is solved
* new-game generation at three difficulty levels, restart, clear
  user entries and solution reveal
'''
import time
import tkinter as tk
from tkinter import messagebox
from sudoku_engine import SudokuBoard, SudokuGenerator, SudokuSolver
class SudokuGUI:
    """Main application window of the Sudoku game."""
    # ------------------------------------------------------------------ style
    WINDOW_BG = "#f4f1ea"
    GRID_BG = "#ffffff"
    LINE_COLOR = "#9e9a90"
    BOX_LINE_COLOR = "#5f5b54"
    FIXED_BG = "#e6e2d8"
    FIXED_FG = "#3a3a3a"
    USER_FG = "#1a4f8b"
    CONFLICT_BG = "#f5b7b1"
    CONFLICT_FG = "#7b241c"
    SOLVED_BG = "#a9dfbf"
    SELECT_BG = "#d6e4f0"
    CELL_FONT = ("Helvetica", 18, "bold")
    LABEL_FONT = ("Helvetica", 11)
    STATUS_FONT = ("Helvetica", 10)
    DIFFICULTIES = ("easy", "medium", "hard")
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.configure(bg=self.WINDOW_BG)
        self.root.resizable(False, False)
        self.board = SudokuBoard()
        self.cells = [[None] * 9 for _ in range(9)]
        self.solved_announced = False
        self.game_over = False
        self.elapsed_seconds = 0
        self._timer_job = None
        self._build_menu()
        self._build_grid()
        self._build_controls()
        self._start_timer()
        self.new_game("medium")
    # ------------------------------------------------------------------ menu
    def _build_menu(self):
        """Create the top-level menu bar."""
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        for diff in self.DIFFICULTIES:
            game_menu.add_command(
                label=f"New {diff.title()} Game",
                command=lambda d=diff: self.new_game(d))
        game_menu.add_separator()
        game_menu.add_command(label="Restart", command=self.restart_game)
        game_menu.add_command(label="Clear My Entries", command=self.clear_entries)
        game_menu.add_command(label="Reveal Solution", command=self.reveal_solution)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="Game", menu=game_menu)
        self.root.config(menu=menubar)
    # ------------------------------------------------------------------ grid
    def _build_grid(self):
        """Build the 9x9 grid as nine 3x3 framed boxes."""
        board_frame = tk.Frame(self.root, bg=self.BOX_LINE_COLOR, bd=2)
        board_frame.grid(row=0, column=0, padx=10, pady=(10, 4))
        for br in range(3):
            for bc in range(3):
                box = tk.Frame(board_frame, bd=1, bg=self.BOX_LINE_COLOR)
                box.grid(row=br, column=bc, padx=2, pady=2)
                for i in range(3):
                    for j in range(3):
                        self._create_cell(box, br * 3 + i, bc * 3 + j, i, j)
    def _create_cell(self, parent, row, col, inner_row, inner_col):
        """Create one Entry widget and register its bindings."""
        entry = tk.Entry(
            parent,
            width=2,
            font=self.CELL_FONT,
            justify="center",
            bd=0,
            highlightthickness=1,
            highlightbackground=self.LINE_COLOR,
            highlightcolor=self.BOX_LINE_COLOR,
            insertontime=0,
            disabledbackground=self.FIXED_BG,
        )
        entry.grid(row=inner_row, column=inner_col, padx=1, pady=1, ipady=4)
        vcmd = (self.root.register(self._validate_input), "%P")
        entry.configure(validate="key", validatecommand=vcmd)
        entry.bind("<KeyRelease>", lambda e, r=row, c=col: self._on_cell_changed(r, c))
        entry.bind("<FocusOut>", lambda e, r=row, c=col: self._on_focus_out(r, c))
        entry.bind("<Up>", lambda e, r=row, c=col: self._move_focus(r, c, -1, 0))
        entry.bind("<Down>", lambda e, r=row, c=col: self._move_focus(r, c, 1, 0))
        entry.bind("<Left>", lambda e, r=row, c=col: self._move_focus(r, c, 0, -1))
        entry.bind("<Right>", lambda e, r=row, c=col: self._move_focus(r, c, 0, 1))
        entry.bind("<Home>", lambda e, r=row, c=col: self._move_focus(r, c, -row, -col))
        entry.bind("<End>", lambda e, r=row, c=col: self._move_focus(r, c, 8 - row, 8 - col))
        self.cells[row][col] = entry
    def _validate_input(self, new_text):
        """Allow only empty text or a single digit 1-9."""
        return new_text == "" or (len(new_text) == 1 and new_text in "123456789")
    def _move_focus(self, row, col, dr, dc):
        """Move keyboard focus to a neighbouring cell (clamped to board)."""
        new_row = min(max(row + dr, 0), 8)
        new_col = min(max(col + dc, 0), 8)
        self.cells[new_row][new_col].focus_set()
        return "break"
    # ------------------------------------------------------------- controls
    def _build_controls(self):
        """Build the button bar and the status label."""
        bar = tk.Frame(self.root, bg=self.WINDOW_BG)
        bar.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 4))
        tk.Button(bar, text="Check", command=self.check_board).grid(row=0, column=0, padx=4)
        tk.Button(bar, text="Clear Entries", command=self.clear_entries).grid(row=0, column=1, padx=4)
        tk.Button(bar, text="Restart", command=self.restart_game).grid(row=0, column=2, padx=4)
        self.status_label = tk.Label(bar, text="", font=self.STATUS_FONT, bg=self.WINDOW_BG)
        self.status_label.grid(row=0, column=3, padx=10)
    # ---------------------------------------------------------------- timer
    def _start_timer(self):
        """Start the periodic one-second timer tick."""
        self._timer_job = self.root.after(1000, self._tick)
    def _tick(self):
        """Advance the elapsed-time counter and refresh the status bar."""
        self.elapsed_seconds += 1
        self._update_status()
        self._timer_job = self.root.after(1000, self._tick)
    # ------------------------------------------------------------ game flow
    def new_game(self, difficulty="medium"):
        """Generate a fresh puzzle, reset all state and refresh the grid."""
        puzzle, solution = SudokuGenerator().generate(difficulty)
        self.board = SudokuBoard(puzzle, solution)
        self.solved_announced = False
        self.game_over = False
        self.elapsed_seconds = 0
        self._refresh_all_cells()
        self._update_status()
    def restart_game(self):
        """Clear the user's entries but keep the same puzzle."""
        self.board.clear_user_entries()
        self.solved_announced = False
        self.game_over = False
        self._refresh_all_cells()
        self._update_status()
    def clear_entries(self):
        """Alias of restart: wipe every editable cell."""
        self.restart_game()
    def reveal_solution(self):
        """Fill the grid with the stored solution and stop the game."""
        if not self.board.solution:
            messagebox.showinfo("Sudoku", "No solution available.")
            return
        self.game_over = True
        for r in range(9):
            for c in range(9):
                entry = self.cells[r][c]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, str(self.board.solution[r][c]))
                if self.board.is_fixed(r, c):
                    entry.config(state="disabled", disabledforeground=self.FIXED_FG)
                else:
                    entry.config(fg=self.USER_FG, bg=self.SOLVED_BG)
        self._update_status()
    def check_board(self):
        """Report mistakes and empty cells, or confirm a correct solution."""
        if self.board.is_solved():
            messagebox.showinfo("Check", "The puzzle is solved correctly!")
            return
        conflicts = self.board.find_conflicts()
        empty = self.board.count_empty()
        messages = []
        if conflicts:
            messages.append(f"{len(conflicts)} conflicting cell(s) are highlighted in red")
        if empty:
            messages.append(f"{empty} empty cell(s) remaining")
        messagebox.showwarning("Check", "; ".join(messages) or "Keep going!")
    # ------------------------------------------------------- grid refresh
    def _refresh_all_cells(self):
        """Push the board state into all 81 Entry widgets."""
        for r in range(9):
            for c in range(9):
                entry = self.cells[r][c]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                value = self.board.get_cell(r, c)
                if value:
                    entry.insert(0, str(value))
                if self.board.is_fixed(r, c):
                    entry.config(state="disabled",
                                 disabledforeground=self.FIXED_FG,
                                 disabledbackground=self.FIXED_BG)
                else:
                    entry.config(state="normal",
                                 fg=self.USER_FG,
                                 bg=self.GRID_BG)
        self._highlight_conflicts()
    def _highlight_conflicts(self):
        """Recolor editable cells according to current conflicts."""
        conflicts = self.board.find_conflicts()
        for r in range(9):
            for c in range(9):
                if self.board.is_fixed(r, c):
                    continue
                entry = self.cells[r][c]
                if (r, c) in conflicts:
                    entry.config(bg=self.CONFLICT_BG, fg=self.CONFLICT_FG)
                else:
                    entry.config(bg=self.GRID_BG, fg=self.USER_FG)
    # ------------------------------------------------------ event handlers
    def _on_cell_changed(self, row, col):
        """Sync an Entry with the board, recolor conflicts, update the
        status bar and announce completion exactly once."""
        if self.game_over:
            return
        text = self.cells[row][col].get()
        value = int(text) if len(text) == 1 and text in "123456789" else 0
        self.board.set_cell(row, col, value)
        self._highlight_conflicts()
        self._update_status()
        if self.board.is_solved() and not self.solved_announced:
            self.solved_announced = True
            self.game_over = True
            messagebox.showinfo(
                "Sudoku",
                f"Congratulations! Puzzle solved in {self.elapsed_seconds} seconds.")
    def _on_focus_out(self, row, col):
        """Normalize invalid or empty text when a cell loses focus."""
        if self.game_over:
            return
        entry = self.cells[row][col]
        text = entry.get()
        if len(text) != 1 or text not in "123456789":
            entry.delete(0, tk.END)
            self.board.set_cell(row, col, 0)
            self._highlight_conflicts()
            self._update_status()
    # -------------------------------------------------------------- status
    def _update_status(self):
        """Refresh the status bar text."""
        filled = self.board.count_filled()
        conflicts = len(self.board.find_conflicts())
        self.status_label.config(
            text=(f"Filled: {filled}/81  |  Conflicts: {conflicts}  |  "
                  f"Time: {self.elapsed_seconds}s"))