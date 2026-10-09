def main_menu(): loop: show banner, options: New Journey, Continue (list saves), Endings Collection, How to Play, Quit
def new_game(): ask name (validate non-empty, default "Wanderer"), create state, engine.run()
def continue_game(): list saves, pick slot, load, run
def main(): try/except KeyboardInterrupt for clean exit
if __name__ == "__main__": main()