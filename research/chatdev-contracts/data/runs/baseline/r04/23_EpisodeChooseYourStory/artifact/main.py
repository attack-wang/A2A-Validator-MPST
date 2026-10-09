def main():
    story_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "story.json")
    story = load_story(story_path)
    try:
        from gui import GameGUI  # tkinter
        app = GameGUI(engine)
        app.run()
    except ImportError:
        from console_ui import ConsoleUI
        ConsoleUI(engine).run()