class Game:
    STARTING_MONEY = 1500
    JAIL_FINE = 50
    MAX_JAIL_TURNS = 3
    def __init__(self, player_names, max_rounds=50)
    def setup(...)
    def run(self)
    def play_round(self)
    def take_turn(self, player)
    def roll_phase / move_player(player, steps)
    def handle_landing(self, player)
    def handle_property_landing(self, player, prop)
    def handle_chance_landing(self, player)
    def apply_chance_effect(self, player, card)
    def transfer(self, payer, payee, amount)  # handles bankruptcy
    def check_bankruptcy(self, player)
    def display_status(self)
    def display_board(self)  # maybe a simple text board? Could be nice but complex. I'll display a compact list of spaces with owners.
    def prompt(self, msg, options)  # input helper with validation
    def determine_winner(self)