    @staticmethod
    def _normalize_date(value):
        text = str(value).strip()
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        raise ValueError(f"Invalid date: {value!r}. Expected format YYYY-MM-DD.")
    ...