class TicTacToeGUI:
    def __init__(self, root, game=None):
        self._root = root
        self._game = game if game is not None else TicTacToeGame()
        self._cells = {}          # (row, col) -> tk.Button
        self._score = {"X": 0, "O": 0, "Draws": 0}
        self._root.title("Tic-Tac-Toe")
        self._root.resizable(False, False)
        self._root.configure(bg="#ffffff")
        self._cell_font = tkfont.Font(size=self.CELL_FONT_SIZE, weight="bold")
        self._status_font = tkfont.Font(size=13)
        self._score_font = tkfont.Font(size=11)
        self._build_widgets()
        self._refresh_all()
    def _build_widgets(self):
        """Create the status bar, the 3x3 button grid and the controls."""
        # Status label
        self._status_label = tk.Label(
            self._root,
            text="",
            font=self._status_font,
            pady=8,
            bg="#ffffff",
        )
        self._status_label.grid(row=0, column=0, columnspan=3, sticky="ew")
        # Board buttons
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                button = tk.Button(
                    self._root,
                    text=" ",
                    font=self._cell_font,
                    width=4,
                    height=2,
                    bg=self.DEFAULT_CELL_COLOR,
                    command=lambda r=row, c=col: self._on_cell_click(r, c),
                )
                button.grid(row=row + 1, column=col, padx=3, pady=3,
                            sticky="nsew")
                self._cells[(row, col)] = button
        # Scoreboard
        self._score_label = tk.Label(
            self._root, text="", font=self._score_font, bg="#ffffff", pady=6
        )
        self._score_label.grid(row=4, column=0, columnspan=3, sticky="ew")
        # New game button
        self._new_game_button = tk.Button(
            self._root,
            text="New Game",
            font=self._status_font,
            command=self._start_new_round,
        )
        self._new_game_button.grid(row=5, column=0, columnspan=3,
                                   sticky="ew", padx=10, pady=(0, 10))