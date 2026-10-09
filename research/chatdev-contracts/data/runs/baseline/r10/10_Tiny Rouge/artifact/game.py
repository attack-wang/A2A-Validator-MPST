"""Core game logic: state machine, movement, combat, level progression."""
class Game:
    def __init__(self):
        pygame setup here? Or in main? I'll do pygame.init() in Game.
        self.renderer = Renderer(self)
        self.clock = pygame.time.Clock()
        self.state = STATE_PLAYING
        self.level_number = 1
        self.messages = []
        self.move_timer = 0
        self._load_level(1)
        self.log("Welcome to the Tower of the Sorcerer!")
    def _load_level(self, level): ...
    def run(self): main loop
    def _handle_events(self): quit, restart key, ESC
    def _update(self, dt): movement repeat handling
    def _try_move(self, dx, dy): core interaction
    def _fight(self, monster): combat
    def _open_chest(self, chest): heal
    def _enter_door(self): next level
    def _game_over(self): state change
    def restart(self): reset
    def log(self, text): append message, trim
    def adjacent_monsters(self): for UI