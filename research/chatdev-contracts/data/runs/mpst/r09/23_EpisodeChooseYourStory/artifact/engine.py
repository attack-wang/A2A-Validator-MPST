def display_scene(self, scene_id, scene):
    ui.clear_screen()
    ui.divider('=')
    ui.print_wrapped(f"[ {scene_id.replace('_', ' ').title()} ]")  # maybe location header
    ui.divider('=')
    ui.type_print(scene.get("text", ""), delay=ui.TYPE_DELAY)