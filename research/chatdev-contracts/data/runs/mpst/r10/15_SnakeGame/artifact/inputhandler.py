class InputHandler:
    def process_events(self):
        """Pump the pygame event queue and return a list of actions.
        Each action is a tuple: ("quit",), ("direction", (dx, dy)),
        ("confirm", key), ("back",) etc.
        """
        actions = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                actions.append(("quit",))
            elif event.type == pygame.KEYDOWN:
                direction = DIRECTION_KEYS.get(event.key)
                if direction:
                    actions.append(("direction", direction))
                elif event.key in (pygame.K_ESCAPE,):
                    actions.append(("back",))
                elif event.key == pygame.K_p:
                    actions.append(("pause",))
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    actions.append(("confirm", event.key))
                elif event.key in DIFFICULTY_KEYS:
                    actions.append(("difficulty", DIFFICULTY_KEYS[event.key]))
        return actions