'''
chance.py
Chance module for the simplified Monopoly Go! game.
Defines ChanceCard and ChanceDeck. Each card is described by a message
plus an effect code that the Game interprets when the card is drawn.
'''
import random
class ChanceCard:
    """A single chance card: a message plus the effect it triggers."""
    # Effect codes understood by the Game class.
    EFFECTS = {
        "COLLECT",        # player receives `amount`
        "PAY",            # player pays `amount` (to bank / free parking pot)
        "MOVE",           # player moves forward `steps` spaces
        "MOVE_BACK",      # player moves back `steps` spaces
        "GO_TO",          # player moves directly to `target` space kind
        "GO_TO_JAIL",     # player is sent to jail
    }
    def __init__(self, message, effect, amount=0, steps=0, target=None):
        self.message = message
        self.effect = effect
        self.amount = amount
        self.steps = steps
        self.target = target
    def __str__(self):
        return self.message
class ChanceDeck:
    """A shuffled deck of chance cards with draw/refill behaviour."""
    def __init__(self, cards=None):
        if cards is None:
            cards = ChanceDeck.default_cards()
        self._cards = list(cards)
        random.shuffle(self._cards)
    def draw(self):
        """Draw the top card, reshuffling the discard pile when empty."""
        if not self._cards:
            self._cards = ChanceDeck.default_cards()
            random.shuffle(self._cards)
        return self._cards.pop(0)
    @staticmethod
    def default_cards():
        return [
            ChanceCard("Advance to GO! Collect $200.", "GO_TO", target="go"),
            ChanceCard("Go directly to Jail. Do not pass GO, do not collect $200.", "GO_TO_JAIL"),
            ChanceCard("Bank error in your favor. Collect $100.", "COLLECT", amount=100),
            ChanceCard("Doctor's fee. Pay $50.", "PAY", amount=50),
            ChanceCard("Speeding fine. Pay $30.", "PAY", amount=30),
            ChanceCard("You won a beauty contest! Collect $25.", "COLLECT", amount=25),
            ChanceCard("Bank pays you a dividend of $50.", "COLLECT", amount=50),
            ChanceCard("Go back 3 spaces.", "MOVE_BACK", steps=3),
            ChanceCard("Take a stroll — advance 5 spaces.", "MOVE", steps=5),
            ChanceCard("Holiday fund matures. Collect $150.", "COLLECT", amount=150),
            ChanceCard("Pay school fees of $40.", "PAY", amount=40),
            ChanceCard("Your building loan matures. Collect $75.", "COLLECT", amount=75),
        ]