'''
gui.py
This module implements the tkinter-based graphical user interface for the
tic-tac-toe game, handling rendering, mouse interaction, turn tracking,
score keeping, and game-over presentation.
'''
import tkinter as tk
from functools import partial
from constants import (
    BOARD_SIZE,
    EMPTY,
    PLAYER_X,
    PLAYER_O,
    DRAW_KEY,
    WINDOW_TITLE,
    BG_COLOR,
    TEXT_COLOR,
    MUTED_TEXT_COLOR,
    CELL_COLOR,
    CELL_HOVER_COLOR,
    CELL_TEXT_COLOR,
    X_COLOR,
    O_COLOR,
    WIN_HIGHLIGHT_COLOR,
    WIN_TEXT_COLOR,
    TITLE_FONT,
    STATUS_FONT,
    SCORE_FONT,
    CELL_FONT,
    BUTTON_FONT,
    ACCENT_COLOR,
    ACCENT_HOVER_COLOR,
    ACCENT_TEXT_COLOR,
)
from game_logic import Board
class TicTacToeGUI:
    '''Main application window that renders the board and handles play.'''
    def __init__(self, root):
        '''Construct the window, widgets, and initial game state.'''
        self.root = root
        self.board = Board()
        self.current_player = PLAYER_X
        self.game_over = False
        self.scores = {PLAYER_X: 0, PLAYER_O: 0, DRAW_KEY: 0}
        self._create_widgets()
        self._configure_window()  # Called after widgets exist so centering is accurate.
        self._update_status()
    def _configure_window(self):
        '''Set up the main window's title, fixed size, and centered position.'''
        self.root.title(WINDOW_TITLE)
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)
        self._center_window()
    def _center_window(self):
        '''Center the window on the screen using its required size.'''
        self.root.update_idletasks()
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = max(0, (screen_width - window_width) // 2)
        y = max(0, (screen_height - window_height) // 3)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    def _create_widgets(self):
        '''Build the title label, board grid, status bar, reset button, and scoreboard.'''
        # Title label at the top of the window.
        self.title_label = tk.Label(
            self.root,
            text="Tic-Tac-Toe",
            font=TITLE_FONT,
            fg=TEXT_COLOR,
            bg=BG_COLOR,
        )
        self.title_label.pack(pady=(16, 8))
        # Turn indicator / result message line.
        self.status_label = tk.Label(
            self.root,
            text="",
            font=STATUS_FONT,
            fg=TEXT_COLOR,
            bg=BG_COLOR,
        )
        self.status_label.pack(pady=(0, 12))
        # Board frame containing the 3x3 grid of clickable cells.
        self.board_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.board_frame.pack()
        self.cell_buttons = []
        for row in range(BOARD_SIZE):
            button_row = []
            for col in range(BOARD_SIZE):
                button = tk.Button(
                    self.board_frame,
                    text=EMPTY,
                    font=CELL_FONT,
                    width=4,
                    height=2,
                    bg=CELL_COLOR,
                    fg=CELL_TEXT_COLOR,
                    activebackground=CELL_HOVER_COLOR,
                    activeforeground=CELL_TEXT_COLOR,
                    relief=tk.FLAT,
                    bd=0,
                    highlightthickness=0,
                    command=partial(self._on_cell_click, row, col),
                )
                button.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
                button_row.append(button)
            self.cell_buttons.append(button_row)
        # Controls frame holding the reset button.
        controls = tk.Frame(self.root, bg=BG_COLOR)
        controls.pack(pady=16)
        self.reset_button = tk.Button(
            controls,
            text="New Game",
            font=BUTTON_FONT,
            bg=ACCENT_COLOR,
            fg=ACCENT_TEXT_COLOR,
            activebackground=ACCENT_HOVER_COLOR,
            activeforeground=ACCENT_TEXT_COLOR,
            relief=tk.FLAT,
            padx=16,
            pady=6,
            command=self._reset_game,
        )
        self.reset_button.pack()
        # Scoreboard showing running tallies across rounds.
        self.score_label = tk.Label(
            self.root,
            text=self._format_scores(),
            font=SCORE_FONT,
            fg=MUTED_TEXT_COLOR,
            bg=BG_COLOR,
        )
        self.score_label.pack(pady=(0, 12))
    def run(self):
        '''Start the tkinter main event loop.'''
        self.root.mainloop()
    def _on_cell_click(self, row, col):
        '''Handle a cell click: validate the move, render it, and check game end.'''
        if self.game_over:
            return  # Ignore clicks once the game has ended.
        if not self.board.make_move(row, col, self.current_player):
            return  # Illegal move (occupied or out of range): ignore.
        self._render_move(row, col)
        winner, line = self.board.check_winner()
        if winner is not None:
            message = f"Player {winner} wins!"
            color = X_COLOR if winner == PLAYER_X else O_COLOR
            self._end_game(message, color, line, winner)
        elif self.board.is_full():
            self._end_game("It's a draw!", MUTED_TEXT_COLOR, None, None)
        else:
            # Alternate turns between X and O.
            self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
            self._update_status()
    def _render_move(self, row, col):
        '''Draw the placed symbol in the player's color and lock the cell.'''
        symbol = self.board.get_cell(row, col)
        color = X_COLOR if symbol == PLAYER_X else O_COLOR
        self.cell_buttons[row][col].configure(
            text=symbol,
            fg=color,
            state=tk.DISABLED,
            disabledforeground=color,
        )
    def _end_game(self, message, color, line, winner):
        '''Finalize the round: update scores, highlight the win, show the result.'''
        self.game_over = True
        if winner is not None:
            self.scores[winner] += 1
            self._highlight_winning_cells(line)
        else:
            self.scores[DRAW_KEY] += 1
        self._update_status(message, color)
        self._refresh_score()
    def _highlight_winning_cells(self, line):
        '''Recolor the three cells forming the winning line.'''
        for row, col in line:
            self.cell_buttons[row][col].configure(
                bg=WIN_HIGHLIGHT_COLOR,
                fg=WIN_TEXT_COLOR,
                disabledforeground=WIN_TEXT_COLOR,
            )
    def _reset_game(self):
        '''Clear the board and state so a fresh game can begin (X starts).'''
        self.board.reset()
        self.current_player = PLAYER_X
        self.game_over = False
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.cell_buttons[row][col].configure(
                    text=EMPTY,
                    bg=CELL_COLOR,
                    fg=CELL_TEXT_COLOR,
                    state=tk.NORMAL,
                )
        self._update_status()
    def _update_status(self, message=None, color=TEXT_COLOR):
        '''Show whose turn it is, or a custom end-of-game message.'''
        if message is None:
            message = f"Player {self.current_player}'s turn"
            color = X_COLOR if self.current_player == PLAYER_X else O_COLOR
        self.status_label.configure(text=message, fg=color)
    def _refresh_score(self):
        '''Update the scoreboard label with the latest tallies.'''
        self.score_label.configure(text=self._format_scores())
    def _format_scores(self):
        '''Return the formatted score line for X wins, O wins, and draws.'''
        return (
            f"X wins: {self.scores[PLAYER_X]}    "
            f"O wins: {self.scores[PLAYER_O]}    "
            f"Draws: {self.scores[DRAW_KEY]}"
        )