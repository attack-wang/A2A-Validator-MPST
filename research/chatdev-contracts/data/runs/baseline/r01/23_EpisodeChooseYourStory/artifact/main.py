def main():
    while True:
        show menu
        choice = input...
        1 → new_game(); 2 → load_game_menu(); 3 → break
    print farewell
def new_game():
    slot = input("Name your save slot (Enter for 'quicksave'): ").strip() or "quicksave"
    state = GameState()
    engine = StoryEngine(STORY_DATA, state)
    engine.save_handler = lambda: SaveManager.save_game(engine.game_state, slot)
    try:
        engine.run()
    except QuitGame:
        print("Returning to main menu...")  # or farewell
    except ValueError as e: print error
def load_game():
    saves = SaveManager.list_saves()
    if not saves: print("No saves found."); return
    list them; pick number; 
    data = SaveManager.load_game(saves[i])
    state = GameState.from_dict(data["game_state"])
    engine = StoryEngine(STORY_DATA, state)
    engine.save_handler = ...
    engine.run() with try/except