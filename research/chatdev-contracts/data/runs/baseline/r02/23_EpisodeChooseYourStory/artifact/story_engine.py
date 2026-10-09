class StoryEngine:
    COMMANDS = {"save", "load", "status", "inventory", "help", "quit", "menu"}
    def __init__(self, scenes, state, display, save_manager, meta)
    def run(self):
        enter current or start scene; loop until ending or quit
    def _enter_scene(scene_id)
    def _resolve_next(spec) -> str
    def _visible_choices(scene)
    def _handle_command(cmd) -> bool (returns whether to continue loop / special like load)
    def _ending(scene)