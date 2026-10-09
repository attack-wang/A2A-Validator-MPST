'''
Player module: represents a Dou Dizhu player and manages their hand of cards.
'''
from collections import Counter
class Player:
    def __init__(self, name, is_human=False):
        self.name = name
        self.is_human = is_human
        self.hand = []
        self.is_landlord = False
    def sort_hand(self):
        self.hand.sort(key=lambda c: -c.value)
    def add_cards(self, cards):
        self.hand.extend(cards)
        self.sort_hand()
    def hand_counts(self):
        return Counter(c.value for c in self.hand)
    def has_cards(self, cards):
        need = Counter(c.value for c in cards)
        have = self.hand_counts()
        return all(have[v] >= n for v, n in need.items())
    def remove_cards(self, cards):
        if not self.has_cards(cards):
            raise ValueError('%s does not hold the requested cards' % self.name)
        for c in cards:
            for i, held in enumerate(self.hand):
                if held.value == c.value:
                    del self.hand[i]
                    break
        self.sort_hand()
    def hand_size(self):
        return len(self.hand)
    def hand_str(self):
        return ' '.join(c.rank for c in self.hand)