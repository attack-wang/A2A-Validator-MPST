'''
gui.py
Tkinter front-end for the Minesweeper game.
Provides the difficulty menu, the Canvas-based board rendering,
mouse interaction (left-click = reveal, right-click = flag),
a status bar with mine counter and timer, and game-over dialogs.
'''
import time
import tkinter as tk
from tkinter import messagebox
from config import DIFFICULTY_LEVELS
from game_logic import MinesweeperGame, STATE_PLAYING, STATE_WON, STATE_LOST
CELL_SIZE = 32
FONT = ("Arial", 14, "bold")
STATUS_FONT = ("Arial", 12, "bold")
MINE_SYMBOL = "\N{BLACK CIRCLE}"      # ●
FLAG_SYMBOL = "\N{BLACK FLAG}"        # ⚑ (distinct visual for flagged cells)
NUMBER_COLORS = {1: "#0000FF", 2: "#008000", 3: "#FF0000", 4: "#000080",
                 5: "#800000", 6: "#008080", 7: "#000000", 8: "#808080"}
class MinesweeperGUI:
    """Tkinter controller rendering a MinesweeperGame and handling input."""
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.resizable(False, False)
        self.game = None
        self.canvas = None
        self._timer_id = None
        self._start_time = None
        self.elapsed = 0
        self._build_menu()
        self._build_status_bar()
        self.new_game("Beginner")  # default difficulty
    def _build_menu(self):
        """Menu bar: New Game, Exit, and the 3 difficulty presets."""
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game", command=self._restart)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="Game", menu=game_menu)
        diff_menu = tk.Menu(menubar, tearoff=0)
        for name in DIFFICULTY_LEVELS:
            diff_menu.add_command(label=name,
                                  command=lambda n=name: self.new_game(n))
        menubar.add_cascade(label="Difficulty", menu=diff_menu)
        self.root.config(menu=menubar)
    def _build_status_bar(self):
        """Status bar showing remaining mines and elapsed time."""
        self.status_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE)
        self.status_frame.pack(fill=tk.X, padx=4, pady=4)
        self.mines_label = tk.Label(self.status_frame, text="Mines: 0",
                                    font=STATUS_FONT, fg="#CC0000")
        self.mines_label.pack(side=tk.LEFT, padx=8)
        self.time_label = tk.Label(self.status_frame, text="Time: 0",
                                   font=STATUS_FONT)
        self.time_label.pack(side=tk.RIGHT, padx=8)
    def _build_board(self):
        """(Re)create the Canvas for the current board dimensions."""
        if self.canvas is not None:
            self.canvas.destroy()
        self.canvas = tk.Canvas(self.root,
                                width=self.game.cols * CELL_SIZE,
                                height=self.game.rows * CELL_SIZE,
                                bd=0, highlightthickness=1,
                                highlightbackground="#808080")
        self.canvas.pack(padx=4, pady=4)
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Button-2>", self.on_right_click)  # macOS
    def new_game(self, difficulty_name):
        """Start a fresh game with the selected difficulty."""
        self._stop_timer()
        self.game = MinesweeperGame(DIFFICULTY_LEVELS[difficulty_name])
        self.elapsed = 0
        self._build_board()
        self.draw_board()
        self._update_status_bar()
    def _restart(self):
        """Restart the current difficulty."""
        if self.game is not None:
            self.new_game(self.game.config.name)
    def _event_to_cell(self, event):
        """Convert a canvas click into (row, col); None if outside the grid."""
        col = int(self.canvas.canvasx(event.x)) // CELL_SIZE
        row = int(self.canvas.canvasy(event.y)) // CELL_SIZE
        if 0 <= row < self.game.rows and 0 <= col < self.game.cols:
            return row, col
        return None
    def on_left_click(self, event):
        """Left-click: uncover the cell (starts timer on the first move)."""
        if self.game.state != STATE_PLAYING:
            return
        pos = self._event_to_cell(event)
        if pos is None:
            return
        if not self.game.mines_placed:
            self._start_timer()
        self.game.reveal_cell(*pos)
        self.draw_board()
        self._update_status_bar()
        self._check_game_end()
    def on_right_click(self, event):
        """Right-click: toggle a flag on the cell."""
        if self.game.state != STATE_PLAYING:
            return
        pos = self._event_to_cell(event)
        if pos is None:
            return
        self.game.toggle_flag(*pos)
        self.draw_board()
        self._update_status_bar()
    def draw_board(self):
        """Render every cell — called after every move so markings update."""
        self.canvas.delete(tk.ALL)
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                self.draw_cell(r, c)
    def draw_cell(self, row, col):
        """Render one cell according to its state (hidden/revealed/flagged)."""
        cell = self.game.get_cell(row, col)
        x1, y1 = col * CELL_SIZE, row * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        bg, fg, text = "#C0C0C0", "#000000", ""
        if cell.is_revealed:
            if cell.is_mine:
                bg = "#FF5A5A" if cell.is_exploded else "#E8E8E8"
                fg, text = "#000000", MINE_SYMBOL
            else:
                bg = "#E8E8E8"
                if cell.adjacent_mines > 0:
                    text = str(cell.adjacent_mines)
                    fg = NUMBER_COLORS.get(cell.adjacent_mines, "#000000")
        elif cell.is_flagged:
            if self.game.state == STATE_LOST and not cell.is_mine:
                bg, fg, text = "#FF9999", "#000000", "✗"  # wrong flag
            else:
                bg, fg, text = "#FFD966", "#CC0000", FLAG_SYMBOL
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg, outline="#808080")
        if text:
            self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2,
                                    text=text, font=FONT, fill=fg)
    def _update_status_bar(self):
        """Refresh mine counter and timer labels."""
        self.mines_label.config(text=f"Mines: {self.game.remaining_mines()}")
        self.time_label.config(text=f"Time: {self.elapsed}")
    def _start_timer(self):
        """Begin counting seconds from the first reveal."""
        self._start_time = time.time()
        self._tick()
    def _tick(self):
        """Periodic callback refreshing the elapsed-time display."""
        if self.game is None or self.game.state != STATE_PLAYING:
            return
        self.elapsed = int(time.time() - self._start_time)
        self.time_label.config(text=f"Time: {self.elapsed}")
        self._timer_id = self.root.after(1000, self._tick)
    def _stop_timer(self):
        """Cancel the periodic timer callback, if running."""
        if self._timer_id is not None:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None
    def _check_game_end(self):
        """Show a dialog when the game is won or lost."""
        if self.game.state == STATE_WON:
            self._stop_timer()
            messagebox.showinfo("Minesweeper",
                                f"You cleared the board in {self.elapsed} seconds!\n"
                                "Play again?")
            self._restart()
        elif self.game.state == STATE_LOST:
            self._stop_timer()
            messagebox.showinfo("Minesweeper", "Boom! You hit a mine.\n"
                                "Better luck next time!")
            self._restart()