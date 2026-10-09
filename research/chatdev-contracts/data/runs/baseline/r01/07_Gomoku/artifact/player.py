'''
player.py
This module defines the Player entity for the Gomoku game. Each player owns a
unique numeric identifier, a display name, and the rendering color of their
stones. It also provides helpers to resolve the opponent of a player and a
factory function to build Player instances from numeric cell values.
'''
from constants import (PLAYER_EMPTY, PLAYER_BLACK, PLAYER_WHITE,
                       BLACK_STONE_COLOR, WHITE_STONE_COLOR)
class Player:
    """Represents one of the two Gomoku players (Black or White)."""
    _registry = {
        PLAYER_BLACK: ("Black", BLACK_STONE_COLOR),
        PLAYER_WHITE: ("White", WHITE_STONE_COLOR),
    }
    def __init__(self, player_id):
        if player_id not in self._registry:
            raise ValueError(f"Invalid player id: {player_id}")
        self._player_id = player_id
        self._name, self._color = self._registry[player_id]
    @property
    def player_id(self):
        return self._player_id
    @property
    def name(self):
        return self._name
    @property
    def color(self):
        return self._color
    @property
    def opponent(self):
        """Return the Player instance of the opposing side."""
        other_id = PLAYER_WHITE if self._player_id == PLAYER_BLACK else PLAYER_BLACK
        return Player(other_id)
    def __eq__(self, other):
        return isinstance(other, Player) and self._player_id == other.player_id
    def __hash__(self):
        return hash(self._player_id)
    def __repr__(self):
        return f"Player(id={self._player_id}, name={self._name})"
def get_player_by_id(player_id):
    """Factory helper: return a Player for a numeric id, or None for empty cells."""
    if player_id is None or player_id == PLAYER_EMPTY:
        return None
    if player_id in (PLAYER_BLACK, PLAYER_WHITE):
        return Player(player_id)
    return None