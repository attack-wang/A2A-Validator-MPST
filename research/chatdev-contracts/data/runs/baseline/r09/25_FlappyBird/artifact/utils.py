def make_vertical_gradient(width, height, top_hex, bottom_hex):
    """Return a tk.PhotoImage with a smooth vertical gradient."""
    import tkinter as tk
    top = _hex_to_rgb(top_hex)
    bottom = _hex_to_rgb(bottom_hex)
    img = tk.PhotoImage(width=width, height=height)
    for y in range(height):
        t = y / max(1, height - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        img.put("#%02x%02x%02x" % (r, g, b), (0, y, width, y + 1))
    return img