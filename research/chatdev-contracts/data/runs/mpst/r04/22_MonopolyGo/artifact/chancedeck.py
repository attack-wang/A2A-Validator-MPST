'''chancedeck.py — Simplified chance cards with a closed set of executable actions.'''
import random
# Closed set of actions: "money" | "move" | "move_to" | "go_to_jail" | "jail_card"
CHANCE_CARDS = [
    {"action": "money", "amount": 100, "text": "Bank error in your favour. Collect $100."},
    {"action": "money", "amount": -50, "text": "Doctor's fee. Pay $50."},
    {"action": "money", "amount": 150, "text": "Your building loan matures. Collect $150."},
    {"action": "money", "amount": -100, "text": "Pay school fees of $100."},
    {"action": "move", "steps": 3, "text": "Advance 3 spaces."},
    {"action": "move", "steps": -3, "text": "Go back 3 spaces."},
    {"action": "move_to", "position": 0, "text": "Advance to GO. Collect $200."},
    {"action": "move_to", "position": 23, "text": "Take a stroll to Boardwalk."},
    {"action": "go_to_jail", "text": "Go directly to Jail. Do not pass GO, do not collect $200."},
    {"action": "jail_card", "text": "Get out of Jail free. Keep this card until needed."},
]
class ChanceCard:
    def __init__(self, text, action, **params):
        self.text = text
        self.action = action
        self.params = params
    def __str__(self):
        return self.text
class ChanceDeck:
    def __init__(self, rng=None):
        self.rng = rng or random.Random()
        self._cards = [ChanceCard(spec["text"], spec["action"], **{k: v for k, v in spec.items() if k not in ("text", "action")}) for spec in CHANCE_CARDS]
        self._draw_pile = []
        self.reset()
    def reset(self):
        self._draw_pile = list(self._cards)
        self.rng.shuffle(self._draw_pile)
    def draw(self):
        if not self._draw_pile:
            self.reset()
        return self._draw_pile.pop()