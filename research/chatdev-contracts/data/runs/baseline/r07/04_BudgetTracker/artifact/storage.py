def save(self, expenses, savings_goals):
    payload = {...}
    tmp_path = self.filepath + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        os.replace(tmp_path, self.filepath)
    except OSError as exc:
        raise IOError(f"Could not save data to {self.filepath}: {exc}")