import random
from card import Card, RANK_NAMES
def build_deck():
    deck = []
    for rank in range(3, 16):  # 3..15 (2)
        for suit in SUITS:
            deck.append(Card(rank, suit))
    deck.append(Card(16))  # small joker
    deck.append(Card(17))  # big joker
    return deck
def deal():
    deck = build_deck()
    random.shuffle(deck)
    hands = [sorted(deck[i*17:(i+1)*17], key=lambda c: -c.rank) for i in range(3)]
    kitty = deck[51:54]
    return hands, kitty