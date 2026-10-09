'''
Constants and configuration data for the simplified Monopoly Go! game.
'''
# --- Money ---
START_MONEY = 1500          # Cash each player starts with
GO_SALARY = 200             # Collected when passing or landing on GO
JAIL_BAIL = 50              # Cost to leave jail (added to Free Parking pot)
# --- Jail / doubles rules ---
JAIL_MAX_TURNS = 3          # Failed doubles attempts before bail is forced
MAX_DOUBLES_IN_ROW = 3      # Three doubles in a row sends you to jail
JAIL_POSITION = 6           # Board index of the "Jail / Just Visiting" square
# --- Board layout ---
# Each entry: (kind, name, price, rent)
# kind: "go" | "property" | "chance" | "jail" | "free_parking" | "go_to_jail"
# price/rent are ignored (0) for non-property spaces.
BOARD_LAYOUT = [
    ("go",           "GO",                    0,   0),
    ("property",     "Old Kent Road",        60,   4),
    ("property",     "Whitechapel Road",     60,   6),
    ("chance",       "Chance",                0,   0),
    ("property",     "The Angel Islington", 100,  10),
    ("property",     "Euston Road",          100,  12),
    ("jail",         "Jail / Just Visiting",  0,   0),
    ("property",     "Pentonville Road",     140,  16),
    ("property",     "Pall Mall",            140,  18),
    ("property",     "Whitehall",            160,  20),
    ("property",     "Northumberland Ave.",  160,  22),
    ("chance",       "Chance",                0,   0),
    ("free_parking", "Free Parking",          0,   0),
    ("property",     "Bow Street",           180,  24),
    ("property",     "Marlborough Street",   180,  26),
    ("property",     "Vine Street",          200,  30),
    ("property",     "The Strand",           220,  32),
    ("property",     "Fleet Street",         220,  34),
    ("go_to_jail",   "Go To Jail",            0,   0),
    ("property",     "Trafalgar Square",     240,  36),
    ("property",     "Leicester Square",     240,  38),
    ("property",     "Coventry Street",      260,  42),
    ("chance",       "Chance",                0,   0),
    ("property",     "Piccadilly",           280,  46),
]
# --- Chance cards ---
# Each dict maps to ChanceCard(text, effect, amount, destination,
#                              steps, to_pot, collect_go)
# effect: "move_to" | "go_to_jail" | "receive" | "pay_bank"
#         | "collect_from_players" | "move_relative" | "jail_free_card"
CHANCE_CARDS = [
    {"text": "Advance to GO! Collect $200.",                      "effect": "move_to",  "destination": 0,  "collect_go": True},
    {"text": "Go directly to Jail. Do not pass GO.",              "effect": "go_to_jail"},
    {"text": "The bank pays you a $50 dividend.",                 "effect": "receive",  "amount": 50},
    {"text": "Speeding fine! Pay $15 into the pot.",              "effect": "pay_bank", "amount": 15, "to_pot": True},
    {"text": "You won a beauty contest! Collect $25.",            "effect": "receive",  "amount": 25},
    {"text": "Doctor's fee. Pay $50.",                            "effect": "pay_bank", "amount": 50},
    {"text": "Street repairs. Pay $40 into the pot.",             "effect": "pay_bank", "amount": 40, "to_pot": True},
    {"text": "It's your birthday! Collect $10 from each player.", "effect": "collect_from_players", "amount": 10},
    {"text": "Go back 3 spaces.",                                 "effect": "move_relative", "steps": -3},
    {"text": "Get Out of Jail Free! Keep this card.",             "effect": "jail_free_card"},
    {"text": "Take a stroll to Free Parking.",                    "effect": "move_to",  "destination": 12},
    {"text": "Advance to Piccadilly.",                            "effect": "move_to",  "destination": 23},
]