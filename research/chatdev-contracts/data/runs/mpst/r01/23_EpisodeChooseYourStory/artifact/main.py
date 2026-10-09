'''
main.py
Entry point for the interactive storytelling game "The Hollow Shrine".
Builds the structured story graph, validates it, and runs the
interactive loop. Run with:  python main.py
'''
from game_state import GameState
from story_engine import StoryEngine, build_default_story
def main():
    """Set up the story graph and run the interactive game loop."""
    story = build_default_story()
    engine = StoryEngine(story, GameState(player_name="Traveler"),
                         start_node="arrival")
    # Fail fast on broken links or dead ends before the player starts.
    problems = engine.validate_story()
    for problem in problems:
        print(f"Story warning: {problem}")
    engine.run()
if __name__ == "__main__":
    main()