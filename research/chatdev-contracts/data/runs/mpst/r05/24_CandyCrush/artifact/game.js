class Game {
  constructor(ui) {
    this.ui = ui;
    this.board = new Board();
    this.score = 0; this.movesLeft = INITIAL_MOVES; this.timeLeft = INITIAL_TIME;
    this.state = 'idle'; this.combo = 0; this.selected = null;
    this.timerId = null;
  }
  start() {
    this.ui.buildBoard(this.board);
    this.updateHUD();
    this.state = 'playing';
    this.startTimer();
  }
  startTimer() {
    clearInterval(this.timerId);
    this.timerId = setInterval(() => this.tick(), 1000);
  }
  tick() {
    if (this.state !== 'playing') return;
    this.timeLeft--;
    this.updateHUD();
    if (this.timeLeft <= 0) this.endGame('Time is up!');
  }
  onCellPointerDown(r, c) / onCellDrag(...) — input handling in ui? 