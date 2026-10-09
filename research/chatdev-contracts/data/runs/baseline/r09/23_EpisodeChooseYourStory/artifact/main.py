def main():
    ui = ConsoleUI()
    print banner
    choice = input("(N)ew journey or (L)oad saved journey? ").strip().lower()
    state = None
    if choice == "l" and os.path.exists(SAVE_FILE):
        with open... data = json.load
        state = GameState.from_dict(data)
        print("Journey restored.")
    if state is None:
        name = input("What name do travelers know you by? (Enter for 'Traveler') ").strip() or "Traveler"
        state = GameState(player_name=name, coins=5)
    engine = StoryEngine(STORY, state, ui)
    replay loop:
    while True:
        engine.run()
        save chronicle
        again = input("Begin a new journey? (y/n) ")
        if again == 'y': state = fresh; engine = new StoryEngine...
        else break