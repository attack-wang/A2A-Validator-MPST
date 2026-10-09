'''
chance.py
Module defining the ChanceCard and ChanceDeck classes for the simplified
Monopoly Go! game. A ChanceCard holds a description, an effect type
("money", "advance_to_go", "move_to", "move_back" or "go_to_jail") and an
optional amount (money delta, target board position, or steps to move back).
A ChanceDeck holds a shuffled pile of cards and reshuffles automatically
when the pile is exhausted.
'''
import random
class ChanceCard:
    '''A single chance card with a description, an effect and an amount.'''
    def __init__(self, description, effect, amount=0):
        '''Initialize the card with its text, effect type and amount.'''
        self.description = description
        self.effect = effect      # "money", "advance_to_go", "move_to",
                                  # "move_back", or "go_to_jail"
        self.amount = amount      # money delta, target position, or steps back
class ChanceDeck:
    '''A shuffled deck of chance cards that reshuffles when exhausted.'''
    def __init__(self):
        '''Build the full card set and shuffle it ready for drawing.'''
        self.cards = self._build()
        self.draw_index = 0
        random.shuffle(self.cards)
    def _build(self):
        '''Create the complete set of chance cards used by the game.'''
        return [
            ChanceCard("Bank error in your favor. Collect $50.", "money", 50),
            ChanceCard("You won a beauty contest! Collect $100.", "money", 100),
            ChanceCard("Bank pays you a dividend of $150.", "money", 150),
            ChanceCard("Doctor's fee. Pay $50.", "money", -50),
            ChanceCard("Speeding fine. Pay $75.", "money", -75),
            ChanceCard("Pay hospital fees of $100.", "money", -100),
            ChanceCard("Advance to GO! Collect $200.", "advance_to_go"),
            ChanceCard("Take a stroll to Boardwalk!", "move_to", 23),
            ChanceCard("Advance to St. Charles Place.", "move_to", 11),
            ChanceCard("Take a trip to Reading Railroad.", "move_to", 5),
            ChanceCard("Go back 3 spaces.", "move_back", 3),
            ChanceCard("Go directly to Jail! Do not pass GO, do not collect $200.", "go_to_jail"),
        ]
    def draw(self):
        '''Draw the next card, reshuffling the deck when it runs out.'''
        if self.draw_index >= len(self.cards):
            random.shuffle(self.cards)
            self.draw_index = 0
        card = self.cards[self.draw_index]
        self.draw_index += 1
        return card