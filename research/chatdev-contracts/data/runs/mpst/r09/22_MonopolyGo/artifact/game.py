class Game:
    def __init__(self, player_names, starting_money=1500, max_rounds=... )
    def setup
    def play(self) -> main loop
    def take_turn(self, player)
    def handle_jail(self, player) -> bool moved (rolled and moved?)
    def move_and_resolve(self, player, steps)
    def resolve_space(self, player)
    def handle_property(self, player, prop)
    def handle_chance(self, player)
    def apply_card(self, player, card)
    def pass_go(self, player)
    def send_to_jail(self, player)
    def charge(self, player, amount, creditor=None, reason) -> handles bankruptcy
    def bankrupt_player(self, player, creditor)
    def check_game_over(self)
    def declare_winner(self)
    def show_status(self)