class Player:
    def __init__(self, name, is_ai):
        self.name = name
        self.is_ai = is_ai
        self.hand = []
        self.is_landlord = False
    def hand_count(self):
        return len(self.hand)
    def remove_cards(self, cards):
        ...