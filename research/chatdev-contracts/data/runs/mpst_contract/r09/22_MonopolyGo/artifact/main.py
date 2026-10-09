#!/usr/bin/env python3
"""Simplified Monopoly Go! - console game."""
import random

BOARD = [
    ("GO", "go", 0, 0),
    ("Mediterranean Avenue", "prop", 60, 2),
    ("Chance", "chance", 0, 0),
    ("Baltic Avenue", "prop", 60, 4),
    ("Income Tax", "tax", 100, 0),
    ("Reading Railroad", "prop", 200, 25),
    ("Oriental Avenue", "prop", 100, 6),
    ("Chance", "chance", 0, 0),
    ("Vermont Avenue", "prop", 100, 6),
    ("Connecticut Avenue", "prop", 120, 8),
    ("Jail", "jail", 0, 0),
    ("St. Charles Place", "prop", 140, 10),
    ("Electric Company", "prop", 150, 12),
    ("Chance", "chance", 0, 0),
    ("States Avenue", "prop", 140, 10),
    ("Virginia Avenue", "prop", 160, 12),
    ("Free Parking", "parking", 0, 0),
    ("St. James Place", "prop", 180, 14),
    ("Tennessee Avenue", "prop", 180, 14),
    ("Chance", "chance", 0, 0),
    ("New York Avenue", "prop", 200, 16),
    ("Go To Jail", "gotojail", 0, 0),
    ("Kentucky Avenue", "prop", 220, 18),
    ("Boardwalk", "prop", 400, 50),
]

CHANCE = [
    ("Bank pays you a dividend of $50.", 50),
    ("Advance to GO and collect $200.", "go"),
    ("Go directly to Jail! Do not pass GO.", "jail"),
    ("Pay hospital fees of $100.", -100),
    ("Speeding fine: pay $15.", -15),
    ("You won a beauty contest: collect $10.", 10),
    ("Building loan matures: collect $150.", 150),
    ("Go back 3 spaces.", -3),
]

GO_POS, JAIL_POS = 0, 10


class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.pos = 0
        self.jail = False
        self.jail_turns = 0
        self.alive = True
        self.owned = []

    def net_worth(self):
        return self.money + sum(BOARD[p][2] for p in self.owned)


class Game:
    def __init__(self, names):
        self.players = [Player(n) for n in names]
        self.owner = {}  # board position -> player index
        self.pot = 0
        self.round = 0

    def info(self):
        print("\n--- Status: Round %d ---" % self.round)
        for i, p in enumerate(self.players):
            props = ", ".join(BOARD[o][0] for o in p.owned) or "none"
            state = " (IN JAIL)" if p.jail else ("" if p.alive else " (BANKRUPT)")
            print("%d. %-12s $%-5d at %-22s owns: [%s]%s"
                  % (i + 1, p.name, p.money, BOARD[p.pos][0], props, state))

    def pay(self, p, amount, to=None):
        p.money -= amount
        if to is not None:
            to.money += amount
        if p.money < 0:
            self.bankrupt(p)

    def bankrupt(self, p):
        print("*** %s is BANKRUPT and eliminated! ***" % p.name)
        p.alive = False
        idx = self.players.index(p)
        for pos in list(self.owner):
            if self.owner[pos] == idx:
                del self.owner[pos]
        p.owned = []

    def send_jail(self, p):
        print("%s is sent directly to Jail!" % p.name)
        p.pos = JAIL_POS
        p.jail = True
        p.jail_turns = 0

    def move(self, p, steps):
        old = p.pos
        p.pos = (old + steps) % len(BOARD)
        if old + steps >= len(BOARD):
            print("%s passed GO and collects $200." % p.name)
            p.money += 200
        self.land(p)

    def land(self, p):
        name, kind, price, rent = BOARD[p.pos]
        print("%s landed on %s." % (p.name, name))
        if kind == "prop":
            if p.pos in self.owner:
                o = self.players[self.owner[p.pos]]
                if o is not p and o.alive:
                    print("%s pays $%d rent to %s." % (p.name, rent, o.name))
                    self.pay(p, rent, o)
                elif o is p:
                    print("%s owns this property." % p.name)
            elif p.money >= price:
                ans = input("Buy %s for $%d (rent $%d)? (y/n) "
                            % (name, price, rent)).strip().lower()
                if ans.startswith("y"):
                    p.money -= price
                    p.owned.append(p.pos)
                    self.owner[p.pos] = self.players.index(p)
                    print("%s bought %s." % (p.name, name))
                else:
                    print("%s declined to buy." % p.name)
            else:
                print("%s cannot afford %s ($%d)." % (p.name, name, price))
        elif kind == "tax":
            print("%s pays $%d tax into the Free Parking pot." % (p.name, price))
            self.pay(p, price)
            self.pot += price
        elif kind == "gotojail":
            self.send_jail(p)
        elif kind == "parking":
            if self.pot:
                print("%s collects $%d from the Free Parking pot!" % (p.name, self.pot))
                p.money += self.pot
                self.pot = 0
            else:
                print("Free Parking: pot is empty, rest easy.")
        elif kind == "chance":
            self.chance(p)

    def chance(self, p):
        desc, effect = random.choice(CHANCE)
        print("CHANCE CARD: %s" % desc)
        if effect == "go":
            p.pos = GO_POS
            p.money += 200
        elif effect == "jail":
            self.send_jail(p)
        elif effect == -3:
            p.pos = (p.pos - 3) % len(BOARD)
            self.land(p)
        elif effect > 0:
            p.money += effect
        else:
            self.pay(p, -effect)
            self.pot += -effect

    def turn(self, p):
        print("\n=== %s's turn (money $%d, at %s) ==="
              % (p.name, p.money, BOARD[p.pos][0]))
        if p.jail:
            choice = ""
            while choice not in ("p", "r"):
                choice = input("In jail (attempt %d/3): (p)ay $50 or (r)oll for doubles? "
                               % (p.jail_turns + 1)).strip().lower()
            if choice == "p" and p.money >= 50:
                p.money -= 50
                p.jail = False
                print("%s paid $50 and leaves jail." % p.name)
            else:
                d1, d2 = random.randint(1, 6), random.randint(1, 6)
                print("%s rolled %d and %d." % (p.name, d1, d2))
                if d1 == d2:
                    p.jail = False
                    print("Doubles! %s leaves jail and moves." % p.name)
                    self.move(p, d1 + d2)
                else:
                    p.jail_turns += 1
                    if p.jail_turns >= 3:
                        print("Third failed attempt: %s must pay $50." % p.name)
                        p.money -= 50
                        p.jail = False
                        if p.money < 0:
                            self.bankrupt(p)
                            return
                        self.move(p, d1 + d2)
                    else:
                        print("%s stays in jail." % p.name)
                return
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        print("%s rolled %d and %d (total %d)." % (p.name, d1, d2, d1 + d2))
        self.move(p, d1 + d2)

    def over(self):
        return sum(1 for p in self.players if p.alive) <= 1

    def play(self, max_rounds=20):
        print("Welcome to Simplified Monopoly Go! "
              "(Game ends after %d rounds or when one player remains.)" % max_rounds)
        while self.round < max_rounds:
            self.round += 1
            self.info()
            for p in self.players:
                if p.alive:
                    self.turn(p)
                if self.over():
                    break
            if self.over():
                break
        self.finish()

    def finish(self):
        alive = [p for p in self.players if p.alive]
        print("\n=== GAME OVER ===")
        if len(alive) == 1:
            print("Winner: %s! All rivals went bankrupt." % alive[0].name)
        else:
            best = max(alive, key=Player.net_worth)
            print("Time is up! Richest player wins: %s (net worth $%d)"
                  % (best.name, best.net_worth()))
        print("Final standings:")
        for p in sorted(self.players, key=Player.net_worth, reverse=True):
            print("%-12s money $%-5d net worth $%d %s"
                  % (p.name, p.money, p.net_worth(),
                     "(bankrupt)" if not p.alive else ""))


def main():
    print("Simplified Monopoly Go!")
    n = 0
    while not 2 <= n <= 4:
        try:
            n = int(input("Number of players (2-4): "))
        except ValueError:
            n = 0
    names = []
    for i in range(n):
        d = input("Name of player %d: " % (i + 1)).strip()
        names.append(d or "Player %d" % (i + 1))
    Game(names).play()


if __name__ == "__main__":
    main()