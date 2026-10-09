'''Player module: represents a Dou Dizhu player with hand management and actions.'''
from card import Card
class Player:
    def __init__(self, name, is_human=False):
        self.name = name
        self.is_human = is_human
        self.hand = []
        self.role = 'peasant'  # or 'landlord'
        self.bid = 0  # current bid in bidding phase
    def receive_cards(self, cards):
        self.hand.extend(cards)
        self.sort_hand()
    def sort_hand(self):
        self.hand.sort(key=lambda c: c.value, reverse=True)
    def is_empty(self):
        return len(self.hand) == 0
    def remove_cards(self, cards):
        for c in cards:
            self.hand.remove(c)
        # hand stays sorted
    def has_card(self, card): ...
    def find_card_by_rank(self, rank): ...