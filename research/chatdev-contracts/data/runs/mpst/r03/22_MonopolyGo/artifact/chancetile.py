class Tile:
    def __init__(self, name, position):
        self.name = name
        self.position = position
    def land_on(self, game, player):
        print(f"{player.name} landed on {self.name}. Nothing special happens.")
    def short_name(self):
        return self.name
class PropertyTile(Tile):
    def __init__(self, name, position, price, rent):
        super().__init__(name, position)
        self.price = price
        self.rent = rent
        self.owner = None
    @property
    def is_owned(self):
        return self.owner is not None
    def land_on(self, game, player):
        if not self.is_owned:
            game.prompt_buy_property(player, self)
        elif self.owner is player:
            print(f"{player.name} is at home on their own property {self.name}.")
        elif self.owner.bankrupt:
            # shouldn't happen since bankrupt clears ownership
            self.owner = None
            game.prompt_buy_property(player, self)
        else:
            rent = self.rent
            print(f"{self.name} is owned by {self.owner.name}. Rent due: ${rent}")
            game.transfer(player, self.owner, rent)
class GoTile(Tile):
    def land_on(self, game, player):
        print(f"{player.name} landed on GO. (Salary already collected for passing.)")
class JailTile(Tile):
    def land_on(self, game, player):
        print(f"{player.name} is just visiting jail.")
class GoToJailTile(Tile):
    def land_on(self, game, player):
        print(f"{player.name} is sent directly to jail!")
        game.send_player_to_jail(player)
class FreeParkingTile(Tile):
    def land_on(self, game, player):
        pot = game.free_parking_pot
        if pot > 0:
            print(f"{player.name} lands on Free Parking and collects the pot of ${pot}!")
            player.receive(pot)
            game.free_parking_pot = 0
        else:
            print(f"{player.name} is resting at Free Parking. The pot is empty.")
class ChanceTile(Tile):
    def land_on(self, game, player):
        print(f"{player.name} landed on Chance!")
        game.draw_chance(player)