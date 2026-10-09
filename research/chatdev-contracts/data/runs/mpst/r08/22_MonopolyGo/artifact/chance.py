'''
chance.py
Chance cards and the deck used by the Monopoly Go! game.
'''
import random
class ChanceCard:
    """A single chance card with a description and an effect callable."""
    def __init__(self, description, effect):
        self.description = description
        self.effect = effect  # callable(player, game) -> str message
    def apply(self, player, game):
        """Execute the card's effect and return the resulting message."""
        return self.effect(player, game)
def _collect_50(player, game):
    """Effect: the bank pays the player $50."""
    player.receive(50)
    return f"{player.name} collects $50."
def _collect_100(player, game):
    """Effect: the bank pays the player $100."""
    player.receive(100)
    return f"{player.name} collects $100."
def _pay_pot_50(player, game):
    """Effect: the player pays a $50 fine into the Free Parking pot."""
    if player.pay(50):
        game.pot += 50
        return f"{player.name} pays a $50 fine into the pot."
    game.handle_bankruptcy(player, None)
    return f"{player.name} could not pay the fine and is bankrupt!"
def _advance_to_go(player, game):
    """Effect: teleport the player to GO and pay the GO salary."""
    passed = player.move_to(0, game.board.SIZE)
    if passed:
        player.receive(game.GO_SALARY)
    return f"{player.name} advances to GO and collects ${game.GO_SALARY}."
def _go_to_jail(player, game):
    """Effect: send the player directly to jail without passing GO."""
    game.send_to_jail(player)
    return f"{player.name} is sent directly to Jail!"
def _back_three(player, game):
    """Effect: move the player back three spaces and resolve the new space."""
    player.position = (player.position - 3) % game.board.SIZE
    game.resolve_space(player, [])
    return f"{player.name} moves back 3 spaces to {game.board.spaces[player.position].name}."
def _jail_free_card(player, game):
    """Effect: the player keeps a Get Out of Jail Free card."""
    player.get_out_of_jail_cards += 1
    return f"{player.name} keeps a 'Get Out of Jail Free' card."
class ChanceDeck:
    """A shuffled, cyclic deck of chance cards."""
    def __init__(self):
        self.cards = [
            ChanceCard("Bank error in your favor. Collect $50.", _collect_50),
            ChanceCard("You win a beauty contest. Collect $100.", _collect_100),
            ChanceCard("Speeding fine: pay $50 into the pot.", _pay_pot_50),
            ChanceCard("Advance to GO. Collect $200.", _advance_to_go),
            ChanceCard("Go directly to Jail. Do not pass GO.", _go_to_jail),
            ChanceCard("Move back 3 spaces.", _back_three),
            ChanceCard("Get Out of Jail Free. Keep this card.", _jail_free_card),
            ChanceCard("Bank pays you a dividend of $50.", _collect_50),
        ]
        self.index = 0
        random.shuffle(self.cards)
    def draw(self):
        """Return the next card in the deck, cycling forever."""
        card = self.cards[self.index]
        self.index = (self.index + 1) % len(self.cards)
        return card