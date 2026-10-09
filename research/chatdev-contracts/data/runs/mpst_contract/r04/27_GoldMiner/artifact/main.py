import math, random, time
import tkinter as tk

W, H = 800, 600
PX, PY = W // 2, 46
MIN_LEN, MAX_LEN = 34, 540
AMIN, AMAX = 20, 160

SPEC = {
    'gold_s':  (14, 50,  1.2, '#ffd24a'),
    'gold_m':  (20, 150, 2.0, '#f0a818'),
    'gold_l':  (28, 500, 3.6, '#d97e00'),
    'rock':    (22, 20,  5.0, '#8a8a8a'),
    'diamond': (16, 600, 1.5, '#66e0ff'),
    'tnt':     (18, 0,   1.0, '#e03328'),
    'bag':     (16, 0,   2.0, '#9a6b3f'),
}

class Obj:
    def __init__(self, kind, x, y):
        self.kind = kind
        self.r, self.value, self.weight, self.color = SPEC[kind]
        if kind == 'bag':
            self.value = random.choice([50, 100, 150, 250, 400])
        self.x, self.y = x, y

class Game:
    def __init__(self, root):
        self.root = root
        self.cv = tk.Canvas(root, width=W, height=H, bg='#1d2b3a',
                            highlightthickness=0)
        self.cv.pack()
        root.bind('<space>', self.on_key)
        root.bind('<Button-1>', self.on_key)
        root.bind('<Escape>', lambda e: root.destroy())
        self.state = 'menu'
        self.level = 1
        self.score = 0
        self.flash = None
        self.reset_level()
        self.last = time.time()
        self.loop()

    def reset_level(self):
        self.goal = 400 + (self.level - 1) * 350
        self.time_left = max(28, 62 - (self.level - 1) * 4)
        self.angle = math.radians(90)
        self.dirn = 1
        self.length = MIN_LEN
        self.claw = 'swing'
        self.carried = None
        self.clear_t = 0.0
        self.objects = []
        counts = [('gold_s', 5), ('gold_m', 3), ('gold_l', 2),
                  ('rock', 2 + min(self.level, 4)),
                  ('diamond', 1 if self.level >= 2 else 0),
                  ('tnt', min(1 + self.level // 2, 5)), ('bag', 1)]
        for kind, n in counts:
            for _ in range(n):
                for _try in range(220):
                    x = random.uniform(50, W - 50)
                    y = random.uniform(270, H - 35)
                    d = math.hypot(x - PX, y - PY)
                    if d < 240 or d > 515:
                        continue
                    if all(math.hypot(x - o.x, y - o.y) > 46 for o in self.objects):
                        self.objects.append(Obj(kind, x, y))
                        break

    def tip(self):
        return (PX + math.cos(self.angle) * self.length,
                PY + math.sin(self.angle) * self.length)

    def on_key(self, e):
        if self.state == 'menu':
            self.state = 'playing'
        elif self.state == 'playing' and self.claw == 'swing':
            self.claw = 'extend'
        elif self.state == 'clear':
            self.clear_t = 0.0
        elif self.state == 'over':
            self.level, self.score = 1, 0
            self.reset_level()
            self.state = 'playing'

    def explode(self, x, y):
        self.flash = (x, y, 0.45)
        self.objects = [o for o in self.objects
                        if math.hypot(o.x - x, o.y - y) > 110]

    def collect(self):
        if self.carried:
            self.score += self.carried.value
            self.carried = None
        self.length = MIN_LEN
        self.claw = 'swing'
        if self.score >= self.goal:
            self.state = 'clear'
            self.clear_t = 1.6

    def update(self, dt):
        if self.flash:
            x, y, t = self.flash
            t -= dt
            self.flash = (x, y, t) if t > 0 else None
        if self.state == 'clear':
            self.clear_t -= dt
            if self.clear_t <= 0:
                self.level += 1
                self.reset_level()
                self.state = 'playing'
            return
        if self.state != 'playing':
            return
        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left = 0
            self.state = 'clear' if self.score >= self.goal else 'over'
            self.clear_t = 1.6
            return
        if self.claw == 'swing':
            spd = math.radians(70 + 12 * self.level)
            self.angle += self.dirn * spd * dt
            if math.degrees(self.angle) >= AMAX:
                self.angle = math.radians(AMAX); self.dirn = -1
            elif math.degrees(self.angle) <= AMIN:
                self.angle = math.radians(AMIN); self.dirn = 1
        elif self.claw == 'extend':
            self.length += 420 * dt
            tx, ty = self.tip()
            for o in list(self.objects):
                if math.hypot(o.x - tx, o.y - ty) < o.r + 6:
                    if o.kind == 'tnt':
                        self.objects.remove(o)
                        self.explode(tx, ty)
                        self.claw = 'retract'
                    else:
                        self.objects.remove(o)
                        self.carried = o
                        self.claw = 'retract'
                    break
            else:
                if self.length >= MAX_LEN:
                    self.claw = 'retract'
        elif self.claw == 'retract':
            w = self.carried.weight if self.carried else 1.0
            self.length -= (300.0 / w) * dt
            if self.length <= MIN_LEN:
                self.collect()

    def draw_obj(self, o, x, y):
        r, c = o.r, o.color
        if o.kind == 'diamond':
            p = [x, y - r, x + r, y, x, y + r, x - r, y]
            self.cv.create_polygon(p, fill=c, outline='#ffffff')
        elif o.kind == 'bag':
            self.cv.create_rectangle(x - r, y - r, x + r, y + r,
                                     fill=c, outline='#5c3d20')
        else:
            self.cv.create_oval(x - r, y - r, x + r, y + r,
                                fill=c, outline='#000000')
        label = {'tnt': 'T', 'bag': '?'}.get(o.kind, str(o.value))
        self.cv.create_text(x, y, text=label, fill='#222222',
                            font=('Arial', 9, 'bold'))

    def draw(self):
        cv = self.cv
        cv.delete('all')
        cv.create_rectangle(0, PY + 8, W, H, fill='#3a2a1a', width=0)
        cv.create_line(0, PY + 8, W, PY + 8, fill='#241a10', width=3)
        for o in self.objects:
            self.draw_obj(o, o.x, o.y)
        tx, ty = self.tip()
        cv.create_line(PX, PY, tx, ty, fill='#d8d8d8', width=2)
        a = self.angle
        for s in (-1, 1):
            pa = a + s * math.radians(150)
            cv.create_line(tx, ty, tx + math.cos(pa) * 16,
                           ty + math.sin(pa) * 16,
                           fill='#c0c0c0', width=3)
        cv.create_oval(PX - 6, PY - 6, PX + 6, PY + 6, fill='#d8d8d8')
        if self.carried:
            self.draw_obj(self.carried, tx, ty)
        if self.flash:
            x, y, t = self.flash
            r = (0.45 - t) / 0.45 * 110
            cv.create_oval(x - r, y - r, x + r, y + r,
                           outline='#ff8800', width=3)
        cv.create_rectangle(0, 0, W, 34, fill='#101820', width=0)
        cv.create_text(70, 17, text='Level %d' % self.level,
                       fill='#ffffff', font=('Arial', 12, 'bold'))
        cv.create_text(230, 17, text='Gold: %d / %d' % (self.score, self.goal),
                       fill='#ffd24a', font=('Arial', 12, 'bold'))
        cv.create_text(430, 17, text='Time: %d' % math.ceil(self.time_left),
                       fill='#ff6a5a', font=('Arial', 12, 'bold'))
        cv.create_text(600, 17, text='Claw: %d° len %d' %
                       (round(math.degrees(self.angle)), self.length),
                       fill='#9fd8ff', font=('Arial', 11))
        cv.create_text(730, 17, text='SPACE = grab',
                       fill='#aaaaaa', font=('Arial', 10))
        if self.state == 'menu':
            cv.create_rectangle(150, 200, 650, 400, fill='#101820', width=2)
            cv.create_text(400, 250, text='GOLD MINER', fill='#ffd24a',
                           font=('Arial', 30, 'bold'))
            cv.create_text(400, 300, text='Press SPACE to drop the claw.\n'
                           'Grab gold before time runs out.\n'
                           'Meet the gold goal to advance.\n'
                           'Avoid rocks and TNT!',
                           fill='#ffffff', font=('Arial', 13))
            cv.create_text(400, 375, text='Press SPACE to start',
                           fill='#66e0ff', font=('Arial', 13, 'bold'))
        elif self.state == 'clear':
            cv.create_text(400, 280, text='Level %d cleared!' % self.level,
                           fill='#66ff88', font=('Arial', 26, 'bold'))
            cv.create_text(400, 320, text='Score: %d' % self.score,
                           fill='#ffffff', font=('Arial', 16))
        elif self.state == 'over':
            cv.create_rectangle(150, 210, 650, 390, fill='#101820', width=2)
            cv.create_text(400, 260, text='GAME OVER', fill='#ff5544',
                           font=('Arial', 30, 'bold'))
            cv.create_text(400, 305, text='Reached level %d — Score %d' %
                           (self.level, self.score),
                           fill='#ffffff', font=('Arial', 14))
            cv.create_text(400, 350, text='Press SPACE to restart',
                           fill='#66e0ff', font=('Arial', 13, 'bold'))

    def loop(self):
        now = time.time()
        dt = min(0.05, now - self.last)
        self.last = now
        self.update(dt)
        self.draw()
        self.root.after(16, self.loop)

def main():
    root = tk.Tk()
    root.title('Gold Miner')
    root.resizable(False, False)
    Game(root)
    root.mainloop()

if __name__ == '__main__':
    main()