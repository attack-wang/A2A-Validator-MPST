def run_game():
    pygame.init()
    screen = ...
    clock = ...
    fonts = build_fonts()
    state = "playing"
    level_num = 1
    score = 0
    level = Level(level_num)
    claw = Claw(swing_speed=level_swing_speed(level_num))
    time_left = float(level.time_limit)
    floating = []
    while running:
        # events per state
        ...
        if state == "playing":
            time_left -= dt
            delivered = claw.update(level.objects)
            if delivered is not None:
                score += delivered.value
                floating.append(FloatingText(...))
                if score >= level.goal:
                    state = "level_complete"
            if time_left <= 0:
                time_left = 0
                if score >= level.goal:
                    state = "level_complete"
                else:
                    state = "game_over"
        # draw everything