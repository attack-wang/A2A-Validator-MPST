class Game:
    def __init__(self, player_names)
    setup: create deck, shuffle, deal 17 each, 3 bottom cards
    bidding_phase(): rotate starting bidder (random or round-based), each player bids in turn; bidding ends when someone bids 3 or after all players have had a chance / two passes in a row. Standard simple rule: each player in turn either bids higher (1,2,3) or passes; if all pass, redeal; highest bid becomes landlord. Let me implement: starting from dealer position, players take turns; a player may pass or bid higher than current highest; if a player bids 3, bidding ends immediately; otherwise after all 3 players have acted, the highest bidder wins; if all pass, reshuffle and redeal.
    playing_phase(): landlord plays first; track current_combo and who played it; turns rotate; if two consecutive passes, the combo leader leads anew (current_combo = None).
    check win: after each play, if hand empty → game over. If landlord out → landlord wins; else peasants win.