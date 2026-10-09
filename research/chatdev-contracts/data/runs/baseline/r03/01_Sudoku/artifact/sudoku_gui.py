'''
sudoku_gui.py
Tkinter front end for the classic Sudoku game.
Renders the 9x9 board on a canvas, handles mouse selection and keyboard
input, highlights rule conflicts in real time, offers mistake checking,
hints, difficulty selection, and confirms completion with a victory dialog.
'''
import random
import time
import tkinter as tk
from tkinter import messagebox, ttk
from sudoku_board import SudokuBoard
from sudoku_generator import SudokuGenerator
class SudokuGUI(tk.Frame):
    """Interactive Tkinter frame hosting the complete Sudoku game UI."""
    CELL = 56
    MARGIN = 24
    WIDTH = MARGIN * 2 + CELL * 9
    HEIGHT = WIDTH
    # Color palette for board rendering.
    BG_COLOR = "#faf6ec"
    LINE_COLOR = "#3a3a3a"
    BOX_LINE_COLOR = "#1c1c1c"
    FIXED_COLOR = "#2b2b2b"
    USER_COLOR = "#1a5fb4"
    HINT_COLOR = "#7d3cb5"
    SELECT_COLOR = "#ffe08a"
    PEER_COLOR = "#eef3e2"
    SAME_COLOR = "#cfe0f5"
    CONFLICT_COLOR = "#f5b0a8"
    ERROR_COLOR = "#d7263d"
    def __init__(self, master):
        """Construct the UI, bind keyboard input, and launch a medium game."""
        super().__init__(master)
        self.master = master
        self.generator = SudokuGenerator()
        self.board = None                 # SudokuBoard instance (set in new_game)
        self.selected = None              # (row, col) of the selected cell or None
        self._game_over = False           # True once the puzzle has been solved
        self._show_errors = False         # whether mistake highlighting is active
        self._error_cells = set()         # cells flagged by "Check Mistakes"
        self._hint_cells = set()          # cells revealed by hints
        self._start_time = time.time()    # timestamp of the current game start
        self._mistakes = 0                # number of wrong entries made
        self._build_ui()
        self._bind_keys()
        self.new_game("medium")
        self.after(1000, self._tick)      # start the elapsed-time updater
    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        """Create the control bar, board canvas, and status bar."""
        bar = tk.Frame(self)
        bar.pack(fill="x", padx=self.MARGIN, pady=(self.MARGIN, 4))
        tk.Label(bar, text="Difficulty:").pack(side="left")
        self.difficulty_var = tk.StringVar(value="medium")
        ttk.Combobox(bar, textvariable=self.difficulty_var, state="readonly",
                     values=("easy", "medium", "hard"),
                     width=8).pack(side="left", padx=(4, 8))
        tk.Button(bar, text="New Game",
                  command=self._on_new_game).pack(side="left", padx=4)
        tk.Button(bar, text="Check Mistakes",
                  command=self._check_mistakes).pack(side="left", padx=4)
        tk.Button(bar, text="Hint",
                  command=self._give_hint).pack(side="left", padx=4)
        self.mistake_label = tk.Label(bar, text="Mistakes: 0")
        self.mistake_label.pack(side="right", padx=(8, 0))
        self.time_label = tk.Label(bar, text="Time: 00:00")
        self.time_label.pack(side="right")
        self.canvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT,
                                bg=self.BG_COLOR, highlightthickness=0)
        self.canvas.pack(padx=self.MARGIN, pady=4)
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.status_label = tk.Label(self, text="", anchor="w")
        self.status_label.pack(fill="x", padx=self.MARGIN, pady=(0, self.MARGIN))
    def _bind_keys(self):
        """Bind digit entry, clearing, and arrow-key navigation to the canvas."""
        self.canvas.configure(takefocus=True)
        for digit in "123456789":
            self.canvas.bind(digit,
                             lambda event, d=int(digit): self._enter_value(d))
        self.canvas.bind("0", lambda event: self._clear_cell())
        self.canvas.bind("<Delete>", lambda event: self._clear_cell())
        self.canvas.bind("<BackSpace>", lambda event: self._clear_cell())
        self.canvas.bind("<Up>", lambda event: self._move_selection(-1, 0))
        self.canvas.bind("<Down>", lambda event: self._move_selection(1, 0))
        self.canvas.bind("<Left>", lambda event: self._move_selection(0, -1))
        self.canvas.bind("<Right>", lambda event: self._move_selection(0, 1))
    # ------------------------------------------------------------- events
    def _on_canvas_click(self, event):
        """Select the board cell under the mouse cursor."""
        if self._game_over:
            return
        col = (event.x - self.MARGIN) // self.CELL
        row = (event.y - self.MARGIN) // self.CELL
        if 0 <= row < 9 and 0 <= col < 9:
            self.selected = (int(row), int(col))
            self.canvas.focus_set()
            self._redraw()
            self._set_status(f"Selected cell R{row + 1}C{col + 1}")
    def _enter_value(self, value):
        """Place the typed digit into the selected editable cell."""
        if self._game_over or self.selected is None:
            return
        row, col = self.selected
        if self.board.is_fixed(row, col):
            self._set_status("That cell is a given clue and cannot be changed.")
            return
        if not self.board.set_value(row, col, value):
            self._set_status("Invalid entry; please type a digit from 1 to 9.")
            return
        if value != self.board.get_solution_value(row, col):
            self._mistakes += 1
            self.mistake_label.config(text=f"Mistakes: {self._mistakes}")
        self._error_cells.discard((row, col))
        self._show_errors = False
        self._redraw()
        if self.board.is_complete():
            self._check_victory()
    def _clear_cell(self):
        """Erase the selected editable cell."""
        if self._game_over or self.selected is None:
            return
        row, col = self.selected
        if self.board.is_fixed(row, col):
            self._set_status("That cell is a given clue and cannot be changed.")
            return
        self.board.clear_value(row, col)
        self._error_cells.discard((row, col))
        self._redraw()
    def _move_selection(self, drow, dcol):
        """Move the selection with the arrow keys, clamped to the board."""
        if self._game_over:
            return
        if self.selected is None:
            self.selected = (0, 0)
        else:
            row, col = self.selected
            self.selected = (max(0, min(8, row + drow)),
                             max(0, min(8, col + dcol)))
        self._redraw()
    # ----------------------------------------------------------- commands
    def _on_new_game(self):
        """Start a fresh game at the difficulty chosen in the combobox."""
        self.new_game(self.difficulty_var.get())
    def new_game(self, difficulty="medium"):
        """Generate a new puzzle, reset all state, and redraw the board."""
        puzzle, solution = self.generator.generate(difficulty)
        self.board = SudokuBoard(puzzle, solution)
        self.selected = None
        self._game_over = False
        self._show_errors = False
        self._error_cells = set()
        self._hint_cells = set()
        self._mistakes = 0
        self.mistake_label.config(text="Mistakes: 0")
        self._start_time = time.time()
        self._set_status(f"New {difficulty} puzzle started. Good luck!")
        self._redraw()
    def _check_mistakes(self):
        """Highlight wrong entries and rule conflicts; confirm completion."""
        if self._game_over:
            self._set_status("Game over — start a new game to play again.")
            return
        self._error_cells = self.board.find_incorrect_cells()
        conflicts = self.board.find_conflicts()
        self._show_errors = True
        self._redraw()
        if self.board.is_complete():
            self._check_victory()  # handles victory
        elif self._error_cells or conflicts:
            n = len(self._error_cells)
            msg = f"Found {n} incorrect cell(s) (marked in red)."
            if conflicts:
                msg += (f" {len(conflicts)} cell(s) break the "
                        f"row/column/box rule (dark red).")
            self._set_status(msg)
        else:
            self._set_status("No mistakes so far — keep going!")
    def _give_hint(self):
        """Reveal the correct value for one open or wrong cell."""
        if self._game_over:
            self._set_status("Game over — start a new game to play again.")
            return
        candidates = [(r, c) for r in range(9) for c in range(9)
                      if not self.board.is_fixed(r, c)
                      and self.board.get_value(r, c)
                      != self.board.get_solution_value(r, c)]
        if not candidates:
            self._set_status("No hint needed — everything matches so far!")
            if self.board.is_complete():
                self._check_victory()
            return
        row, col = random.choice(candidates)
        value = self.board.get_solution_value(row, col)
        self.board.set_value(row, col, value)
        self._hint_cells.add((row, col))
        self._error_cells.discard((row, col))
        self.selected = (row, col)
        self._redraw()
        self._set_status(f"Hint: R{row + 1}C{col + 1} is {value}.")
        if self.board.is_complete():
            self._check_victory()
    def _check_victory(self):
        """Confirm completion with a congratulation dialog and stop play."""
        self._game_over = True
        self._show_errors = False
        self._error_cells = set()
        self._redraw()
        elapsed = int(time.time() - self._start_time)
        messagebox.showinfo(
            "Congratulations!",
            f"Puzzle solved correctly!\n"
            f"Time: {elapsed // 60:02d}:{elapsed % 60:02d}   "
            f"Mistakes: {self._mistakes}")
        self._set_status("Solved! Press 'New Game' to play again.")
    # ----------------------------------------------------------- rendering
    def _redraw(self):
        """Render grid lines, cell highlights, and all values."""
        self.canvas.delete("all")
        board_px = self.CELL * 9
        for i in range(10):
            offset = self.MARGIN + i * self.CELL
            if i % 3 == 0:
                color, width = self.BOX_LINE_COLOR, 3
            else:
                color, width = self.LINE_COLOR, 1
            self.canvas.create_line(offset, self.MARGIN, offset,
                                    self.MARGIN + board_px,
                                    fill=color, width=width)
            self.canvas.create_line(self.MARGIN, offset,
                                    self.MARGIN + board_px, offset,
                                    fill=color, width=width)
        if self.board is None:
            return
        conflicts = self.board.find_conflicts()
        for r in range(9):
            for c in range(9):
                x0 = self.MARGIN + c * self.CELL
                y0 = self.MARGIN + r * self.CELL
                x1, y1 = x0 + self.CELL, y0 + self.CELL
                fill = self._cell_fill(r, c, conflicts)
                if fill:
                    self.canvas.create_rectangle(x0, y0, x1, y1,
                                                 fill=fill, outline="")
                value = self.board.get_value(r, c)
                if value != 0:
                    self.canvas.create_text(
                        x0 + self.CELL / 2, y0 + self.CELL / 2,
                        text=str(value), font=("Arial", 20, "bold"),
                        fill=self._text_color(r, c, conflicts))
    def _cell_fill(self, r, c, conflicts):
        """Pick the background color for cell (r, c)."""
        if self.selected == (r, c):
            return self.SELECT_COLOR
        if self._show_errors and (r, c) in self._error_cells:
            return self.ERROR_COLOR
        if (r, c) in conflicts:
            return self.CONFLICT_COLOR
        if self.selected is not None:
            sr, sc = self.selected
            if r == sr or c == sc or (r // 3 == sr // 3 and c // 3 == sc // 3):
                if (self.board.get_value(sr, sc) != 0
                        and self.board.get_value(r, c)
                        == self.board.get_value(sr, sc)):
                    return self.SAME_COLOR
                return self.PEER_COLOR
        return None
    def _text_color(self, r, c, conflicts):
        """Pick the digit color for cell (r, c)."""
        if self.board.is_fixed(r, c):
            return self.FIXED_COLOR
        if self._show_errors and (r, c) in self._error_cells:
            return self.ERROR_COLOR
        if (r, c) in conflicts:
            return self.ERROR_COLOR
        if (r, c) in self._hint_cells:
            return self.HINT_COLOR
        return self.USER_COLOR
    # -------------------------------------------------------------- status
    def _set_status(self, text):
        """Display a message in the status bar."""
        self.status_label.config(text=text)
    def _tick(self):
        """Update the elapsed-time label once per second."""
        if not self._game_over:
            elapsed = int(time.time() - self._start_time)
            self.time_label.config(
                text=f"Time: {elapsed // 60:02d}:{elapsed % 60:02d}")
        self.after(1000, self._tick)