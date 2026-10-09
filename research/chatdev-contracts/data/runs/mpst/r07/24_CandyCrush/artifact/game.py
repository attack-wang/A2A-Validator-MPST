class Game:
    def __init__(self):
        pygame init, screen, clock, fonts
        self.board = Board()
        self.state = IDLE
        self.score = 0
        self.moves_left = MOVES_LIMIT
        self.time_left = GAME_TIME_LIMIT
        self.cascade_level = 0
        self.selected = None  # (r, c)
        self.clearing = []  # list of candies being cleared (with scale anim)
        self.swap_anim = {...}  # candies involved, progress
        self.float_texts = []  # floating score texts
        self.hint = None
        self.hint_timer = 0
        self.message = None, message_timer
    def reset(self): new game
    def handle_input(self, events): mouse clicks/drag, keys (H hint, P pause, R restart, ESC quit)
    def try_swap(self, pos1, pos2): initiate swap animation; moves_left -= 1 will happen only if valid? In Candy Crush, invalid swaps don't consume moves. So: animate swap; after animation, check matches: if none, animate swap back (no move consumed); else consume move, proceed to clearing.
    def update(self, dt): state machine updates + timer countdown (only when IDLE/SWAPPING/etc., not paused/game over)
    def start_clearing(self, matches): compute score, spawn float text, move matched candies to clearing list with scale-down animation, set grid cells to None... 
Hmm wait — careful: if I set grid cells to None immediately but keep candy objects in clearing list for animation, then gravity shouldn't run until clearing animation done. That's fine since state machine handles ordering.
    def update_clearing(self, dt): shrink candies; when done, clear list, apply gravity + refill, state = FALLING
    def update_falling(self, dt): move candies; when all landed: matches = find_matches; if matches: cascade_level += 1; start_clearing(matches); else: cascade_level = 0; check valid moves / shuffle; state = IDLE; check game over conditions.
    def draw(self): board bg, grid cells, candies, clearing candies, selection highlight, hint highlight, HUD, float texts, overlays.
    def run(self): main loop