class Space:
    def __init__(self, name, position):
        self.name = name
        self.position = position
    def land_on(self, player, game):
        game.log(f"{player.name} lands on {self.name}. Nothing happens.")
    def __str__(self):
        return self.name
class GoSpace(Space):
    def land_on(self, player, game):
        game.log(f"{player.name} lands exactly on GO.")
class Property(Space):
    def __init__(self, name, position, price, rent):
        super().__init__(name, position)
        self.price = price
        self.rent = rent
        self.owner = None
    def land_on(self, player, game):
        if self.owner is None:
            game.offer_property_purchase(player, self)
        elif self.owner is player:
            game.log(f"{player.name} landed on own property {self.name}.")
        else:
            game.charge_rent(player, self)
class ChanceSpace(Space):
    def land_on(self, player, game):
        game.log(f"{player.name} lands on Chance.")
        game.draw_chance(player)
class JailSpace(Space):
    def land_on(self, player, game):
        game.log(f"{player.name} is just visiting jail.")
class GoToJailSpace(Space):
    def land_on(self, player, game):
        game.log(f"{player.name} landed on Go To Jail!")
        game.send_to_jail(player)
class FreeParkingSpace(Space):
    def land_on(self, player, game):
        game.collect_free_parking(player)
class TaxSpace(Space):
    def __init__(self, name, position, amount):
        super().__init__(name, position)
        self.amount = amount
    def land_on(self, player, game):
        game.pay_to_pot(player, self.amount, f"{self.name}")
def build_board():
    spaces = [
        GoSpace("GO", 0),
        Property("Mediterranean Avenue", 1, 60, 10),
        ChanceSpace("Chance", 2),
        Property("Baltic Avenue", 3, 60, 12),
        TaxSpace("Income Tax", 4, 100),
        Property("Oriental Avenue", 5, 100, 20),
        JailSpace("Jail / Just Visiting", 6),
        Property("Vermont Avenue", 7, 100, 22),
        ChanceSpace("Chance", 8),
        Property("Connecticut Avenue", 9, 120, 25),
        FreeParkingSpace("Free Parking", 10),
        Property("St. Charles Place", 11, 140, 30),
        Property("States Avenue", 12, 140, 30),
        ChanceSpace("Chance", 13),
        Property("Virginia Avenue", 14, 160, 35),
        GoToJailSpace("Go To Jail", 15),
        Property("St. James Place", 16, 180, 40),
        TaxSpace("Luxury Tax", 17, 75),
        Property("Tennessee Avenue", 18, 180, 40),
        ChanceSpace("Chance", 19),
        Property("New York Avenue", 20, 200, 45),
        Property("Kentucky Avenue", 21, 220, 50),
        ChanceSpace("Chance", 22),
        Property("Boardwalk", 23, 400, 80),
    ]
    return spaces
class Board:
    def __init__(self):
        self.spaces = build_board()
        self.jail_position = next(
            s.position for s in self.spaces if isinstance(s, JailSpace)
        )
    def __len__(self):
        return len(self.spaces)
    def get_space(self, position):
        return self.spaces[position % len(self.spaces)]
    def display(self, players):
        print("\n--- BOARD ---")
        for space in self.spaces:
            line = f"  {space.position:>2}. {space.name}"
            if getattr(space, "owner", None) is not None:
                line += f" [owner: {space.owner.name}]"
            elif isinstance(space, Property):
                line += f" [for sale: ${space.price}, rent: ${space.rent}]"
            here = [p.name for p in players if p.position == space.position and not p.bankrupt]
            if here:
                line += f"  <{', '.join(here)}>"
            print(line)