'''
sudoku_gui.py
Tkinter-based graphical front-end for the Sudoku game.
Provides cell selection (mouse + arrow keys), digit entry, real-time
conflict highlighting, mistake tracking, hints, and completion
confirmation.
'''
import random
import tkinter as tk
from tkinter import messagebox, ttk
from sudoku_logic import SudokuBoard
from sudokugenerator import SudokuGenerator
# Colors
BG_COLOR = "#ffffff"
GIVEN_BG = "#f0f0f0"
SELECTED_BG = "#ffe066"
PEER_BG = "#fff3bf"
SAME_BG = "#cfe8ff"
CONFLICT_COLOR = "#e03131"
GIVEN_TEXT = "#1a1a1a"
USER_TEXT = "#1c64d9"
HINT_TEXT = "#2f9e44"
CELL_SIZE = 56
BOARD_PX = CELL_SIZE * 9
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.resizable(False, False)
        self.board = SudokuBoard()
        self.generator = SudokuGenerator()
        self.selected = None  # (row, col) or None
        self.mistakes = 0
        self.elapsed = 0
        self.timer_running = False
        self.game_over = False
        self.hinted = set()  # cells revealed by Hint
        self._timer_job = None
        self._build_menu_bar()
        self._build_top_bar()
        self._build_canvas()
        self._build_bottom_bar()
        self.root.bind("<Key>", self.on_key)
        self.new_game("Easy")
    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_menu_bar(self):
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(
            label="New Game",
            command=lambda: self.new_game(self.difficulty_var.get()),
        )
        game_menu.add_command(label="Restart Puzzle", command=self.restart_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="Game", menu=game_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="How to Play", command=self.show_help)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)
    def _build_top_bar(self):
        top = tk.Frame(self.root)
        top.pack(fill="x", padx=10, pady=(8, 0))
        self.difficulty_var = tk.StringVar(value="Easy")
        ttk.Combobox(
            top,
            textvariable=self.difficulty_var,
            values=list(self.generator.DIFFICULTY_LEVELS.keys()),
            width=8,
            state="readonly",
        ).pack(side="left")
        tk.Button(top, text="New Game",
                  command=lambda: self.new_game(self.difficulty_var.get())).pack(side="left", padx=6)
        self.timer_label = tk.Label(top, text="00:00", font=("Arial", 11, "bold"))
        self.timer_label.pack(side="right")
        self.mistakes_label = tk.Label(top, text="Mistakes: 0")
        self.mistakes_label.pack(side="right", padx=10)
    def _build_canvas(self):
        self.canvas = tk.Canvas(
            self.root, width=BOARD_PX, height=BOARD_PX,
            bg=BG_COLOR, highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=5)
        self.canvas.bind("<Button-1>", self.on_click)
        self._draw_grid_lines()
    def _build_bottom_bar(self):
        bottom = tk.Frame(self.root)
        bottom.pack(fill="x", padx=10, pady=(0, 10))
        tk.Button(bottom, text="Check", command=self.on_check).pack(side="left")
        tk.Button(bottom, text="Hint", command=self.on_hint).pack(side="left", padx=6)
        tk.Button(bottom, text="Erase", command=self.on_erase).pack(side="left")
        self.status_label = tk.Label(bottom, text="", anchor="w")
        self.status_label.pack(side="left", padx=12, fill="x", expand=True)
    def _draw_grid_lines(self):
        for i in range(10):
            width = 3 if i % 3 == 0 else 1
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, BOARD_PX, width=width)
            self.canvas.create_line(0, i * CELL_SIZE, BOARD_PX, i * CELL_SIZE, width=width)
    # ------------------------------------------------------------------
    # Game flow
    # ------------------------------------------------------------------
    def new_game(self, difficulty="Easy"):
        """Generate a fresh puzzle and reset all game state."""
        puzzle, solution = self.generator.generate(difficulty)
        self.board.load_puzzle(puzzle, solution)
        self.selected = None
        self.mistakes = 0
        self.elapsed = 0
        self.game_over = False
        self.hinted = set()
        self.timer_running = True
        self.difficulty_var.set(difficulty)
        self._update_status_labels()
        self.redraw_board()
        self.set_status(f"New {difficulty} puzzle started. Good luck!")
        self._schedule_tick()
    def restart_game(self):
        """Clear all user entries and replay the same puzzle."""
        for r in range(9):
            for c in range(9):
                if not self.board.is_given(r, c):
                    self.board.clear_value(r, c)
        self.mistakes = 0
        self.hinted = set()
        self.game_over = False
        self.timer_running = True
        self._update_status_labels()
        self.redraw_board()
        self.set_status("Puzzle restarted — same board, fresh start.")
    def _schedule_tick(self):
        if self._timer_job is not None:
            self.root.after_cancel(self._timer_job)
        self._tick()
    def _tick(self):
        if self.timer_running and not self.game_over:
            self.elapsed += 1
            self.timer_label.config(text=self._format_time(self.elapsed))
        self._timer_job = self.root.after(1000, self._tick)
    @staticmethod
    def _format_time(seconds):
        return f"{seconds // 60:02d}:{seconds % 60:02d}"
    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------
    def on_click(self, event):
        if self.game_over:
            return
        col, row = event.x // CELL_SIZE, event.y // CELL_SIZE
        if self.board.in_bounds(row, col):
            self.selected = (row, col)
            self.redraw_board()
    def on_key(self, event):
        if self.game_over:
            return
        key = event.keysym
        if key in ("Up", "Down", "Left", "Right"):
            self._move_selection(key)
            return
        if key == "Escape":
            self.selected = None
            self.redraw_board()
            return
        if key in ("Delete", "BackSpace"):
            if self.selected:
                self._erase_selected()
            return
        char = event.char
        if char and char.isdigit() and char != "0":
            if self.selected:
                self._enter_value(self.selected[0], self.selected[1], int(char))
            else:
                self.set_status("Select a cell first (click or use arrow keys).")
    def _move_selection(self, direction):
        if not self.selected:
            self.selected = (0, 0)
        else:
            r, c = self.selected
            dr, dc = {"Up": (-1, 0), "Down": (1, 0),
                      "Left": (0, -1), "Right": (0, 1)}[direction]
            self.selected = (max(0, min(8, r + dr)), max(0, min(8, c + dc)))
        self.redraw_board()
    def _enter_value(self, row, col, value):
        if self.board.is_given(row, col):
            self.set_status("That cell is fixed — choose an empty cell.")
            return
        self.board.set_value(row, col, value)
        self.hinted.discard((row, col))
        if not self.board.is_valid_placement(row, col, value):
            self.mistakes += 1
            self._update_status_labels()
            self.set_status(f"{value} conflicts with an existing number.")
        else:
            self.set_status("")
        self.redraw_board()
        if self.board.is_complete():
            self._finish_game()
    def _erase_selected(self):
        row, col = self.selected
        if self.board.is_given(row, col):
            self.set_status("That cell is fixed and cannot be erased.")
            return
        self.board.clear_value(row, col)
        self.hinted.discard((row, col))
        self.redraw_board()
    def on_erase(self):
        if self.game_over:
            return
        if not self.selected:
            self.set_status("Select a cell to erase.")
            return
        self._erase_selected()
    def on_check(self):
        """Verify the player's entries against the solution and rules."""
        if self.board.is_complete():
            self._finish_game()
            return
        conflicts = self.board.find_conflicts()
        wrong = self.board.count_mistakes()
        empty = 81 - self.board.count_filled()
        message = f"Empty cells: {empty}."
        if wrong:
            message += f" {wrong} entr{'y' if wrong == 1 else 'ies'} differ from the solution."
        if conflicts:
            message += f" {len(conflicts)} cell(s) in conflict (shown in red)."
        if not wrong and not conflicts:
            message += " No mistakes so far — keep going!"
        messagebox.showinfo("Check", message)
    def on_hint(self):
        """Reveal the correct value for the selected (or a random) cell."""
        if self.game_over:
            return
        target = None
        if self.selected:
            r, c = self.selected
            if not self.board.is_given(r, c) and self.board.get_value(r, c) != self.board.solution[r][c]:
                target = (r, c)
        if target is None:
            empties = [
                (r, c) for r in range(9) for c in range(9)
                if not self.board.is_given(r, c)
                and self.board.get_value(r, c) != self.board.solution[r][c]
            ]
            if empties:
                target = random.choice(empties)
        if target is None:
            self.set_status("Nothing left to hint — the board matches the solution.")
            return
        r, c = target
        self.board.set_value(r, c, self.board.solution[r][c])
        self.hinted.add((r, c))
        self.selected = (r, c)
        self.redraw_board()
        if self.board.is_complete():
            self._finish_game()
    def _finish_game(self):
        """Confirm completion: stop the timer and congratulate the player."""
        self.game_over = True
        self.timer_running = False
        self.selected = None
        self.redraw_board()
        messagebox.showinfo(
            "Sudoku Solved!",
            f"Congratulations! Puzzle completed in {self._format_time(self.elapsed)} "
            f"with {self.mistakes} mistake(s).",
        )
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def redraw_board(self):
        self.canvas.delete("all")
        self._draw_grid_lines()
        conflicts = self.board.find_conflicts()
        sel = self.selected
        sel_value = self.board.get_value(*sel) if sel else 0
        for r in range(9):
            for c in range(9):
                value = self.board.get_value(r, c)
                x0, y0 = c * CELL_SIZE, r * CELL_SIZE
                bg = BG_COLOR
                if sel:
                    sr, sc = sel
                    if (r, c) == sel:
                        bg = SELECTED_BG
                    elif r == sr or c == sc or (r // 3 == sr // 3 and c // 3 == sc // 3):
                        bg = PEER_BG
                    if value != 0 and value == sel_value and (r, c) != sel:
                        bg = SAME_BG
                self.canvas.create_rectangle(
                    x0, y0, x0 + CELL_SIZE, y0 + CELL_SIZE,
                    fill=bg, width=0,
                )
                if value != 0:
                    if (r, c) in conflicts:
                        color = CONFLICT_COLOR
                    elif self.board.is_given(r, c):
                        color = GIVEN_TEXT
                    elif (r, c) in self.hinted:
                        color = HINT_TEXT
                    else:
                        color = USER_TEXT
                    self.canvas.create_text(
                        x0 + CELL_SIZE // 2, y0 + CELL_SIZE // 2,
                        text=str(value), font=("Arial", 22, "bold"), fill=color,
                    )
        if sel:
            sr, sc = sel
            self.canvas.create_rectangle(
                sc * CELL_SIZE, sr * CELL_SIZE,
                (sc + 1) * CELL_SIZE, (sr + 1) * CELL_SIZE,
                outline=CONFLICT_COLOR, width=2,
            )
    # ------------------------------------------------------------------
    # Misc
    # ------------------------------------------------------------------
    def set_status(self, text):
        self.status_label.config(text=text)
    def _update_status_labels(self):
        self.mistakes_label.config(text=f"Mistakes: {self.mistakes}")
        self.timer_label.config(text=self._format_time(self.elapsed))
    def show_help(self):
        messagebox.showinfo(
            "How to Play",
            "Fill the 9x9 grid so that every row, every column and every 3x3 box\n"
            "contains the digits 1-9 exactly once.\n\n"
            "• Click a cell (or use the arrow keys) to select it.\n"
            "• Press 1-9 to place a digit; Backspace/Delete clears it.\n"
            "• Conflicting numbers are shown in red immediately.\n"
            "• Use Check to verify your entries against the solution,\n"
            "  Hint to reveal a cell, and New Game to start over."
        )