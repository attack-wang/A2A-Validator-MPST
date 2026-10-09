'''
ui.py
Text-based user interface helpers: banners, status displays,
dice results, card reveals and input prompts.
'''
def banner():
    print("\n" + "=" * 60)
def show_round(round_num, max_rounds):
    print(f"\n--- ROUND {round_num} / {max_rounds} " + "-" * 30)
def show_player_summary(players):
    print("Player status:")
    for p in players:
        props = ", ".join(prop.name for prop in p.properties) or "none"
        jail = " [IN JAIL]" if p.in_jail else ""
        bank = " [BANKRUPT]" if p.bankrupt else ""
        print(f"  {p.name}: ${p.money}{jail}{bank} | Properties: {props}")
def show_turn_header(player):
    print(f"\n>>> {player.name}'s turn (money: ${player.money}, position: {player.position})")
def show_dice_roll(d1, d2, total, is_doubles):
    print(f"  Rolled: [{d1}] + [{d2}] = {total}" + (" (DOUBLES!)" if is_doubles else ""))
def show_message(text):
    print(f"  * {text}")
def show_card(card):
    print(f"  ~ CHANCE CARD ~ {card.text}")
def prompt(message):
    return input(message).strip()
def prompt_yes_no(message):
    while True:
        answer = input(f"{message} [y/n]: ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")
def show_property_card(prop):
    print(f"  {prop}")
def show_board(board, players):
    print("\n  BOARD:")
    for i, space in enumerate(board.spaces):
        here = [p.name for p in players if p.position == i and p.is_active]
        tokens = f" <- {', '.join(here)}" if here else ""
        print(f"   [{i:2d}] {space}{tokens}")