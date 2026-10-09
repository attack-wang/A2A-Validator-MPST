'''
Tkinter front-end for the Minesweeper game.
Renders the board on a Canvas, handles left-click (reveal),
right-click (flag) and middle-click / double-click (chord) input,
and displays the mine counter, timer and a smiley reset button.
'''
import tkinter as tk
from tkinter import messagebox
from game_logic import Board
DIFFICULTIES = {
    "Beginner": {"rows": 9, "cols": 9, "mines": 10},
    "Intermediate": {"rows": 16, "cols": 16, "mines": 40},
    "Expert": {"rows": 16, "cols": 30, "mines": 99},
}
CELL_SIZE = 30
NUMBER_COLORS = {
    1: "#0000FF",
    2: "#008000",
    3: "#FF0000",
    4: "#000080",
    5: "#800000",
    6: "#008080",
    7: "#000000",
    8: "#808080",
}
COVERED_FILL = "#C0C0C0"
COVERED_LIGHT = "#FFFFFF"
COVERED_DARK = "#7B7B7B"
REVEALED_FILL = "#E3E3E3"
REVEALED_OUTLINE = "#A8A8A8"
MINE_BG = "#B0B0B0"
EXPLODED_BG = "#FF5A4E"
FLAG_COLOR = "#CC0000"
FLAG_GLYPH = "\u2691"   # ⚑
MINE_GLYPH = "\u2738"   # ✸
WRONG_GLYPH = "\u2717"  # ✗
SMILEY_PLAY = "\U0001F642"  # 🙂
SMILEY_OOH = "\U0001F62E"   # 😮
SMILEY_WIN = "\U0001F60E"   # 😎
SMILEY_LOSE = "\U0001F635"  # 😵
class MinesweeperGUI:
    """Main application window: menu, status bar and board canvas."""
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.resizable(False, False)
        self.difficulty = "Beginner"
        self.board = None
        self.canvas = None
        self.elapsed = 0
        self.timer_id = None
        self.timer_running = False
        self.game_ended = False
        self._press_cell = None  # cell where the last left press happened
        self._build_menu()
        self._build_status_bar()
        self._build_board_frame()
        self.new_game("Beginner")
    # ------------------------------------------------------------------ UI setup
    def _build_menu(self):
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game", accelerator="F2",
                              command=lambda: self.new_game(self.difficulty))
        game_menu.add_separator()
        self._difficulty_var = tk.StringVar(value=self.difficulty)
        for name in DIFFICULTIES:
            game_menu.add_radiobutton(label=name, variable=self._difficulty_var,
                                      value=name, command=lambda n=name: self.new_game(n))
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="Game", menu=game_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="How to play", command=self._show_help)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)
        self.root.bind("<F2>", lambda e: self.new_game(self.difficulty))
    def _build_status_bar(self):
        bar = tk.Frame(self.root, bd=2, relief="groove")
        bar.pack(fill="x", padx=6, pady=(6, 3))
        self.mine_label = tk.Label(bar, text="010", font=("Consolas", 16, "bold"),
                                   fg="#FF0000", bg="#000000", width=4, anchor="center")
        self.mine_label.pack(side="left", padx=4, pady=2)
        self.smiley = tk.Button(bar, text=SMILEY_PLAY, font=("Segoe UI Emoji", 14),
                                width=3, command=self._restart)
        self.smiley.pack(side="left", padx=8, pady=2)
        self.timer_label = tk.Label(bar, text="000", font=("Consolas", 16, "bold"),
                                    fg="#FF0000", bg="#000000", width=4, anchor="center")
        self.timer_label.pack(side="right", padx=4, pady=2)
    def _build_board_frame(self):
        self.board_frame = tk.Frame(self.root, bd=3, relief="sunken",
                                    bg=COVERED_FILL)
        self.board_frame.pack(padx=6, pady=(3, 6))
    def _rebuild_canvas(self):
        """(Re)create the board canvas with the size of the current board."""
        if self.canvas is not None:
            self.canvas.destroy()
        width = self.board.cols * CELL_SIZE
        height = self.board.rows * CELL_SIZE
        self.canvas = tk.Canvas(self.board_frame, width=width, height=height,
                                highlightthickness=0, bg=COVERED_FILL)
        self.canvas.pack()
        # NOTE: <Button-1> is an alias of <ButtonPress-1>; binding both would
        # overwrite one binding, so the press/release pair is used instead.
        self.canvas.bind("<ButtonPress-1>", self._on_mouse_press)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_release)
        self.canvas.bind("<Button-2>", self._on_chord_click)          # mac right / middle
        self.canvas.bind("<Button-3>", self._on_right_click)
        self.canvas.bind("<Control-Button-1>", self._on_right_click)  # mac ctrl-click flag
        self.canvas.bind("<Double-Button-1>", self._on_chord_click)
    # ------------------------------------------------------------------ game flow
    def new_game(self, difficulty):
        """Start a fresh game on the requested difficulty."""
        self.difficulty = difficulty
        self._difficulty_var.set(difficulty)
        self._stop_timer()
        self.elapsed = 0
        self.game_ended = False
        self._press_cell = None
        spec = DIFFICULTIES[difficulty]
        self.board = Board(spec["rows"], spec["cols"], spec["mines"])
        self._rebuild_canvas()
        self._redraw()
        self._update_status()
        self.smiley.config(text=SMILEY_PLAY)
    def _restart(self):
        """Restart the current difficulty (smiley button)."""
        self.new_game(self.difficulty)
    def _reveal_action(self, row, col):
        """Reveal a cell, start the timer on the first move and refresh UI."""
        hit = self.board.reveal_cell(row, col)
        if self.board.mines_placed and not self.timer_running and not self.board.game_over:
            self._start_timer()
        self._after_move()
        return hit
    def _after_move(self):
        """Refresh the board and status bar, then handle game end."""
        self._redraw()
        self._update_status()
        if self.board.game_over and not self.game_ended:
            self._end_game(self.board.won)
    def _end_game(self, won):
        """Stop the timer, update the smiley and inform the player."""
        self.game_ended = True
        self._stop_timer()
        if won:
            self.smiley.config(text=SMILEY_WIN)
            messagebox.showinfo(
                "Minesweeper",
                f"You cleared the board in {self.elapsed} seconds!\n"
                "Click the smiley or press F2 to play again.")
        else:
            self.smiley.config(text=SMILEY_LOSE)
            messagebox.showerror(
                "Minesweeper",
                "Boom! You uncovered a mine.\n"
                "Click the smiley or press F2 to try again.")
    def _show_help(self):
        messagebox.showinfo(
            "How to play",
            "Goal: uncover every cell that has no mine.\n\n"
            "Left-click: uncover a cell.\n"
            "Right-click (or Ctrl+click on macOS): place/remove a flag.\n"
            "Middle-click / double-click a number: reveal its neighbours when\n"
            "the matching number of flags is placed around it (chording).\n\n"
            "Numbers show how many mines touch that cell.\n"
            "Uncovering a mine loses the game. F2 starts a new game.")
    # ------------------------------------------------------------------ timer
    def _start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self._tick()
    def _stop_timer(self):
        self.timer_running = False
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    def _tick(self):
        if not self.timer_running:
            return
        self.elapsed += 1
        self._update_status()
        self.timer_id = self.root.after(1000, self._tick)
    # ------------------------------------------------------------------ status / drawing
    def _update_status(self):
        """Refresh the mine counter and the timer read-out."""
        remaining = max(self.board.total_mines - self.board.flag_count, 0)
        self.mine_label.config(text=f"{remaining:03d}")
        self.timer_label.config(text=f"{min(self.elapsed, 999):03d}")
    def _redraw(self):
        """Redraw every cell on the canvas."""
        self.canvas.delete("all")
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                self._draw_cell(r, c)
    def _draw_cell(self, row, col):
        """Paint a single cell according to its current state."""
        cell = self.board.cells[row][col]
        x0, y0 = col * CELL_SIZE, row * CELL_SIZE
        x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
        lost = self.board.game_over and not self.board.won
        if cell.is_revealed:
            bg = EXPLODED_BG if cell.is_mine else REVEALED_FILL
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg,
                                         outline=REVEALED_OUTLINE)
            if cell.is_mine:
                self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2,
                                        text=MINE_GLYPH,
                                        font=("Segoe UI Symbol", 14))
            elif cell.adjacent_mines:
                self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2,
                                        text=str(cell.adjacent_mines),
                                        fill=NUMBER_COLORS[cell.adjacent_mines],
                                        font=("Consolas", 14, "bold"))
        else:
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=COVERED_FILL,
                                         outline=COVERED_DARK)
            self.canvas.create_line(x0, y0, x1, y0, fill=COVERED_LIGHT)
            self.canvas.create_line(x0, y0, x0, y1, fill=COVERED_LIGHT)
            self.canvas.create_line(x0 + 1, y1 - 1, x1 - 1, y1 - 1, fill=COVERED_DARK)
            self.canvas.create_line(x1 - 1, y0 + 1, x1 - 1, y1 - 1, fill=COVERED_DARK)
            if cell.is_flagged:
                glyph, color = (WRONG_GLYPH, "#000000") if (lost and not cell.is_mine) \
                               else (FLAG_GLYPH, FLAG_COLOR)
                self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=glyph,
                                        fill=color, font=("Segoe UI Symbol", 14))
            elif cell.is_mine and lost:   # reveal all mines on loss
                self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2,
                                        text=MINE_GLYPH,
                                        font=("Segoe UI Symbol", 14))
    # ------------------------------------------------------------------ input
    def _cell_at(self, event):
        """Map a canvas event position to a (row, col) cell, or None."""
        if self.board is None:
            return None
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if self.board.in_bounds(row, col):
            return row, col
        return None
    def _on_mouse_press(self, event):
        """Left press: remember the cell and show the 'ooh' smiley."""
        self._press_cell = self._cell_at(event)
        if not self.board.game_over:
            self.smiley.config(text=SMILEY_OOH)
    def _on_mouse_release(self, event):
        """Left release: restore the smiley and reveal the pressed cell."""
        cell = self._cell_at(event)
        if not self.board.game_over:
            self.smiley.config(text=SMILEY_PLAY)
        if (cell is not None and cell == self._press_cell
                and not self.board.game_over):
            self._reveal_action(*cell)
        self._press_cell = None
    def _on_right_click(self, event):
        """Right click: toggle a flag on the clicked cell."""
        cell = self._cell_at(event)
        if cell is None or self.board.game_over:
            return
        if self.board.toggle_flag(*cell):
            self._redraw()
            self._update_status()
    def _on_chord_click(self, event):
        """Middle click / double click: chord on a revealed number cell."""
        cell = self._cell_at(event)
        if cell is None or self.board.game_over:
            return
        if self.board.cells[cell[0]][cell[1]].is_revealed:
            self._reveal_action_chord(cell)
    def _reveal_action_chord(self, cell):
        hit = self.board.chord(*cell)
        if self.board.mines_placed and not self.timer_running and not self.board.game_over:
            self._start_timer()
        self._after_move()
        return hit