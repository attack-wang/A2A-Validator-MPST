'''
Tkinter graphical interface for the Minesweeper game.
Renders the board as a grid of buttons, handles left-click revealing and
right-click flagging, keeps a live mine counter and timer, and shows
win/lose dialogs. All helper methods referenced by menus, header and
click handlers are fully implemented in this module.
'''
import tkinter as tk
from tkinter import messagebox
from config import (DIFFICULTY_SETTINGS, DEFAULT_DIFFICULTY, CELL_WIDTH,
                    CELL_HEIGHT, CELL_MIN_SIZE, FONT_MAIN, FONT_HEADER,
                    NUMBER_COLORS, COVERED_BG, REVEALED_BG, FLAG_BG, FLAG_FG,
                    MINE_BG, MINE_FG, EXPLODED_BG, EXPLODED_FG,
                    FLAG_TEXT, MINE_TEXT, COUNTER_FORMAT)
from game_logic import MinesweeperBoard
class MinesweeperGUI(tk.Tk):
    '''Main application window: menu, header (counter/timer/status) and board grid.'''
    def __init__(self):
        super().__init__()
        self.title("Minesweeper")
        self.resizable(False, False)
        self.current_difficulty = DEFAULT_DIFFICULTY
        self.board = None
        self.cell_buttons = []
        self.board_frame = None
        self.timer_job = None
        self.elapsed_seconds = 0
        self._build_menu()
        self._build_header()
        self.new_game(DEFAULT_DIFFICULTY)
    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_menu(self):
        '''Create the menu bar with difficulty selection and exit.'''
        menubar = tk.Menu(self)
        game_menu = tk.Menu(menubar, tearoff=0)
        for difficulty in DIFFICULTY_SETTINGS:
            game_menu.add_command(
                label=difficulty,
                command=lambda d=difficulty: self.new_game(d)
            )
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self._quit_game)
        menubar.add_cascade(label="Game", menu=game_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="How to play", command=self._show_help)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)
    def _build_header(self):
        '''Create the header with the mine counter, status text and timer.'''
        header = tk.Frame(self, bd=2, relief="groove")
        header.pack(fill="x", padx=6, pady=(6, 2))
        self.mine_label = tk.Label(header, text=COUNTER_FORMAT.format(0),
                                   font=FONT_HEADER, fg="#CC0000", width=5, anchor="w")
        self.mine_label.pack(side="left", padx=8)
        self.status_label = tk.Label(header, text="", font=FONT_HEADER)
        self.status_label.pack(side="left", expand=True, fill="x")
        self.timer_label = tk.Label(header, text=COUNTER_FORMAT.format(0),
                                    font=FONT_HEADER, fg="#0000CC", width=5, anchor="e")
        self.timer_label.pack(side="right", padx=8)
    def _build_grid(self):
        '''(Re)build the grid of cell buttons for the current board.'''
        if self.board_frame is not None:
            self.board_frame.destroy()
        self.board_frame = tk.Frame(self, bd=3, relief="sunken")
        self.board_frame.pack(padx=6, pady=6)
        self.cell_buttons = []
        for r in range(self.board.rows):
            row_buttons = []
            for c in range(self.board.cols):
                button = tk.Button(
                    self.board_frame,
                    width=CELL_WIDTH,
                    height=CELL_HEIGHT,
                    font=FONT_MAIN,
                    bg=COVERED_BG,
                    relief="raised",
                )
                button.grid(row=r, column=c, padx=0, pady=0, sticky="nsew")
                button.bind("<Button-1>", lambda _e, rr=r, cc=c: self._on_left_click(rr, cc))
                button.bind("<Button-3>", lambda _e, rr=r, cc=c: self._on_right_click(rr, cc))
                button.bind("<Button-2>", lambda _e, rr=r, cc=c: self._on_right_click(rr, cc))
                row_buttons.append(button)
            self.cell_buttons.append(row_buttons)
        for r in range(self.board.rows):
            self.board_frame.rowconfigure(r, weight=1, minsize=CELL_MIN_SIZE)
        for c in range(self.board.cols):
            self.board_frame.columnconfigure(c, weight=1, minsize=CELL_MIN_SIZE)
        self._refresh_board()
    # ------------------------------------------------------------------
    # Game lifecycle
    # ------------------------------------------------------------------
    def new_game(self, difficulty):
        '''Start a fresh game at the given difficulty.'''
        rows, cols, num_mines = DIFFICULTY_SETTINGS[difficulty]
        self.current_difficulty = difficulty
        self._stop_timer()
        self.elapsed_seconds = 0
        self.board = MinesweeperBoard(rows, cols, num_mines)
        self.status_label.config(text="{}: {}x{} grid, {} mines".format(
            difficulty, rows, cols, num_mines))
        self._build_grid()
        self._update_header()
    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _on_left_click(self, row, col):
        '''Reveal a cell; handle win/lose outcomes and refresh the display.'''
        if self.board.game_over:
            return
        revealed = self.board.reveal(row, col)
        if not revealed:
            self._refresh_board()
            return
        self._start_timer()
        if self.board.game_over and self.board.won:
            self.board.flag_all_mines()
            self._stop_timer()
            self._refresh_board()
            self._update_header()
            self.status_label.config(text="You win!")
            if messagebox.askyesno(
                    "Minesweeper",
                    "Congratulations, you cleared the board!\nStart a new game?"):
                self.new_game(self.current_difficulty)
        elif self.board.game_over:
            self.board.reveal_all_mines()
            self._stop_timer()
            self._refresh_board()
            self._update_header()
            self.status_label.config(text="Boom! Game over.")
            if messagebox.askyesno(
                    "Minesweeper",
                    "You hit a mine! Game over.\nStart a new game?"):
                self.new_game(self.current_difficulty)
        else:
            self._refresh_board()
            self._update_header()
    def _on_right_click(self, row, col):
        '''Toggle a flag on a covered cell and refresh the display.'''
        if self.board.game_over:
            return
        if self.board.toggle_flag(row, col):
            self._refresh_board()
            self._update_header()
    # ------------------------------------------------------------------
    # Timer management
    # ------------------------------------------------------------------
    def _start_timer(self):
        '''Start the 1-second ticker if it is not already running.'''
        if self.timer_job is None and not self.board.game_over:
            self.timer_job = self.after(1000, self._tick)
    def _tick(self):
        '''Advance the timer by one second and reschedule while the game runs.'''
        self.elapsed_seconds += 1
        self._update_header()
        self.timer_job = None
        if not self.board.game_over:
            self.timer_job = self.after(1000, self._tick)
    def _stop_timer(self):
        '''Cancel any pending timer callback.'''
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None
    # ------------------------------------------------------------------
    # Menu / header helpers
    # ------------------------------------------------------------------
    def _quit_game(self):
        '''Stop the timer and close the application window.'''
        self._stop_timer()
        self.destroy()
    def _show_help(self):
        '''Show a short instructions dialog.'''
        messagebox.showinfo(
            "How to play",
            "Left-click a cell to reveal it.\n"
            "Right-click a cell to flag/unflag a suspected mine.\n"
            "Numbers show how many mines are adjacent.\n"
            "Reveal every safe cell to win!"
        )
    def _update_header(self):
        '''Refresh the mine counter and timer labels.'''
        mines_left = self.board.num_mines - self.board.count_flags()
        self.mine_label.config(text=COUNTER_FORMAT.format(max(mines_left, 0)))
        self.timer_label.config(text=COUNTER_FORMAT.format(min(self.elapsed_seconds, 999)))
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def _refresh_board(self):
        '''Update the visual state of every cell button.'''
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                self._update_cell(r, c)
    def _update_cell(self, row, col):
        '''Apply the correct color, text and relief for a single cell.'''
        cell = self.board.grid[row][col]
        button = self.cell_buttons[row][col]
        if cell.is_revealed:
            if cell.is_mine:
                if self.board.exploded_at == (row, col):
                    bg, fg = EXPLODED_BG, EXPLODED_FG
                else:
                    bg, fg = MINE_BG, MINE_FG
                text = MINE_TEXT
                relief = "sunken"
            else:
                bg = REVEALED_BG
                fg = NUMBER_COLORS.get(cell.adjacent_mines, "#000000")
                text = str(cell.adjacent_mines) if cell.adjacent_mines > 0 else ""
                relief = "sunken"
            button.config(text=text, bg=bg, fg=fg, relief=relief,
                          state="disabled", disabledforeground=fg)
        elif cell.is_flagged:
            button.config(text=FLAG_TEXT, bg=FLAG_BG, fg=FLAG_FG,
                          relief="raised", state="normal")
        else:
            button.config(text="", bg=COVERED_BG, fg="#000000",
                          relief="raised", state="normal")