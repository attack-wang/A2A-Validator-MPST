class MinesweeperGUI:
    '''Main application window: renders the board and handles player input.'''
    def __init__(self, root):
        self.root = root
        self.root.title('Minesweeper')
        self.root.resizable(False, False)  # or True
        self.difficulty = Difficulty.BEGINNER
        self.board = None
        self.cell_buttons = None
        self.timer_id = None
        self.elapsed_time = 0
        self.timer_running = False
        self._build_menu()
        self._build_header()
        self._build_board_area()
        self.new_game(self.difficulty)
    def _build_menu(self):
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label='New Game', command=lambda: self.new_game(self.difficulty))
        game_menu.add_separator()
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        for level in Difficulty.all_levels():
            game_menu.add_radiobutton(
                label=level.capitalize(),
                variable=self.difficulty_var,
                value=level,
                command=lambda: self.new_game(self.difficulty_var.get())
            )
        game_menu.add_separator()
        game_menu.add_command(label='Exit', command=self.root.quit)
        menubar.add_cascade(label='Game', menu=game_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label='How to Play', command=self._show_help)
        menubar.add_cascade(label='Help', menu=help_menu)
        self.root.config(menu=menubar)
    def _build_header(self):
        header = tk.Frame(self.root, bg=..., padx=..., pady=...)
        header.pack(fill='x', padx=6, pady=(6, 3))
        self.mine_counter = tk.Label(header, text='010', font=('Consolas', 16, 'bold'), bg='black', fg='red', width=4, anchor='center', relief='sunken')
        self.mine_counter.pack(side='left')
        self.face_button = tk.Button(header, text='🙂', font=('Segoe UI Emoji', 14), width=3, command=self._reset_current)
        self.face_button.pack(side='left', expand=True)  # center
        self.timer_label = tk.Label(header, text='000', ...)
        self.timer_label.pack(side='right')