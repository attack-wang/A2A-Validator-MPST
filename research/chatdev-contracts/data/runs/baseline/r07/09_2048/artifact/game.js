/**
 * game.js
 * Core game logic for 2048: grid state, tile movement, merging,
 * random tile spawning, score tracking and game-over detection.
 * Contains no DOM code so it can be tested independently.
 */
'use strict';
/** Unique id source for tiles (used by the UI to track DOM elements). */
let TILE_ID_COUNTER = 0;
class Tile {
  constructor(value, row, col) {
    this.id = ++TILE_ID_COUNTER;
    this.value = value;
    this.row = row;
    this.col = col;
    this.isNew = false;
    this.mergedFrom = null;
  }
}
class Game {
  constructor(size = 4) {
    this.size = size;
    this.grid = [];
    this.score = 0;
    this.highestTile = 0;
    this.gameOver = false;
    this.won = false;
    this.reset();
  }
  reset() {
    this.grid = Array.from({ length: this.size }, () => Array(this.size).fill(null));
    this.score = 0;
    this.highestTile = 0;
    this.gameOver = false;
    this.won = false;
    this.addRandomTile();
    this.addRandomTile();
  }
  getEmptyCells() {
    const cells = [];
    for (let r = 0; r < this.size; r++) {
      for (let c = 0; c < this.size; c++) {
        if (!this.grid[r][c]) cells.push({ row: r, col: c });
      }
    }
    return cells;
  }
  addRandomTile() {
    const empty = this.getEmptyCells();
    if (empty.length === 0) return null;
    const cell = empty[Math.floor(Math.random() * empty.length)];
    const value = Math.random() < 0.9 ? 2 : 4;
    const tile = new Tile(value, cell.row, cell.col);
    tile.isNew = true;
    this.grid[cell.row][cell.col] = tile;
    if (value > this.highestTile) this.highestTile = value;
    return tile;
  }
  _clearTileFlags() {
    for (const tile of this.getTiles()) {
      tile.isNew = false;
      tile.mergedFrom = null;
    }
  }
  _getLineCells(direction, index) {
    const cells = [];
    for (let i = 0; i < this.size; i++) {
      let r, c;
      switch (direction) {
        case 'left':  r = index; c = i; break;
        case 'right': r = index; c = this.size - 1 - i; break;
        case 'up':    r = i; c = index; break;
        case 'down':  r = this.size - 1 - i; c = index; break;
        default: throw new Error('Unknown direction: ' + direction);
      }
      cells.push({ row: r, col: c });
    }
    return cells;
  }
  _slideAndMerge(tiles) {
    const output = [];
    let scoreGained = 0;
    let i = 0;
    while (i < tiles.length) {
      if (i + 1 < tiles.length && tiles[i].value === tiles[i + 1].value) {
        const merged = new Tile(tiles[i].value * 2, tiles[i].row, tiles[i].col);
        merged.mergedFrom = [tiles[i], tiles[i + 1]];
        output.push(merged);
        scoreGained += merged.value;
        i += 2;
      } else {
        output.push(tiles[i]);
        i += 1;
      }
    }
    while (output.length < this.size) output.push(null);
    return { tiles: output, scoreGained };
  }
  move(direction) {
    if (this.gameOver) return null;
    if (!['left', 'right', 'up', 'down'].includes(direction)) return null;
    this._clearTileFlags();
    let moved = false;
    let scoreGained = 0;
    const mergedTiles = [];
    const movedTiles = [];
    for (let index = 0; index < this.size; index++) {
      const cells = this._getLineCells(direction, index);
      const tiles = cells.map(cell => this.grid[cell.row][cell.col]).filter(Boolean);
      const result = this._slideAndMerge(tiles);
      for (let i = 0; i < this.size; i++) {
        const cell = cells[i];
        const oldTile = this.grid[cell.row][cell.col];
        const newTile = result.tiles[i];
        if (newTile !== oldTile) moved = true;
        this.grid[cell.row][cell.col] = newTile;
        if (!newTile) continue;
        if (newTile.mergedFrom) {
          newTile.row = cell.row;
          newTile.col = cell.col;
          mergedTiles.push(newTile);
          for (const src of newTile.mergedFrom) {
            src.row = cell.row;
            src.col = cell.col;
            movedTiles.push(src);
          }
        } else if (newTile.row !== cell.row || newTile.col !== cell.col) {
          newTile.row = cell.row;
          newTile.col = cell.col;
          movedTiles.push(newTile);
        }
      }
    }
    if (!moved) return null;
    this.score += scoreGained;
    for (const t of mergedTiles) {
      if (t.value > this.highestTile) this.highestTile = t.value;
      if (t.value >= 2048 && !this.won) this.won = true;
    }
    const newTile = this.addRandomTile();
    if (!this.movesAvailable()) this.gameOver = true;
    return { moved: true, scoreGained, mergedTiles, movedTiles, newTile };
  }
  movesAvailable() {
    for (let r = 0; r < this.size; r++) {
      for (let c = 0; c < this.size; c++) {
        if (!this.grid[r][c]) return true;
        const tile = this.grid[r][c];
        if (c + 1 < this.size && this.grid[r][c + 1] && this.grid[r][c + 1].value === tile.value) return true;
        if (r + 1 < this.size && this.grid[r + 1][c] && this.grid[r + 1][c].value === tile.value) return true;
      }
    }
    return false;
  }
  getTiles() {
    const tiles = [];
    for (let r = 0; r < this.size; r++) {
      for (let c = 0; c < this.size; c++) {
        if (this.grid[r][c]) tiles.push(this.grid[r][c]);
      }
    }
    return tiles;
  }
}