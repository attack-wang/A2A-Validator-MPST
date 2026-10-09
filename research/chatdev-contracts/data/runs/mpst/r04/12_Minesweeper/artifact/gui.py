'''
gui.py
Tkinter front-end for the Minesweeper game: menu bar, status bar (mine
counter, smiley reset button, timer), canvas board rendering, mouse
controls (left-click reveal, right-click flag, middle-click chord), and
win/loss handling. Fully consolidated GameGUI class.
'''
import tkinter as tk
from tkinter import messagebox
from board import Board
from config import DIFFICULTY_SETTINGS, CELL_SIZE, NUMBER_COLORS
class GameGUI:
    """Main application window: renders the board and handles player input."""
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.master.resizable(False, False)
        self.difficulty = "Beginner"
        self.board = None
        self.timer_id = None
        self.elapsed_time = 0
        self.game_started = False
        self._build_menu()
        self._build_status_bar()
        self._build_canvas()
        self.new_game("Beginner")
    def _build_menu(self):
        menubar = tk.Menu(self.master)
        game_menu = tk.Menu(menubar, tearoff=0)
        for name in DIFFICULTY_SETTINGS:
            game_menu.add_command(label=name, command=lambda n=name: self.new_game(n))
        game_menu.add_separator()
        game_menu.add_command(label="New Game", command=lambda: self.new_game(self.difficulty))
        game_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="Game", menu=game_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="How to Play", command=self._show_help)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.master.config(menu=menubar)
    def _build_status_bar(self):
        self.status_frame = tk.Frame(self.master, bd=3, relief=tk.SUNKEN)
        self.mines_label = tk.Label(self.status_frame, text="010",
                                    font=("Consolas", 16, "bold"), fg="red", bg="black", width=4)
        self.smiley_button = tk.Button(self.status_frame, text="🙂",
                                       font=("Segoe UI Emoji", 12), width=3,
                                       command=lambda: self.new_game(self.difficulty))
        self.timer_label = tk.Label(self.status_frame, text="000",
                                    font=("Consolas", 16, "bold"), fg="red", bg="black", width=4)
        self.mines_label.pack(side=tk.LEFT, padx=6, pady=3)
        self.smiley_button.pack(side=tk.LEFT, expand=True)
        self.timer_label.pack(side=tk.RIGHT, padx=6, pady=3)
        self.status_frame.pack(side=tk.TOP, fill=tk.X)
    def _build_canvas(self):
        self.canvas = tk.Canvas(self.master, bg="#c0c0c0", highlightthickness=0)
        self.canvas.pack(side=tk.TOP)
        self.canvas.bind("<Button-1>", self._on_left_click)
        self.canvas.bind("<Button-3>", self._on_right_click)
        self.canvas.bind("<Button-2>", self._on_middle_click)
    def new_game(self, difficulty):
        self.difficulty = difficulty
        settings = DIFFICULTY_SETTINGS[difficulty]
        self.board = Board(settings["rows"], settings["cols"], settings["mines"])
        self._stop_timer()
        self.elapsed_time = 0
        self.game_started = False
        self.smiley_button.config(text="🙂")
        self.timer_label.config(text="000")
        self.canvas.config(width=self.board.cols * CELL_SIZE, height=self.board.rows * CELL_SIZE)
        self._refresh()
    def _start_timer(self):
        self._tick()
    def _tick(self):
        self.elapsed_time += 1
        self.timer_label.config(text=f"{min(self.elapsed_time, 999):03d}")
        self.timer_id = self.master.after(1000, self._tick)
    def _stop_timer(self):
        if self.timer_id is not None:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None
    def _pos(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if self.board and 0 <= row < self.board.rows and 0 <= col < self.board.cols:
            return row, col
        return None
    def _on_left_click(self, event):
        pos = self._pos(event)
        if pos is None or self.board.game_over:
            return
        if not self.game_started:
            self.game_started = True
            self._start_timer()
        self.board.reveal_cell(*pos)
        self._refresh()
        self._check_end()
    def _on_right_click(self, event):
        pos = self._pos(event)
        if pos is None or self.board.game_over:
            return
        if not self.game_started:
            self.game_started = True
            self._start_timer()
        self.board.toggle_flag(*pos)
        self._refresh()
    def _on_middle_click(self, event):
        pos = self._pos(event)
        if pos is None or self.board.game_over:
            return
        self.board.chord(*pos)
        self._refresh()
        self._check_end()
    def _refresh(self):
        self.canvas.delete(tk.ALL)
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                self._draw_cell(r, c)
        remaining = max(self.board.mine_count - self.board.count_flags(), 0)
        self.mines_label.config(text=f"{min(remaining, 999):03d}")
    def _draw_cell(self, row, col):
        cell = self.board.get_cell(row, col)
        x1, y1 = col * CELL_SIZE, row * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        mx, my = x1 + CELL_SIZE // 2, y1 + CELL_SIZE // 2
        if cell.is_revealed:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#c0c0c0", outline="#808080")
            if cell.is_mine:
                self.canvas.create_text(mx, my, text="💣", font=("Segoe UI Emoji", 12))
            elif cell.adjacent_mines > 0:
                color = NUMBER_COLORS.get(cell.adjacent_mines, "#000000")
                self.canvas.create_text(mx, my, text=str(cell.adjacent_mines),
                                        fill=color, font=("Arial", 12, "bold"))
        else:
            self.canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                                         fill="#c0c0c0", outline="#808080")
            self.canvas.create_line(x1 + 1, y1 + 1, x2 - 1, y1 + 1, fill="#ffffff")
            self.canvas.create_line(x1 + 1, y1 + 1, x1 + 1, y2 - 1, fill="#ffffff")
            self.canvas.create_line(x2 - 1, y2 - 1, x1 + 1, y2 - 1, fill="#808080")
            self.canvas.create_line(x2 - 1, y2 - 1, x2 - 1, y1 + 1, fill="#808080")
            if cell.is_flagged:
                self.canvas.create_text(mx, my, text="🚩", font=("Segoe UI Emoji", 12))
    def _check_end(self):
        if self.board.game_over:
            self._stop_timer()
            if self.board.game_won:
                self.smiley_button.config(text="😎")
                messagebox.showinfo("Minesweeper", f"You won in {self.elapsed_time} seconds!")
            else:
                self.smiley_button.config(text="😵")
                messagebox.showerror("Minesweeper", "Boom! You hit a mine. Game over.")
    def _show_help(self):
        messagebox.showinfo(
            "How to Play",
            "Goal: reveal all safe cells without uncovering any mine.\n\n"
            "• Left-click: reveal a cell\n"
            "• Right-click: place/remove a flag on a suspected mine\n"
            "• Middle-click (chording): reveal neighbors of a revealed number when it is fully flagged\n\n"
            "Numbers show how many mines are adjacent (8 directions).\n"
            "Reveal every safe cell to win!"
        )