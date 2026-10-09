def run(self):
    if os.name == "nt":
        os.system("")  # enable ANSI/VT processing on modern Windows consoles
    sys.stdout.write(...)