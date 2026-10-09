'''
chance.py
Simplified chance deck.
'''
import random
class ChanceCard:
    def __init__(self, text, effect, amount=0, destination=None):
        self.text = text
        self.effect = effect  # 'money', 'move', 'move_to', 'go_to_jail', 'get_out_of_jail', 'collect_from_players'
        self.amount = amount
        self.destination = destination
class ChanceDeck:
    def __init__(self, rng=None):
        self.rng = rng or random
        self.cards = self._build()
        self.rng.shuffle(self.cards)
        self._index = 0
    def _build(self):
        return [
            ChanceCard("Advance to GO! Collect $200.", "move_to", destination=0),
            ChanceCard("Bank pays you a dividend of $50.", "money", amount=50),
            ChanceCard("Pay poor tax of $50.", "money", amount=-50),
            ChanceCard("Go directly to Jail. Do not pass GO.", "go_to_jail"),
            ChanceCard("Get Out of Jail Free. Keep this card.", "get_out_of_jail"),
            ChanceCard("Advance to Boardwalk.", "move_to", destination=39),
            ChanceCard("Advance to Illinois Avenue.", "move_to", destination=24),
            ChanceCard("Go back 3 spaces.", "move", amount=-3),
            ChanceCard("It's your birthday! Collect $10 from each player.", "collect_from_players", amount=10),
            ChanceCard("You won second prize in a beauty contest. Collect $100.", "money", amount=100),
            ChanceCard("Speeding fine: pay $15.", "money", amount=-15),
            ChanceCard("Building loan matures. Collect $150.", "money", amount=150),
            ChanceCard("Pay school fees of $150.", "money", amount=-150),
            ChanceCard("Bank error in your favor. Collect $200.", "money", amount=200),
        ]
    def draw(self):
        card = self.cards[self._index]
        self._index = (self._index + 1) % len(self.cards)
        return card