class TerminalUI:
    def __init__(self, columns: int = BOARD_COLUMNS):
        self.columns = columns
    def show_puzzle_header(self, game: StrandsGame) -> None:
        p = game.puzzle
        print("=" * 60)
        print(f"  STRANDS — Theme: {p.theme}")
        print(f"  Merge all {p.target_count} targets from {p.total_strands} strands.")
        print("=" * 60)
    def render_board(self, game: StrandsGame) -> None:
        print("\n--- Strand Board ---")
        cells = []
        for i, strand in enumerate(game.strands):
            label = f"[{i + 1:>2}]"
            if strand.used:
                text = "-" * max(len(strand.text), 3)
            else:
                marker = "*" if strand.hinted else ""
                text = f"{marker}{strand.text}" if marker else strand.text
            cells.append(f"{label} {text}")
        for row_start in range(0, len(cells), self.columns):
            row = cells[row_start:row_start + self.columns]
            print("".join(cell.ljust(CELL_WIDTH) for cell in row))
        print("( * = hinted strand, --- = already merged )")
    def render_selection(self, game: StrandsGame, preview: Optional[MergeResult]) -> None:
        if not game.selection:
            print("\nSelection: (empty) — e.g. type: select 1 2 3")
            return
        texts = [game.strands[i].text for i in game.selection]
        print("\nSelection: " + " + ".join(texts) + f"  ({len(texts)} strand(s))")
        if preview is not None:
            print(f"  preview: {preview.message}")
    def render_found(self, game: StrandsGame) -> None:
        print(f"\n--- Found Merges ({game.progress()}) ---")
        if not game.found:
            print("  (none yet)")
        for record in game.found:
            print(f"  ✔ {record.phrase}")
        print()
    def render_result(self, result: MergeResult) -> None:
        tag = {
            MergeStatus.VALID: "[VALID]",
            MergeStatus.ALREADY_FOUND: "[REPEAT]",
            MergeStatus.PARTIAL: "[PARTIAL]",
            MergeStatus.INVALID: "[INVALID]",
        }[result.status]
        print(f"{tag} {result.message}")
    def show_message(self, message: str) -> None:
        print(message)
    def show_completion(self, game: StrandsGame) -> None:
        ...
    def show_help(self) -> None:
        print(HELP_TEXT)