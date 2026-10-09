'''
chance.py
Defines ChanceCard and ChanceDeck for the simplified chance events.
Each card has a description and an effect that is dispatched by the
game engine when drawn.
'''
import random
class ChanceCard:
    def __init__(self, description, effect, amount=0, target=None):
        self.description = description
        self.effect = effect  # 'money', 'move_to', 'move_back', 'go_to_jail',
                              # 'collect_from_each', 'pay_each', 'repair', 'jail_free'
        self.amount = amount
        self.target = target  # space name for 'move_to'
    def apply(self, game, player):
        if self.effect == 'money':
            if self.amount >= 0:
                player.receive(self.amount)
                game.log(f"  {player.name} receives ${self.amount}.")
            else:
                game.pay_to_bank(player, -self.amount, self.description)
        elif self.effect == 'move_to':
            game.move_player_to(player, self.target)
        elif self.effect == 'move_back':
            game.move_player(player, -self.amount)
            game.handle_landing(player)
        elif self.effect == 'go_to_jail':
            game.send_to_jail(player)
        elif self.effect == 'collect_from_each':
            game.collect_from_each(player, self.amount)
        elif self.effect == 'pay_each':
            game.pay_each_player(player, self.amount)
        elif self.effect == 'repair':
            cost = self.amount * len(player.properties)
            if cost > 0:
                game.pay_to_bank(player, cost,
                                 f"street repairs ({len(player.properties)} properties x ${self.amount})")
            else:
                game.log(f"  {player.name} owns no properties — no repair cost.")
        elif self.effect == 'jail_free':
            player.get_out_of_jail_cards += 1
            game.log(f"  {player.name} keeps a Get Out of Jail Free card.")
        return self.description
class ChanceDeck:
    def __init__(self):
        self.cards = [
            ChanceCard("Bank pays you a dividend of $50.", 'money', 50),
            ChanceCard("You win a coding contest: collect $100.", 'money', 100),
            ChanceCard("Pay a $50 speeding fine.", 'money', -50),
            ChanceCard("Pay hospital fees of $100.", 'money', -100),
            ChanceCard("Advance to GO! Collect $200.", 'move_to', 0, 'GO'),
            ChanceCard("Take a stroll to Free Parking.", 'move_to', 0, 'Free Parking'),
            ChanceCard("Go back 3 spaces.", 'move_back', 3),
            ChanceCard("Go directly to Jail. Do not pass GO.", 'go_to_jail', 0),
            ChanceCard("It's your birthday! Collect $25 from each player.", 'collect_from_each', 25),
            ChanceCard("Charity drive: pay each player $20.", 'pay_each', 20),
            ChanceCard("Street repairs: pay $25 per property you own.", 'repair', 25),
            ChanceCard("Get Out of Jail Free — keep this card until needed.", 'jail_free', 0),
        ]
        random.shuffle(self.cards)
        self.index = 0
    def draw(self):
        card = self.cards[self.index]
        self.index = (self.index + 1) % len(self.cards)
        return card