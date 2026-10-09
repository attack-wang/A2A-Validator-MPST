'''
chance.py
Chance card module for the simplified Monopoly Go! game.
Defines the ChanceCard class and the deck of simplified chance cards.
'''
import random
from board import Board, GO_SALARY
class ChanceCard:
    """A single chance card with a simple effect."""
    def __init__(self, description, effect, amount=0, target=0):
        self.description = description
        self.effect = effect  # one of the EFFECT_* constants
        self.amount = amount
        self.target = target
    def __str__(self):
        return self.description
EFFECT_MONEY = "money"
EFFECT_MOVE_TO = "move_to"
EFFECT_MOVE_BACK = "move_back"
EFFECT_GO_TO_JAIL = "go_to_jail"
EFFECT_GET_OUT_OF_JAIL = "get_out_of_jail"
EFFECT_COLLECT_FROM_EACH = "collect_from_each"
EFFECT_PAY_EACH = "pay_each"
EFFECT_PAY_PER_PROPERTY = "pay_per_property"
def build_chance_deck():
    """Return a shuffled list of the simplified chance cards."""
    deck = [
        ChanceCard("Advance to GO. Collect $200.", EFFECT_MOVE_TO,
                   amount=GO_SALARY, target=Board.GO_POSITION),
        ChanceCard("Bank pays you dividend of $50.", EFFECT_MONEY, amount=50),
        ChanceCard("Go directly to Jail. Do not pass GO.", EFFECT_GO_TO_JAIL),
        ChanceCard("Get Out of Jail Free. Keep this card.", EFFECT_GET_OUT_OF_JAIL),
        ChanceCard("Collect $50 from every player.", EFFECT_COLLECT_FROM_EACH, amount=50),
        ChanceCard("Pay $50 to every player.", EFFECT_PAY_EACH, amount=50),
        ChanceCard("Pay $25 per property you own.", EFFECT_PAY_PER_PROPERTY, amount=25),
        ChanceCard("Go back 3 spaces.", EFFECT_MOVE_BACK, amount=3),
        ChanceCard("You inherit $100.", EFFECT_MONEY, amount=100),
        ChanceCard("Speeding fine: pay $75.", EFFECT_MONEY, amount=-75),
    ]
    random.shuffle(deck)
    return deck