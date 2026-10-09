"""Game class implementing the Dou Dizhu game flow."""
import random
from constants import CombType, RANK_VALUE, VALUE_RANK
from card import Card, Deck
from combination import Combination, identify
from player import Player
class Game:
    def __init__(self, human_names=("You",)):
        self.players = [...]
        self.landlord_index = None
        self.bottom = []
        self.current = None
        self.active = None  # current Combination on table
        self.active_owner = None
        self.pass_count = 0
        self.winner = None