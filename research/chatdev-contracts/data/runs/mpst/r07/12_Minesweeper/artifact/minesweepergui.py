class MinesweeperGUI:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.canvas = None
        self.mine_label = None
        self.timer_label = None
        self.face_button = None
        self._build_menu()
        self._build_header()
        self._build_canvas()
        self.new_round()