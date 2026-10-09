'''
game.py
Game engine: dealing, bidding phase, turn management with pass-or-beat
enforcement, and win/lose detection for a 3-player Dou Dizhu match.
'''
import random
from card import build_deck
from combination import Combination
from moves import generate_moves, find_moves
from player import Player
from constants import BOMB, ROCKET
class Game:
    """A full Dou Dizhu match between one human and two AI players."""
    def __init__(self, human_name='You'):
        self.players = [Player(human_name, 0), Player('AI-Alice', 1), Player('AI-Bob', 2)]
        self.kitty = []
        self.landlord = None
        self.last_combination = None
        self.last_player = None
    # ---------- setup ----------
    def deal(self):
        """Shuffle and deal 17 cards to each player; keep 3 kitty cards."""
        deck = build_deck()
        random.shuffle(deck)
        for i, p in enumerate(self.players):
            p.hand = sorted(deck[i * 17:(i + 1) * 17], key=lambda c: c.value)
        self.kitty = deck[51:]
        self.landlord = None
        self.last_combination = None
        self.last_player = None
    # ---------- bidding ----------
    def _hand_bid_score(self, hand):
        """Simple hand-strength heuristic used by AI bidding."""
        score = 0
        counts = {}
        for c in hand:
            counts[c.value] = counts.get(c.value, 0) + 1
        for v, n in counts.items():
            if v == 17:
                score += 3
            elif v == 16:
                score += 2
            elif v == 15:
                score += 1
            if n == 4:
                score += 2  # bomb
        return score
    def _ai_bid(self, player, highest):
        """AI decides a bid (0 = pass) strictly above `highest` or passes."""
        score = self._hand_bid_score(player.hand)
        wanted = 3 if score >= 7 else 2 if score >= 4 else 1 if score >= 2 else 0
        return wanted if wanted > highest else 0
    def bid(self):
        """Run the bidding phase; returns True when a landlord is chosen."""
        starter = random.randrange(3)
        order = [(starter + i) % 3 for i in range(3)]
        highest, holder = 0, None
        print('\n--- Bidding phase ---')
        for idx in order:
            p = self.players[idx]
            if idx == 0:
                while True:
                    raw = input(f'{p.name}, your bid (0=pass, 1-3, current highest={highest}): ').strip()
                    if raw in ('0', '1', '2', '3') and int(raw) > highest:
                        bid = int(raw)
                        break
                    print(f'Invalid bid. Enter 0 to pass or a number greater than {highest}.')
            else:
                bid = self._ai_bid(p, highest)
                print(f'{p.name} bids {bid}.' if bid else f'{p.name} passes.')
            if bid > highest:
                highest, holder = bid, p
            if highest == 3:
                break
        if holder is None:
            print('Everyone passed — re-dealing.')
            return False
        self.landlord = holder
        holder.is_landlord = True
        holder.hand.extend(self.kitty)
        holder.hand.sort(key=lambda c: c.value)
        print(f'{holder.name} is the landlord with bid {highest} and picks up: '
              + ' '.join(str(c) for c in self.kitty))
        return True