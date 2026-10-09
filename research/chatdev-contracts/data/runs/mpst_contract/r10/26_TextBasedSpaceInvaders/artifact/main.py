import random
import tkinter as tk

WIDTH, HEIGHT = 480, 640
FPS_MS = 16
PLAYER_SPEED = 5
BULLET_SPEED = 8
EBULLET_SPEED = 4
BASE_SPEED = 1.0
DESCENT = 18
ROWS, COLS = 4, 8
AW, AH = 32, 22
SX, SY = 44, 38
PW, PH = 32, 24
PY = HEIGHT - 48
LIVES = 3
POINTS = [30, 20, 20, 10]
COLORS = ["#00dc64", "#00c8dc", "#f0dc3c", "#f064c8"]

root = tk.Tk()
root.title("Space Invaders")
root.resizable(False, False)
cv = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#080a1c", highlightthickness=0)
cv.pack()
STARS = [(random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)) for _ in range(80)]
keys = {"left": False, "right": False}


def new_game():
    aliens = [{"x": 50 + c * SX, "y": 70 + r * SY, "row": r, "alive": True}
              for r in range(ROWS) for c in range(COLS)]
    return {"px": (WIDTH - PW) // 2, "bullets": [], "ebullets": [], "aliens": aliens,
            "dir": 1, "score": 0, "lives": LIVES, "state": "play", "cool": 0, "fire": 60}


g = new_game()


def on_key(e):
    global g
    k = e.keysym.lower()
    if k in ("left", "a"):
        keys["left"] = True
    elif k in ("right", "d"):
        keys["right"] = True
    elif k == "space" and g["state"] == "play" and g["cool"] <= 0:
        g["bullets"].append([g["px"] + PW // 2, PY - 4])
        g["cool"] = 18
    elif k == "return" and g["state"] != "play":
        g = new_game()


def on_release(e):
    k = e.keysym.lower()
    if k in ("left", "a"):
        keys["left"] = False
    elif k in ("right", "d"):
        keys["right"] = False


root.bind("<KeyPress>", on_key)
root.bind("<KeyRelease>", on_release)


def update():
    if keys["left"]:
        g["px"] -= PLAYER_SPEED
    if keys["right"]:
        g["px"] += PLAYER_SPEED
    g["px"] = max(0, min(WIDTH - PW, g["px"]))
    g["cool"] -= 1

    for b in g["bullets"]:
        b[1] -= BULLET_SPEED
    g["bullets"] = [b for b in g["bullets"] if b[1] > 40]
    for b in g["ebullets"]:
        b[1] += EBULLET_SPEED
    g["ebullets"] = [b for b in g["ebullets"] if b[1] < HEIGHT]

    alive = [a for a in g["aliens"] if a["alive"]]
    speed = BASE_SPEED + (ROWS * COLS - len(alive)) * 0.03
    hit_edge = False
    for a in alive:
        a["x"] += g["dir"] * speed
        if a["x"] <= 0 or a["x"] + AW >= WIDTH:
            hit_edge = True
    if hit_edge:
        g["dir"] *= -1
        for a in alive:
            a["y"] += DESCENT

    g["fire"] -= 1
    if g["fire"] <= 0 and alive:
        s = random.choice(alive)
        g["ebullets"].append([s["x"] + AW // 2, s["y"] + AH])
        g["fire"] = random.randint(30, 70)

    for b in g["bullets"]:
        for a in g["aliens"]:
            if (a["alive"] and a["x"] - 2 <= b[0] <= a["x"] + AW + 2
                    and a["y"] - 2 <= b[1] <= a["y"] + AH + 2):
                a["alive"] = False
                g["score"] += POINTS[a["row"]]
                b[1] = -10
                break

    for b in g["ebullets"]:
        if g["px"] <= b[0] <= g["px"] + PW and PY <= b[1] <= PY + PH:
            b[1] = HEIGHT + 10
            g["lives"] -= 1
            if g["lives"] <= 0:
                g["state"] = "over"

    if any(a["alive"] and a["y"] + AH >= PY for a in g["aliens"]):
        g["state"] = "over"
    if all(not a["alive"] for a in g["aliens"]):
        g["state"] = "win"


def draw():
    cv.delete("all")
    for x, y in STARS:
        cv.create_rectangle(x, y, x + 1, y + 1, fill="#c8c8ff", outline="")
    for a in g["aliens"]:
        if not a["alive"]:
            continue
        x, y, col = a["x"], a["y"], COLORS[a["row"]]
        cv.create_rectangle(x, y, x + AW, y + AH, fill=col, outline="")
        cv.create_rectangle(x + 6, y + 6, x + 12, y + 12, fill="#141414", outline="")
        cv.create_rectangle(x + AW - 12, y + 6, x + AW - 6, y + 12, fill="#141414", outline="")
        cv.create_rectangle(x + 7, y + AH, x + 12, y + AH + 5, fill=col, outline="")
        cv.create_rectangle(x + AW - 12, y + AH, x + AW - 7, y + AH + 5, fill=col, outline="")
    for b in g["bullets"]:
        cv.create_rectangle(b[0] - 2, b[1] - 8, b[0] + 2, b[1] + 4, fill="#ffff78", outline="")
    for b in g["ebullets"]:
        cv.create_rectangle(b[0] - 2, b[1], b[0] + 2, b[1] + 10, fill="#ff5a5a", outline="")
    if g["state"] in ("play", "over"):
        x = g["px"]
        cv.create_polygon(x + PW // 2, PY, x + PW, PY + 16, x + PW, PY + PH,
                          x, PY + PH, x, PY + 16, fill="#50ff78", outline="")
        cv.create_rectangle(x + PW // 2 - 2, PY + 6, x + PW // 2 + 2, PY + 14,
                            fill="#ffc83c", outline="")
    cv.create_text(10, 8, anchor="nw", text=f"Score: {g['score']}", fill="white", font=("Arial", 13))
    cv.create_text(WIDTH - 10, 8, anchor="ne", text=f"Lives: {g['lives']}", fill="white", font=("Arial", 13))
    if g["state"] == "over":
        cv.create_text(WIDTH // 2, HEIGHT // 2 - 30, text="GAME OVER",
                       fill="#ff5050", font=("Arial", 26, "bold"))
    elif g["state"] == "win":
        cv.create_text(WIDTH // 2, HEIGHT // 2 - 30, text="YOU WIN!",
                       fill="#78ff78", font=("Arial", 26, "bold"))
    if g["state"] != "play":
        cv.create_text(WIDTH // 2, HEIGHT // 2 + 20,
                       text=f"Final Score: {g['score']}  -  Press ENTER to restart",
                       fill="white", font=("Arial", 11))


def tick():
    if g["state"] == "play":
        update()
    draw()
    root.after(FPS_MS, tick)


tick()
root.mainloop()