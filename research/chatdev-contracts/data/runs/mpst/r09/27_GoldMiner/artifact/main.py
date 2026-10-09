'''
main.py
Entry point for the Gold Miner game. Imports the game module defensively so
that a missing dependency (e.g. pygame) produces a clear, actionable error
message instead of a raw traceback.
'''
try:
    from game import GoldMinerGame
except ImportError as exc:
    missing = getattr(exc, "name", None) or "a required module"
    print("=" * 60)
    print("Gold Miner could not start: missing dependency '%s'." % missing)
    print("Install the required packages with:")
    print("    pip install -r requirements.txt")
    print("or directly:")
    print("    pip install pygame")
    print("=" * 60)
    raise SystemExit(1)
def main():
    """Create the game instance and run the main loop."""
    game = GoldMinerGame()
    game.run()
if __name__ == "__main__":
    main()