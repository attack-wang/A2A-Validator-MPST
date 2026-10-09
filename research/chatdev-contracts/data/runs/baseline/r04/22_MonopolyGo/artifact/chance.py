"""Chance deck for Monopoly Go!"""
import random
from game_constants import CHANCE_CARDS
class ChanceCard:
    """A single chance card with its effect parameters."""
    def __init__(self, text, effect, amount=0, destination=None, steps=0,
                 to_pot=False, collect_go=False):
        self.text = text
        self.effect = effect
        self.amount = amount
        self.destination = destination
        self.steps = steps
        self.to_pot = to_pot
        self.collect_go = collect_go
class ChanceDeck:
    """A shuffled deck that reshuffles when exhausted."""
    def __init__(self, card_data=CHANCE_CARDS):
        self.cards = [ChanceCard(**d) for d in card_data]
        self.draw_pile = []
        self.shuffle()
    def shuffle(self):
        self.draw_pile = self.cards[:]
        random.shuffle(self.draw_pile)
    def draw(self):
        if not self.draw_pile:
            self.shuffle()
        return self.draw_pile.pop()