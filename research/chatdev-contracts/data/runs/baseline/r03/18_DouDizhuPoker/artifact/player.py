class Player:
    def __init__(self, name, is_human=False):
        self.name = name
        self.is_human = is_human
        self.hand = []
        self.is_landlord = False
    def receive_cards(self, cards):
        self.hand.extend(cards)
        self.sort_hand()
    def sort_hand(self):
        self.hand.sort(key=lambda c: c.rank_value)  # ascending? or descending for display