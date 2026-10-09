"""Central configuration for the simplified Monopoly Go! game.
All board-geometry constants are defined FIRST so that later
structures (BOARD_LAYOUT, CHANCE_CARDS) can safely reference them
at import time.
"""
import random
# --- Board geometry (must be defined before BOARD_LAYOUT / CHANCE_CARDS) ---
BOARD_SIZE = 24
GO_POSITION = 0
JAIL_POSITION = 6
FREE_PARKING_POSITION = 12
GO_TO_JAIL_POSITION = 18
# --- Space types ---
TYPE_GO = "GO"
TYPE_PROPERTY = "PROPERTY"
TYPE_CHANCE = "CHANCE"
TYPE_JAIL = "JAIL"
TYPE_FREE_PARKING = "FREE_PARKING"
TYPE_TAX = "TAX"
TYPE_GO_TO_JAIL = "GO_TO_JAIL"
# --- Rules ---
STARTING_MONEY = 1500
GO_SALARY = 200
JAIL_FINE = 50
JAIL_MAX_TURNS = 3
TAX_AMOUNT = 100
FREE_PARKING_POT_ENABLED = True
DOUBLES_LIMIT = 3
# --- Players ---
MIN_PLAYERS = 2
MAX_PLAYERS = 4
PLAYER_TOKENS = ["Dog", "Car", "Hat", "Boat"]
# --- Board layout: (type, name, price) per index ---
BOARD_LAYOUT = [
    (TYPE_GO, "Go", 0),                              # 0
    (TYPE_PROPERTY, "Mediterranean Ave", 60),        # 1
    (TYPE_CHANCE, "Chance", 0),                      # 2
    (TYPE_PROPERTY, "Baltic Ave", 60),               # 3
    (TYPE_TAX, "Income Tax", TAX_AMOUNT),            # 4
    (TYPE_CHANCE, "Chance", 0),                      # 5
    (TYPE_JAIL, "Jail / Just Visiting", 0),          # 6  = JAIL_POSITION
    (TYPE_PROPERTY, "Oriental Ave", 100),            # 7
    (TYPE_CHANCE, "Chance", 0),                      # 8
    (TYPE_PROPERTY, "Vermont Ave", 100),             # 9
    (TYPE_PROPERTY, "Connecticut Ave", 120),         # 10
    (TYPE_CHANCE, "Chance", 0),                      # 11
    (TYPE_FREE_PARKING, "Free Parking", 0),          # 12 = FREE_PARKING_POSITION
    (TYPE_PROPERTY, "St. Charles Place", 140),       # 13
    (TYPE_CHANCE, "Chance", 0),                      # 14
    (TYPE_PROPERTY, "States Ave", 140),              # 15
    (TYPE_PROPERTY, "Virginia Ave", 160),            # 16
    (TYPE_CHANCE, "Chance", 0),                      # 17
    (TYPE_GO_TO_JAIL, "Go To Jail", 0),              # 18 = GO_TO_JAIL_POSITION
    (TYPE_PROPERTY, "St. James Place", 180),         # 19
    (TYPE_CHANCE, "Chance", 0),                      # 20
    (TYPE_PROPERTY, "Tennessee Ave", 180),           # 21
    (TYPE_PROPERTY, "New York Ave", 200),            # 22
    (TYPE_CHANCE, "Chance", 0),                      # 23
]
# --- Chance card actions ---
CHANCE_GAIN = "GAIN"
CHANCE_LOSE = "LOSE"
CHANCE_MOVE = "MOVE"
CHANCE_GOTO = "GOTO"
CHANCE_GOTO_JAIL = "JAIL"
# --- Chance cards (safe: all referenced constants defined above) ---
CHANCE_CARDS = [
    ("Bank error in your favour — collect $100.", CHANCE_GAIN, 100),
    ("Doctor's fee — pay $50.", CHANCE_LOSE, 50),
    ("Birthday gift — collect $75.", CHANCE_GAIN, 75),
    ("Speeding fine — pay $75.", CHANCE_LOSE, 75),
    ("Advance to GO — collect $200.", CHANCE_GOTO, GO_POSITION),
    ("Take a stroll — advance 3 spaces.", CHANCE_MOVE, 3),
    ("Slip on ice — move back 3 spaces.", CHANCE_MOVE, -3),
    ("Go directly to Jail — do not pass GO.", CHANCE_GOTO_JAIL, JAIL_POSITION),
    ("Tax refund — collect $50.", CHANCE_GAIN, 50),
    ("Charity donation — pay $100.", CHANCE_LOSE, 100),
    ("Holiday fund matures — collect $150.", CHANCE_GAIN, 150),
    ("Street repairs — pay $40.", CHANCE_LOSE, 40),
]