'''
gui.py
Graphical user interface for the Tic-Tac-Toe game, built with tkinter
(included with the Python standard library, so no extra packages are
required).
Classes:
    TicTacToeGUI: Renders the 3x3 grid, handles player clicks, shows the
                  current status, highlights the winning line, and offers
                  a "Play Again" button to restart the round.
'''
import tkinter as tk
from game_logic import TicTacToeGame
class TicTacToeGUI:
    '''
    Tkinter front-end for TicTacToeGame.
    Layout (top to bottom):
        - A status label ("Player X's turn" / winner / draw message).
        - A fixed-size 3x3 grid of large clickable buttons.
        - A "Play Again" button that resets the board.
    '''
    # Visual configuration
    GRID_SIZE = 330            # Pixel size (width and height) of the board area
    COLOR_BG = '#1e2630'       # Window background
    COLOR_CELL = '#2c3a4b'     # Empty cell background
    COLOR_BORDER = '#46586d'   # Thin border around each cell
    COLOR_X = '#4fc3f7'        # Color of the X marks / X player's status
    COLOR_O = '#ffb74d'        # Color of the O marks / O player's status
    COLOR_WIN = '#2e7d32'      # Highlight color for the winning line
    COLOR_TEXT = '#e8eef4'     # Default status text color
    COLOR_PANEL = '#37474f'    # Restart button background
    def __init__(self, root):
        '''
        Build the window and widgets, then prepare a fresh game.
        Args:
            root (tk.Tk): The root tkinter window.
        '''
        self.game = TicTacToeGame()
        self.root = root
        self.cells = {}  # Maps (row, col) -> tk.Button
        self.root.title('Tic-Tac-Toe')
        self.root.configure(bg=self.COLOR_BG)
        self.root.resizable(False, False)
        self._build_ui()
        self._center_window()
        self._update_status()
    def _build_ui(self):
        '''Create the status label, the 3x3 button grid, and the restart button.'''
        # Status label (whose turn / result of the game)
        self.status_label = tk.Label(
            self.root,
            text='',
            font=('Helvetica', 18, 'bold'),
            bg=self.COLOR_BG,
            fg=self.COLOR_TEXT,
            pady=12,
        )
        self.status_label.pack(fill=tk.X)
        # Fixed-size frame that holds the 3x3 grid; rows/columns expand
        # equally so every cell is a uniform square on every platform.
        grid_frame = tk.Frame(
            self.root,
            bg=self.COLOR_BG,
            width=self.GRID_SIZE,
            height=self.GRID_SIZE,
        )
        grid_frame.pack_propagate(False)
        grid_frame.pack(padx=15, pady=5)
        for index in range(3):
            grid_frame.rowconfigure(index, weight=1)
            grid_frame.columnconfigure(index, weight=1)
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    grid_frame,
                    text='',
                    font=('Helvetica', 40, 'bold'),
                    bg=self.COLOR_CELL,
                    fg=self.COLOR_TEXT,
                    activebackground=self.COLOR_CELL,
                    activeforeground=self.COLOR_TEXT,
                    disabledforeground=self.COLOR_TEXT,
                    relief=tk.FLAT,
                    bd=0,
                    highlightthickness=2,
                    highlightbackground=self.COLOR_BORDER,
                    command=lambda r=row, c=col: self._on_cell_click(r, c),
                )
                button.grid(row=row, column=col, padx=4, pady=4, sticky='nsew')
                self.cells[(row, col)] = button
        # Restart button
        restart_button = tk.Button(
            self.root,
            text='Play Again',
            font=('Helvetica', 13, 'bold'),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_TEXT,
            activebackground='#455a64',
            activeforeground=self.COLOR_TEXT,
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self._restart,
        )
        restart_button.pack(pady=12)
    def _center_window(self):
        '''Position the window in the middle of the screen.'''
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        x = max(0, (self.root.winfo_screenwidth() - width) // 2)
        y = max(0, (self.root.winfo_screenheight() - height) // 2)
        self.root.geometry(f'+{x}+{y}')
    def _on_cell_click(self, row, col):
        '''
        Respond to a click on cell (row, col).
        Applies the move through the game logic, refreshes the board, and
        either announces the result (win/draw) or updates the turn status.
        '''
        if not self.game.make_move(row, col):
            return  # Invalid move: cell occupied or game already finished
        self._update_board()
        if self.game.is_game_over():
            self._show_game_end()
        else:
            self._update_status()
    def _update_board(self):
        '''Refresh every button's text, color, and enabled state from the board.'''
        board = self.game.get_board()
        for row in range(3):
            for col in range(3):
                mark = board[row][col]
                button = self.cells[(row, col)]
                if mark:
                    color = self.COLOR_X if mark == 'X' else self.COLOR_O
                    button.config(
                        text=mark,
                        fg=color,
                        disabledforeground=color,
                        state=tk.DISABLED,
                    )
                else:
                    button.config(text='', state=tk.NORMAL)
    def _update_status(self):
        '''Display whose turn it is, colored to match the current player.'''
        player = self.game.get_current_player()
        self.status_label.config(
            text=f"Player {player}'s turn",
            fg=self.COLOR_X if player == 'X' else self.COLOR_O,
        )
    def _show_game_end(self):
        '''Announce the winner (highlighting the winning line) or a draw.'''
        winner = self.game.get_winner()
        if winner:
            self.status_label.config(
                text=f'Player {winner} wins!',
                fg=self.COLOR_X if winner == 'X' else self.COLOR_O,
            )
            for row, col in self.game.get_winning_cells():
                self.cells[(row, col)].config(
                    bg=self.COLOR_WIN,
                    fg='#ffffff',
                    disabledforeground='#ffffff',
                )
        else:
            self.status_label.config(text="It's a draw!", fg=self.COLOR_TEXT)
        # Lock the board so the final position stays visible until restart.
        for button in self.cells.values():
            button.config(state=tk.DISABLED)
    def _restart(self):
        '''Reset the game state and restore every widget for a new round.'''
        self.game.reset()
        for button in self.cells.values():
            button.config(
                text='',
                bg=self.COLOR_CELL,
                fg=self.COLOR_TEXT,
                disabledforeground=self.COLOR_TEXT,
                state=tk.NORMAL,
            )
        self._update_status()
    def run(self):
        '''Start the tkinter event loop.'''
        self.root.mainloop()