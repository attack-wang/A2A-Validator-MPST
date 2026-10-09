'''
gui.py
Graphical user interface for the Tic-Tac-Toe application, built with
the standard-library tkinter package (no external dependencies).
The TicTacToeGUI class owns the GameBoard and the two Player objects,
renders a 3x3 grid of clickable cells plus a scoreboard and status
bar, alternates turns between the players, highlights the winning
line, keeps score across rounds, and offers a rematch after every
game.
'''
import tkinter as tk
from tkinter import messagebox
from game_logic import GameBoard
from players import Player
class TicTacToeGUI:
    '''Main application window: board rendering, turn flow, and end-game handling.'''
    CELL_FONT = ("Helvetica", 32, "bold")
    STATUS_FONT = ("Helvetica", 13)
    TITLE_FONT = ("Helvetica", 20, "bold")
    SCORE_FONT = ("Helvetica", 12, "bold")
    BG_COLOR = "#1e272e"
    BUTTON_COLOR = "#485460"
    BUTTON_ACTIVE_COLOR = "#5758bb"
    X_COLOR = "#ff6b6b"
    O_COLOR = "#4cd137"
    WIN_COLOR = "#fbc531"
    TEXT_COLOR = "#f5f6fa"
    WINDOW_WIDTH = 340
    WINDOW_HEIGHT = 520
    # "hand2" is a valid cursor name on Windows, macOS, and Linux/X11.
    # "pointinghand" only exists on Windows/macOS and raises a TclError
    # on Linux, so the cross-platform name is used instead.
    CURSOR_HAND = "hand2"
    def __init__(self, root):
        '''Initialize game state, build the interface, and show the first turn.'''
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_COLOR)
        self._center_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.board = GameBoard()
        self.players = [Player("X"), Player("O")]
        self.starting_player_index = 0
        self.current_player_index = 0
        self.game_over = False
        self.scoreboard = {"X": 0, "O": 0, "Draws": 0}
        self.buttons = [[None] * GameBoard.BOARD_SIZE
                        for _ in range(GameBoard.BOARD_SIZE)]
        self._build_interface()
        self._update_status()
    # ------------------------------------------------------------------
    # Interface construction
    # ------------------------------------------------------------------
    def _build_interface(self):
        '''Create the title, scoreboard, 3x3 cell grid, status bar, and reset button.'''
        title = tk.Label(self.root, text="Tic-Tac-Toe",
                         font=self.TITLE_FONT,
                         bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        title.grid(row=0, column=0, columnspan=3, pady=(10, 2), sticky="nsew")
        self.score_label = tk.Label(self.root, text="",
                                    font=self.SCORE_FONT,
                                    bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.score_label.grid(row=1, column=0, columnspan=3, pady=(0, 6),
                              sticky="nsew")
        self._update_scoreboard()
        for row in range(GameBoard.BOARD_SIZE):
            self.root.grid_rowconfigure(row + 2, weight=1)
            for col in range(GameBoard.BOARD_SIZE):
                button = tk.Button(
                    self.root,
                    text=" ",
                    width=4, height=1,
                    font=self.CELL_FONT,
                    bg=self.BUTTON_COLOR,
                    fg=self.TEXT_COLOR,
                    activebackground=self.BUTTON_ACTIVE_COLOR,
                    activeforeground=self.TEXT_COLOR,
                    relief=tk.RAISED,
                    bd=3,
                    cursor=self.CURSOR_HAND,
                    command=lambda r=row, c=col: self._on_cell_click(r, c)
                )
                button.grid(row=row + 2, column=col, padx=5, pady=5, sticky="nsew")
                self.buttons[row][col] = button
        self.status_label = tk.Label(self.root, text="",
                                     font=self.STATUS_FONT,
                                     bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.status_label.grid(row=5, column=0, columnspan=3, pady=(8, 2),
                               sticky="nsew")
        reset_button = tk.Button(self.root, text="New Game",
                                 font=self.STATUS_FONT,
                                 bg=self.BUTTON_COLOR,
                                 fg=self.TEXT_COLOR,
                                 activebackground=self.BUTTON_ACTIVE_COLOR,
                                 activeforeground=self.TEXT_COLOR,
                                 relief=tk.RAISED,
                                 cursor=self.CURSOR_HAND,
                                 command=self.reset_game)
        reset_button.grid(row=6, column=0, columnspan=3, padx=12,
                          pady=(2, 12), sticky="nsew")
        for col in range(GameBoard.BOARD_SIZE):
            self.root.grid_columnconfigure(col, weight=1)
    def _center_window(self, width, height):
        '''Position the window in the middle of the screen.'''
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry("{}x{}+{}+{}".format(width, height, x, y))
    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------
    def _on_cell_click(self, row, col):
        '''
        Respond to a click on cell (row, col): ignore clicks after the
        game ends, reject moves onto occupied squares, otherwise apply
        the current player's move and evaluate the resulting state.
        '''
        if self.game_over:
            return
        player = self.players[self.current_player_index]
        if not self.board.is_valid_move(row, col):
            self._update_status("That square is taken - choose another one!")
            return
        self.board.make_move(row, col, player.get_symbol())
        self._refresh_board()
        winner_symbol = self.board.check_winner()
        if winner_symbol is not None:
            self._handle_win(player)
        elif self.board.is_full():
            self._handle_draw()
        else:
            self.current_player_index = 1 - self.current_player_index
            self._update_status()
    # ------------------------------------------------------------------
    # End-game handling
    # ------------------------------------------------------------------
    def _handle_win(self, player):
        '''Record the win, highlight the line, announce it, and offer a rematch.'''
        self.game_over = True
        self.scoreboard[player.get_symbol()] += 1
        self._update_scoreboard()
        self._highlight_winning_line()
        message = "{} wins!".format(player)
        self._update_status(message)
        self._offer_rematch(message)
    def _handle_draw(self):
        '''Record the draw, announce it, and offer a rematch.'''
        self.game_over = True
        self.scoreboard["Draws"] += 1
        self._update_scoreboard()
        message = "It's a draw - the board is full!"
        self._update_status(message)
        self._offer_rematch(message)
    def _offer_rematch(self, message):
        '''Ask the players whether they would like to play again.'''
        if messagebox.askyesno("Game Over", "{}\n\nPlay again?".format(message)):
            self.reset_game()
    def _highlight_winning_line(self):
        '''Recolor the three cells that form the winning line.'''
        line = self.board.get_winning_line()
        if line is None:
            return
        for row, col in line:
            self.buttons[row][col].config(bg=self.WIN_COLOR)
    # ------------------------------------------------------------------
    # Display updates
    # ------------------------------------------------------------------
    def _refresh_board(self):
        '''Mirror the board state onto the cell buttons (text and color).'''
        for row in range(GameBoard.BOARD_SIZE):
            for col in range(GameBoard.BOARD_SIZE):
                symbol = self.board.get_cell(row, col)
                button = self.buttons[row][col]
                button.config(text=symbol)
                if symbol == "X":
                    button.config(fg=self.X_COLOR)
                elif symbol == "O":
                    button.config(fg=self.O_COLOR)
    def _update_status(self, message=None):
        '''Show a custom message, or the current player's turn by default.'''
        if message is None:
            player = self.players[self.current_player_index]
            message = "{} - your turn".format(player)
        self.status_label.config(text=message)
    def _update_scoreboard(self):
        '''Refresh the running win/draw tally shown above the board.'''
        self.score_label.config(
            text="X: {} wins   O: {} wins   Draws: {}".format(
                self.scoreboard["X"], self.scoreboard["O"],
                self.scoreboard["Draws"]))
    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------
    def reset_game(self):
        '''
        Clear the board and interface for a fresh round. The starting
        player alternates each game so neither side keeps an advantage.
        '''
        self.board.reset()
        self.starting_player_index = 1 - self.starting_player_index
        self.current_player_index = self.starting_player_index
        self.game_over = False
        for row in range(GameBoard.BOARD_SIZE):
            for col in range(GameBoard.BOARD_SIZE):
                self.buttons[row][col].config(text=" ",
                                              bg=self.BUTTON_COLOR,
                                              fg=self.TEXT_COLOR)
        self._update_status()