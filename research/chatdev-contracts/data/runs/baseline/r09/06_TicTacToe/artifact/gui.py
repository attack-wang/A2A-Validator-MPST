'''
gui.py
Graphical user interface for the tic-tac-toe game, built with tkinter.
This module contains the TicTacToeGUI class, which renders the 3x3 grid,
handles mouse-click interactions, shows whose turn it is, tracks and
displays each player's move count, highlights the winning line, and
provides a "New Game" button to restart the match.
'''
import tkinter as tk
from tkinter import messagebox
class TicTacToeGUI:
    """Tkinter-based graphical interface for the tic-tac-toe game."""
    CELL_FONT = ('Helvetica', 44, 'bold')
    TITLE_FONT = ('Helvetica', 24, 'bold')
    STATUS_FONT = ('Helvetica', 14)
    MOVES_FONT = ('Helvetica', 11)
    BUTTON_FONT = ('Helvetica', 12, 'bold')
    COLOR_BG = '#2B2B2B'
    COLOR_CELL = '#3C3F41'
    COLOR_CELL_ACTIVE = '#4B6EAF'
    COLOR_X = '#FF6B6B'
    COLOR_O = '#4ECDC4'
    COLOR_WIN = '#FFD93D'
    COLOR_WIN_TEXT = '#1A1A1A'
    COLOR_TEXT = '#F5F5F5'
    def __init__(self, root, game):
        """Build the window, widgets, and initial status display."""
        self.root = root
        self.game = game
        self.root.title('Tic-Tac-Toe')
        self.root.configure(bg=self.COLOR_BG)
        self.root.resizable(False, False)
        self._center_window(440, 600)
        self.cells = [[None for _ in range(3)] for _ in range(3)]
        self._create_widgets()
        self.refresh_ui()
        self.update_status(f"Player {self.game.current_player}'s turn")
    def _center_window(self, width, height):
        """Position the window in the center of the screen."""
        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    def _create_widgets(self):
        """Create the title, status label, 3x3 cell grid, move tracker, and reset button."""
        self.title_label = tk.Label(self.root, text='Tic-Tac-Toe',
                                    font=self.TITLE_FONT,
                                    fg=self.COLOR_TEXT, bg=self.COLOR_BG)
        self.title_label.pack(pady=(15, 5))
        self.status_label = tk.Label(self.root, text='',
                                     font=self.STATUS_FONT,
                                     fg=self.COLOR_TEXT, bg=self.COLOR_BG)
        self.status_label.pack(pady=(0, 8))
        board_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        board_frame.pack(padx=15, pady=5)
        for row in range(3):
            for col in range(3):
                cell = tk.Button(board_frame,
                                 text=' ',
                                 font=self.CELL_FONT,
                                 width=3, height=1,
                                 bg=self.COLOR_CELL,
                                 fg=self.COLOR_TEXT,
                                 activebackground=self.COLOR_CELL_ACTIVE,
                                 activeforeground=self.COLOR_TEXT,
                                 disabledforeground=self.COLOR_TEXT,
                                 relief=tk.RAISED, bd=2,
                                 command=lambda r=row, c=col: self.on_cell_click(r, c))
                cell.grid(row=row, column=col, padx=4, pady=4, ipady=6, sticky='nsew')
                self.cells[row][col] = cell
        for i in range(3):
            board_frame.grid_rowconfigure(i, weight=1)
            board_frame.grid_columnconfigure(i, weight=1)
        self.moves_label = tk.Label(self.root, text='',
                                    font=self.MOVES_FONT,
                                    fg='#B0B0B0', bg=self.COLOR_BG)
        self.moves_label.pack(pady=(10, 0))
        self.reset_button = tk.Button(self.root, text='New Game',
                                      font=self.BUTTON_FONT,
                                      bg=self.COLOR_CELL_ACTIVE,
                                      fg=self.COLOR_TEXT,
                                      activebackground=self.COLOR_CELL,
                                      activeforeground=self.COLOR_TEXT,
                                      relief=tk.RAISED,
                                      padx=20, pady=8,
                                      command=self.reset_game)
        self.reset_button.pack(pady=12)
    def on_cell_click(self, row, col):
        """Handle a click on cell (row, col): apply the move and refresh the UI."""
        if self.game.game_over:
            return
        if not self.game.make_move(row, col):
            return  # Cell already occupied or game finished
        self.refresh_ui()
        if self.game.game_over:
            self.handle_game_end()
        else:
            self.update_status(f"Player {self.game.current_player}'s turn")
    def refresh_ui(self):
        """Sync all widgets with the current state of the game."""
        self.update_board()
        self.update_moves_label()
    def update_board(self):
        """Refresh every cell button to reflect the board contents."""
        for row in range(3):
            for col in range(3):
                symbol = self.game.board[row][col]
                cell = self.cells[row][col]
                if symbol == 'X':
                    cell.config(text='X', state=tk.DISABLED,
                                disabledforeground=self.COLOR_X)
                elif symbol == 'O':
                    cell.config(text='O', state=tk.DISABLED,
                                disabledforeground=self.COLOR_O)
                else:
                    cell.config(text=' ', state=tk.NORMAL,
                                disabledforeground=self.COLOR_TEXT)
    def update_status(self, message):
        """Set the text of the status label."""
        self.status_label.config(text=message)
    def update_moves_label(self):
        """Show how many moves each player has made so far."""
        x_moves = self.game.moves['X']
        o_moves = self.game.moves['O']
        self.moves_label.config(text=f'Moves — X: {x_moves}   |   O: {o_moves}')
    def highlight_winning_line(self):
        """Highlight the three cells that form the winning line."""
        if self.game.winning_line:
            for row, col in self.game.winning_line:
                self.cells[row][col].config(bg=self.COLOR_WIN,
                                            disabledforeground=self.COLOR_WIN_TEXT)
    def handle_game_end(self):
        """Announce the result, highlight the win, and lock the board."""
        if self.game.winner:
            self.highlight_winning_line()
            self.update_status(f'Player {self.game.winner} wins!')
            messagebox.showinfo('Game Over', f'Player {self.game.winner} wins!')
        else:
            self.update_status("It's a draw!")
            messagebox.showinfo('Game Over', "It's a draw!")
        for row in range(3):
            for col in range(3):
                self.cells[row][col].config(state=tk.DISABLED)
    def reset_game(self):
        """Reset the game logic and UI so a fresh round can begin."""
        self.game.reset()
        for row in range(3):
            for col in range(3):
                self.cells[row][col].config(text=' ',
                                            state=tk.NORMAL,
                                            bg=self.COLOR_CELL,
                                            fg=self.COLOR_TEXT,
                                            disabledforeground=self.COLOR_TEXT)
        self.refresh_ui()
        self.update_status(f"Player {self.game.current_player}'s turn")