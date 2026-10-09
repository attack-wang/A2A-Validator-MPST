"""Host-owned bounded Tk startup probe. Never edits generated source."""
import json
from pathlib import Path
import runpy
import sys


def main():
    entry, record = sys.argv[1:3]
    import tkinter as tk
    observation = {"event_loop_observed": False, "mapped_window": False,
                   "widget_count": 0, "callback_errors": []}
    original = tk.Misc.mainloop

    def callback_error(self, kind, value, traceback):
        observation["callback_errors"].append(f"{kind.__name__}: {value}")
        self.quit()

    def bounded_loop(self, n=0):
        def inspect_and_stop():
            observation.update(event_loop_observed=True,
                               mapped_window=bool(self.winfo_ismapped()),
                               widget_count=len(self.winfo_children()))
            self.quit()
        self.after(200, inspect_and_stop)
        original(self, n)

    tk.Misc.mainloop = bounded_loop
    tk.Tk.report_callback_exception = callback_error
    sys.path.insert(0, str(Path(entry).resolve().parent))
    sys.argv = [entry]
    try:
        runpy.run_path(entry, run_name="__main__")
    finally:
        Path(record).write_text(json.dumps(observation), encoding="utf-8")
    if observation["callback_errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
