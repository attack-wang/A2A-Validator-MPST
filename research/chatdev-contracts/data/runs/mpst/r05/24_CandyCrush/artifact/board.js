/* Pure game-state model: grid of candy type indices plus match/gravity logic. */
class Board {
  constructor(size = BOARD_SIZE, numTypes = NUM_TYPES) {
    this.size = size;
    this.numTypes = numTypes;
    this.grid = [];
    this.fillInitial();
  }
  get(r, c) { return this.grid[r][c]; }
  set(r, c, v) { this.grid[r][c] = v; }
  inBounds(r, c) { return r >= 0 && r < this.size && c >= 0 && c < this.size; }
  areAdjacent(r1, c1, r2, c2) { return Math.abs(r1 - r2) + Math.abs(c1 - c2) === 1; }
  randomType() { return Math.floor(Math.random() * this.numTypes); }
  /* Swap two cells in place (used by gameplay and validity probing). */
  swap(r1, c1, r2, c2) {
    const tmp = this.grid[r1][c1];
    this.grid[r1][c1] = this.grid[r2][c2];
    this.grid[r2][c2] = tmp;
  }
  /* Build the starting grid with no pre-existing matches and at least one valid move. */
  fillInitial() {
    this.grid = [];
    for (let r = 0; r < this.size; r++) {
      const row = [];
      for (let c = 0; c < this.size; c++) {
        let type;
        do {
          type = this.randomType();
        } while (
          (c >= 2 && row[c - 1] === type && row[c - 2] === type) ||
          (r >= 2 && this.grid[r - 1][c] === type && this.grid[r - 2][c] === type)
        );
        row.push(type);
      }
      this.grid.push(row);
    }
    // Extremely unlikely, but guarantee a playable opening.
    if (!this.hasValidMove()) this.fillInitial();
  }