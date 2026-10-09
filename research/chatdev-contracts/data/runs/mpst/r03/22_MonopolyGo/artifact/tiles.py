'''
tiles.py: board tile definitions — base Tile class and all specialised tiles.
'''
class Tile:
    """Base class for every square on the board."""
    def __init__(self, name, position):
        """Store the tile's display name and its fixed board position."""
        self.name = name
        self.position = position
    def land_on(self, game, player):
        """Action performed when `player` lands on this tile.
        The base tile has no special effect; subclasses override this.
        """
        print(f"{player.name} landed on {self.name}. Nothing special happens.")
    def short_name(self):
        """Return a compact label used when rendering the board."""
        return self.name
class PropertyTile(Tile):
    """A purchasable property that pays rent to its owner."""
    def __init__(self, name, position, price, rent):
        """Create a property with a price, base rent and no owner yet."""
        super().__init__(name, position)
        self.price = price
        self.rent = rent
        self.owner = None
    @property
    def is_owned(self):
        """True when some player owns this property."""
        return self.owner is not None
    def land_on(self, game, player):
        """Handle buying, resting at home, or paying rent on this property."""
        if not self.is_owned:
            game.prompt_buy_property(player, self)
        elif self.owner is player:
            print(f"{player.name} is at home on their own property {self.name}.")
        elif self.owner.bankrupt:
            # Ownership is cleared on bankruptcy; this is a safety net.
            self.owner = None
            game.prompt_buy_property(player, self)
        else:
            rent = self.rent
            print(f"{self.name} is owned by {self.owner.name}. Rent due: ${rent}")
            game.transfer(player, self.owner, rent)
    def short_name(self):
        """Show the property's initials plus its owner tag on the board."""
        tag = self.owner.name[0].upper() if self.owner else "-"
        return f"{self.name[:6]}({tag})"
class GoTile(Tile):
    """The GO corner: salary is collected automatically while passing."""
    def land_on(self, game, player):
        """Announce landing on GO (the $200 salary is paid while passing)."""
        print(f"{player.name} landed on GO. (Salary already collected for passing.)")
class JailTile(Tile):
    """The jail square: players here are 'just visiting' unless sent to jail."""
    def land_on(self, game, player):
        """Landing here by normal movement is only a visit."""
        print(f"{player.name} is just visiting jail.")
class GoToJailTile(Tile):
    """Sends any player who lands on it directly to jail."""
    def land_on(self, game, player):
        """Teleport the player to jail without collecting a GO salary."""
        print(f"{player.name} is sent directly to jail!")
        game.send_player_to_jail(player)
class FreeParkingTile(Tile):
    """Free Parking: the landing player collects any accumulated pot."""
    def land_on(self, game, player):
        """Pay the accumulated Free Parking pot to the landing player."""
        pot = game.free_parking_pot
        if pot > 0:
            print(f"{player.name} lands on Free Parking and collects the pot of ${pot}!")
            player.receive(pot)
            game.free_parking_pot = 0
        else:
            print(f"{player.name} is resting at Free Parking. The pot is empty.")
class ChanceTile(Tile):
    """A chance square: drawing a card triggers a random event."""
    def land_on(self, game, player):
        """Draw and resolve the top card of the chance deck."""
        print(f"{player.name} landed on Chance!")
        game.draw_chance(player)