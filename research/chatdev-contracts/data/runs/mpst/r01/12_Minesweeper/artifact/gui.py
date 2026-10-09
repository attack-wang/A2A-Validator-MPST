'''
gui.py
Tkinter front-end for the Minesweeper game. Renders the Board on a Canvas
with 3D beveled cells, handles left-click (reveal / chord) and right-click
(flag) input, shows the mine counter, timer, and reset button, and offers
the three difficulty levels through a menu.
'''
import tkinter as tk
from tkinter import messagebox
from game import STATE_READY, STATE_PLAYING, STATE_WON, STATE_LOST
from config import (DIFFICULTIES, MAX_TIME, BG_COLOR, CELL_UNREVEALED,
                    CELL_REVEALED, BEVEL_LIGHT, BEVEL_DARK, TEXT_COLOR,
                    FLAG_COLOR, MINE_COLOR, EXPLOSION_COLOR, NUMBER_COLORS)
FLAG_GLYPH = "\u2691"   # ⚑
MINE_GLYPH = "\u25cf"   # ●
class MinesweeperGUI:
    """Tkinter window that visualises a Game and forwards player input."""
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.root.title("Minesweeper")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        self.cell_size = self._choose_cell_size()
        self._build_menu()
        self._build_header()
        self._build_canvas()
        self._rebuild_board()
        self.redraw()
        self._tick()
    # ------------------------------------------------------------------
    # Layout construction
    # ------------------------------------------------------------------
    def _choose_cell_size(self):
        """Pick a cell size in pixels that fits the current difficulty on screen."""
        width, height, _mines = DIFFICULTIES[self.game.difficulty_name]
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        size = int(min((screen_w - 100) / width, (screen_h - 200) / height))
        return max(18, min(size, 32))
    def _build_menu(self):
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        for name in DIFFICULTIES:
            game_menu.add_command(
                label=name.capitalize(),
                command=lambda n=name: self._start_new_game(n))
        game_menu.add_separator()
        game_menu.add_command(label="New Game", command=self._reset)
        menubar.add_cascade(label="Game", menu=game_menu)
        self.root.config(menu=menubar)
    def _build_header(self):
        header = tk.Frame(self.root, bg=BG_COLOR)
        header.pack(fill="x", padx=8, pady=(6, 2))
        self.mine_label = tk.Label(header, font=("Consolas", 14, "bold"),
                                   bg=BG_COLOR, fg=TEXT_COLOR, width=6)
        self.mine_label.pack(side="left")
        self.reset_button = tk.Button(header, text="\u263a", font=("Segoe UI Symbol", 13, "bold"),
                                      width=3, bg=BG_COLOR, relief="raised",
                                      command=self._reset)
        self.reset_button.pack(side="left", expand=True)
        self.time_label = tk.Label(header, font=("Consolas", 14, "bold"),
                                   bg=BG_COLOR, fg=TEXT_COLOR, width=6)
        self.time_label.pack(side="right")
        self.status = tk.Label(self.root, text="Left-click: reveal  |  Right-click: flag",
                               bg=BG_COLOR, fg=TEXT_COLOR)
        self.status.pack(fill="x", padx=8, pady=(0, 4))
    def _build_canvas(self):
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg=BG_COLOR)
        self.canvas.pack(padx=8, pady=4)
        self.canvas.bind("<Button-1>", self._on_left_click)
        self.canvas.bind("<Button-3>", self._on_right_click)
        self.canvas.bind("<Button-2>", self._on_middle_click)
    def _rebuild_board(self):
        """Resize the canvas for the current board and refresh the header."""
        width, height, _mines = DIFFICULTIES[self.game.difficulty_name]
        self.canvas.config(width=width * self.cell_size,
                           height=height * self.cell_size)
        self.root.geometry("")
        self._update_header()
    # ------------------------------------------------------------------
    # Game control
    # ------------------------------------------------------------------
    def _reset(self):
        self.game.new_game()
        self._rebuild_board()
        self.redraw()
    def _start_new_game(self, difficulty_name):
        self.game.new_game(difficulty_name)
        self.cell_size = self._choose_cell_size()
        self._rebuild_board()
        self.redraw()
    # ------------------------------------------------------------------
    # Input handling
    # ------------------------------------------------------------------
    def _event_cell(self, event):
        """Translate a canvas click into (row, col), or None when outside."""
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if self.game.board.get_cell(row, col) is not None:
            return row, col
        return None
    def _on_left_click(self, event):
        pos = self._event_cell(event)
        if pos is None:
            return
        previous_state = self.game.state
        hit_mine, _revealed = self.game.reveal(*pos)
        self.redraw()
        if previous_state in (STATE_READY, STATE_PLAYING):
            self._announce_result(hit_mine)
    def _on_right_click(self, event):
        pos = self._event_cell(event)
        if pos is None:
            return
        self.game.toggle_flag(*pos)
        self.redraw()
    def _on_middle_click(self, event):
        pos = self._event_cell(event)
        if pos is None:
            return
        previous_state = self.game.state
        hit_mine, _revealed = self.game.reveal(*pos)
        self.redraw()
        if previous_state in (STATE_READY, STATE_PLAYING):
            self._announce_result(hit_mine)
    def _announce_result(self, hit_mine):
        if self.game.state == STATE_WON:
            self.status.config(text="You cleared the board — you win! \u263a")
            messagebox.showinfo("Minesweeper", "You cleared the board — you win!")
        elif hit_mine:
            self.status.config(text="Boom! You hit a mine — game over.")
            messagebox.showinfo("Minesweeper", "Boom! You hit a mine — game over.")
    # ------------------------------------------------------------------
    # Timer / header refresh
    # ------------------------------------------------------------------
    def _tick(self):
        self._update_header()
        self.root.after(500, self._tick)
    def _update_header(self):
        flags = sum(1 for row in self.game.board.grid
                    for cell in row if cell.is_flagged)
        self.mine_label.config(
            text="\u26a0 {:03d}".format(max(self.game.board.mine_count - flags, -99)))
        self.time_label.config(
            text="\u23f1 {:03d}".format(min(self.game.get_elapsed_seconds(), MAX_TIME)))
        if self.game.state == STATE_WON:
            self.reset_button.config(text="\u263a")
        elif self.game.state == STATE_LOST:
            self.reset_button.config(text="\u2620")
        else:
            self.reset_button.config(text="\u263a")
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def redraw(self):
        self.canvas.delete("all")
        for row in self.game.board.grid:
            for cell in row:
                self._draw_cell(cell)
        self._update_header()
    def _draw_cell(self, cell):
        x0 = cell.col * self.cell_size
        y0 = cell.row * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        if cell.is_revealed:
            self._draw_revealed(x0, y0, x1, y1, cell)
        elif cell.is_flagged:
            self._draw_raised(x0, y0, x1, y1)
            if self.game.state == STATE_LOST and not cell.is_mine:
                self._draw_mine(x0, y0, x1, y1)
                self._draw_wrong_flag_mark(x0, y0, x1, y1)
            else:
                self._draw_flag(x0, y0, x1, y1)
        else:
            self._draw_raised(x0, y0, x1, y1)
            if self.game.state == STATE_LOST and cell.is_mine:
                if self.game.lost_cell == (cell.row, cell.col):
                    self.canvas.create_rectangle(x0, y0, x1, y1,
                                                 fill=EXPLOSION_COLOR,
                                                 outline=BEVEL_DARK)
                self._draw_mine(x0, y0, x1, y1)
    def _draw_revealed(self, x0, y0, x1, y1, cell):
        fill = CELL_REVEALED
        if cell.is_mine and self.game.state == STATE_LOST:
            if self.game.lost_cell == (cell.row, cell.col):
                fill = EXPLOSION_COLOR
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill,
                                     outline=BEVEL_DARK)
        if cell.is_mine and self.game.state in (STATE_LOST, STATE_WON):
            self._draw_mine(x0, y0, x1, y1)
        elif cell.adjacent_mines:
            color = NUMBER_COLORS.get(cell.adjacent_mines, TEXT_COLOR)
            self.canvas.create_text(
                (x0 + x1) // 2, (y0 + y1) // 2,
                text=str(cell.adjacent_mines),
                font=("Consolas", max(10, self.cell_size - 12), "bold"),
                fill=color)
    def _draw_raised(self, x0, y0, x1, y1):
        """Draw a hidden cell with a 3D bevel (light top-left, dark bottom-right)."""
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=CELL_UNREVEALED,
                                     outline=BEVEL_DARK)
        b = max(2, self.cell_size // 8)
        # top-left highlight
        self.canvas.create_line(x0, y0, x1, y0, fill=BEVEL_LIGHT, width=b)
        self.canvas.create_line(x0, y0, x0, y1, fill=BEVEL_LIGHT, width=b)
        # bottom-right shadow
        self.canvas.create_line(x0, y1, x1, y1, fill=BEVEL_DARK, width=b)
        self.canvas.create_line(x1, y0, x1, y1, fill=BEVEL_DARK, width=b)
    def _draw_flag(self, x0, y0, x1, y1):
        self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2,
                                text=FLAG_GLYPH,
                                font=("Segoe UI Symbol", max(10, self.cell_size - 8), "bold"),
                                fill=FLAG_COLOR)
    def _draw_mine(self, x0, y0, x1, y1):
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        r = max(3, self.cell_size // 4)
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                fill=MINE_COLOR, outline=MINE_COLOR)
        self.canvas.create_line(cx - r, cy, cx + r, cy, fill=MINE_COLOR)
        self.canvas.create_line(cx, cy - r, cx, cy + r, fill=MINE_COLOR)
    def _draw_wrong_flag_mark(self, x0, y0, x1, y1):
        self.canvas.create_line(x0 + 3, y0 + 3, x1 - 3, y1 - 3, fill="red", width=2)
        self.canvas.create_line(x1 - 3, y0 + 3, x0 + 3, y1 - 3, fill="red", width=2)
    # ------------------------------------------------------------------
    # Event loop
    # ------------------------------------------------------------------
    def run(self):
        self.root.mainloop()