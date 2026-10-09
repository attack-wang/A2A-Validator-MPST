'''
board.py: Board class that builds and manages the tile layout.
'''
from tiles import (Tile, PropertyTile, GoTile, JailTile, GoToJailTile,
                   FreeParkingTile, ChanceTile)
BOARD_SIZE = 24
class Board:
    """Builds the 24-tile loop and provides lookup/rendering helpers."""
    def __init__(self):
        """Construct the fixed tile layout."""
        self.tiles = self._build()
    def _build(self):
        """Create and return the ordered list of tiles forming the board."""
        tiles = [
            GoTile("GO", 0),
            PropertyTile("Old Kent Road", 1, 60, 10),
            PropertyTile("Mediterranean Ave", 2, 60, 10),
            ChanceTile("Chance", 3),
            PropertyTile("Baltic Ave", 4, 80, 12),
            PropertyTile("Oriental Ave", 5, 100, 15),
            JailTile("Jail", 6),
            PropertyTile("Vermont Ave", 7, 100, 15),
            PropertyTile("Connecticut Ave", 8, 120, 18),
            ChanceTile("Chance", 9),
            PropertyTile("St. Charles Place", 10, 140, 20),
            PropertyTile("States Ave", 11, 140, 20),
            FreeParkingTile("Free Parking", 12),
            PropertyTile("Virginia Ave", 13, 160, 24),
            PropertyTile("St. James Place", 14, 180, 26),
            ChanceTile("Chance", 15),
            PropertyTile("Tennessee Ave", 16, 180, 26),
            PropertyTile("New York Ave", 17, 200, 30),
            GoToJailTile("Go To Jail", 18),
            PropertyTile("Kentucky Ave", 19, 220, 32),
            PropertyTile("Indiana Ave", 20, 220, 32),
            ChanceTile("Chance", 21),
            PropertyTile("Illinois Ave", 22, 240, 36),
            PropertyTile("Atlantic Ave", 23, 260, 40),
        ]
        return tiles
    def get_tile(self, position):
        """Return the tile at `position`, wrapping around the board."""
        return self.tiles[position % len(self.tiles)]
    @property
    def size(self):
        """Return the total number of tiles on the board."""
        return len(self.tiles)
    @property
    def jail_position(self):
        """Find and return the board index of the Jail tile."""
        for tile in self.tiles:
            if isinstance(tile, JailTile):
                return tile.position
        return 6  # Fallback matching the standard layout.
    def display(self, players):
        """Render a compact table of every tile with owners and player tokens."""
        print("\n" + "=" * 62)
        print("BOARD")
        print("=" * 62)
        tokens_by_pos = {}
        for p in players:
            if not p.bankrupt:
                tokens_by_pos.setdefault(p.position, []).append(p.name)
        for tile in self.tiles:
            owner = ""
            if isinstance(tile, PropertyTile) and tile.owner is not None:
                owner = f" [Owner: {tile.owner.name}]"
            here = tokens_by_pos.get(tile.position, [])
            token_str = f" << {', '.join(here)}" if here else ""
            print(f"  {tile.position:>2}. {tile.name}{owner}{token_str}")
        print("=" * 62)