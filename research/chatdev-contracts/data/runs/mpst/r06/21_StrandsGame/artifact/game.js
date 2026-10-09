/**
 * game.js
 * Core game logic for the Strands word-segmentation puzzle.
 * Implements: strand selection, merge-tray management, merge validation,
 * valid-merge feedback, spangram handling, completion detection,
 * puzzle navigation, hints, stats, and sound effects.
 */
/* ---------- Feedback message pools ---------- */
const FeedbackMessages = {
  success: [
    "Perfect merge!",
    "Strand-tacular!",
    "You wove it beautifully!",
    "That's a seamless splice!",
    "Brilliant braiding of strands!",
    "A masterful twist of text!"
  ],
  error: [
    "Hmm, those strands don't tie together.",
    "Close, but no valid phrase this time.",
    "That knot came undone — try another combination.",
    "The strands slipped apart. Regroup and retry!"
  ],
  warn: [
    "Select at least one strand first.",
    "The merge tray is empty — pick some strands."
  ]
};
/** Pick a random message from an array. */
function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}
/* ---------- Sound effects (Web Audio, no assets) ---------- */
class SoundKit {
  constructor() {
    this.enabled = true;
    this.ctx = null;
  }
  _ctx() {
    if (!this.enabled) return null;
    if (!this.ctx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) { this.enabled = false; return null; }
      this.ctx = new AC();
    }
    if (this.ctx.state === 'suspended') this.ctx.resume();
    return this.ctx;
  }
  _tone(freq, start, dur, type = 'sine', vol = 0.06) {
    const ctx = this._ctx();
    if (!ctx) return;
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    const t0 = ctx.currentTime + start;
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(vol, t0 + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    osc.connect(g).connect(ctx.destination);
    osc.start(t0);
    osc.stop(t0 + dur + 0.05);
  }
  click() { this._tone(520, 0, 0.06, 'triangle', 0.04); }
  success() { [523.25, 659.25, 783.99].forEach((f, i) => this._tone(f, i * 0.09, 0.18, 'sine', 0.07)); }
  error() { this._tone(160, 0, 0.22, 'sawtooth', 0.05); this._tone(120, 0.08, 0.25, 'sawtooth', 0.04); }
  complete() { [523.25, 659.25, 783.99, 1046.5].forEach((f, i) => this._tone(f, i * 0.12, 0.3, 'sine', 0.08)); }
}
/* ---------- Game controller ---------- */
class StrandsGame {
  constructor(puzzles) {
    this.puzzles = puzzles;
    this.puzzleIndex = 0;
    this.sound = new SoundKit();
    this.dom = {
      strandBoard: document.getElementById('strandBoard'),
      mergeTray: document.getElementById('mergeTray'),
      trayPreview: document.getElementById('trayPreview'),
      clearTrayBtn: document.getElementById('clearTrayBtn'),
      mergeBtn: document.getElementById('mergeBtn'),
      hintBtn: document.getElementById('hintBtn'),
      prevPuzzleBtn: document.getElementById('prevPuzzleBtn'),
      nextPuzzleBtn: document.getElementById('nextPuzzleBtn'),
      puzzleSelect: document.getElementById('puzzleSelect'),
      soundToggleBtn: document.getElementById('soundToggleBtn'),
      progressText: document.getElementById('progressText'),
      progressFill: document.getElementById('progressFill'),
      answersList: document.getElementById('answersList'),
      feedbackMessage: document.getElementById('feedbackMessage'),
      feedbackLog: document.getElementById('feedbackLog'),
      statsText: document.getElementById('statsText'),
      victoryOverlay: document.getElementById('victoryOverlay'),
      victoryText: document.getElementById('victoryText'),
      replayBtn: document.getElementById('replayBtn'),
      nextBtn: document.getElementById('nextBtn'),
      puzzleTheme: document.getElementById('puzzleTheme'),
      puzzleHint: document.getElementById('puzzleHint')
    };
    this.bindEvents();
    this.loadPuzzle(0);
  }
  /* ----- setup ----- */
  bindEvents() {
    this.dom.clearTrayBtn.addEventListener('click', () => { this.sound.click(); this.clearTray(); });
    this.dom.mergeBtn.addEventListener('click', () => this.merge());
    this.dom.hintBtn.addEventListener('click', () => this.hint());
    this.dom.prevPuzzleBtn.addEventListener('click', () => this.navPuzzle(-1));
    this.dom.nextPuzzleBtn.addEventListener('click', () => this.navPuzzle(1));
    this.dom.puzzleSelect.addEventListener('change', (e) => this.loadPuzzle(Number(e.target.value)));
    this.dom.soundToggleBtn.addEventListener('click', () => this.toggleSound());
    this.dom.replayBtn.addEventListener('click', () => this.loadPuzzle(this.puzzleIndex));
    this.dom.nextBtn.addEventListener('click', () => {
      const next = (this.puzzleIndex + 1) % this.puzzles.length;
      this.loadPuzzle(next);
    });
  }
  loadPuzzle(i) {
    this.puzzleIndex = i;
    this.currentPuzzle = this.puzzles[i];
    // Deep-copy strands with runtime state; precompute normalized text.
    this.strands = this.currentPuzzle.strands.map((t, idx) => ({
      id: idx,
      text: t,
      textNorm: t.toUpperCase(),
      used: false
    }));
    this.tray = [];
    this.found = new Set();
    this.foundOrder = [];
    this.stats = { merges: 0, valid: 0, hints: 0 };
    // Populate the puzzle selector.
    this.dom.puzzleSelect.innerHTML = '';
    this.puzzles.forEach((p, idx) => {
      const opt = document.createElement('option');
      opt.value = String(idx);
      opt.textContent = p.title + ' — ' + p.theme;
      if (idx === i) opt.selected = true;
      this.dom.puzzleSelect.appendChild(opt);
    });
    this.dom.puzzleTheme.textContent = this.currentPuzzle.theme;
    this.dom.puzzleHint.textContent = '💡 ' + this.currentPuzzle.hint;
    this.dom.victoryOverlay.classList.add('hidden');
    this.showFeedback('New puzzle loaded: ' + this.currentPuzzle.theme + '.', 'info');
    this.renderBoard();
    this.renderTray();
    this.updateProgress();
    this.updateStats();
  }
  /* ----- rendering ----- */
  renderBoard() {
    this.dom.strandBoard.innerHTML = '';
    this.strands.forEach((s) => {
      const btn = document.createElement('button');
      btn.className = 'strand-tile' + (s.used ? ' used' : '') + (this.tray.includes(s) ? ' selected' : '');
      btn.textContent = s.text;
      btn.dataset.id = String(s.id);
      btn.disabled = s.used;
      btn.addEventListener('click', () => this.onStrandClick(s.id));
      this.dom.strandBoard.appendChild(btn);
    });
  }
  renderTray() {
    this.dom.mergeTray.innerHTML = '';
    this.tray.forEach((s) => {
      const chip = document.createElement('button');
      chip.className = 'tray-chip';
      chip.textContent = s.text;
      chip.dataset.id = String(s.id);
      chip.title = 'Click to remove from tray';
      chip.addEventListener('click', () => this.onTrayItemClick(s.id));
      this.dom.mergeTray.appendChild(chip);
    });
    // Live preview of the concatenation (real-time feedback).
    const preview = this.tray.map(s => s.text).join('');
    this.dom.trayPreview.textContent = preview || '…';
  }
  /* ----- interaction ----- */
  onStrandClick(id) {
    const s = this.strands.find(x => x.id === id);
    if (!s || s.used) return;
    this.sound.click();
    const pos = this.tray.indexOf(s);
    if (pos >= 0) {
      this.tray.splice(pos, 1); // toggle off
    } else {
      this.tray.push(s);        // toggle on
    }
    this.renderBoard();
    this.renderTray();
  }
  onTrayItemClick(id) {
    const s = this.strands.find(x => x.id === id);
    if (!s) return;
    this.sound.click();
    const pos = this.tray.indexOf(s);
    if (pos >= 0) this.tray.splice(pos, 1);
    this.renderBoard();
    this.renderTray();
  }
  clearTray() {
    this.tray = [];
    this.renderBoard();
    this.renderTray();
  }
  /* ----- core: merge & verify ----- */
  merge() {
    if (this.tray.length === 0) {
      this.showFeedback(pick(FeedbackMessages.warn), 'warn');
      return;
    }
    this.stats.merges++;
    const norm = this.tray.map(s => s.text).join('').toUpperCase();
    const match = this.currentPuzzle.answers.find(
      a => a.text.toUpperCase() === norm && !this.found.has(a.text)
    );
    if (match) {
      this.stats.valid++;
      this.tray.forEach(s => { s.used = true; }); // strands consumed
      this.found.add(match.text);
      this.foundOrder.push(match);
      this.sound.success();
      this.showFeedback(
        (match.spangram ? '🌟 SPANGRAM! ' : '') + pick(FeedbackMessages.success) +
        ' “' + match.text + '” is valid!',
        'success'
      );
      this.logFeedback('✔ ' + match.text + (match.spangram ? ' (spangram)' : ''), 'success');
      this.clearTray();
      this.renderBoard();
      this.updateProgress();
      this.updateStats();
      if (this.found.size === this.currentPuzzle.answers.length) this.complete();
    } else {
      this.sound.error();
      this.showFeedback(
        pick(FeedbackMessages.error) + ' — “' + norm + '” doesn\'t form a valid phrase.',
        'error'
      );
      this.logFeedback('✘ ' + norm, 'error');
      // Keep tray so the player can edit; do NOT consume strands.
      this.updateStats();
    }
  }
  /* ----- hint ----- */
  hint() {
    const target = this.currentPuzzle.answers.find(a => !this.found.has(a.text));
    if (!target) {
      this.showFeedback('All answers already found!', 'info');
      return;
    }
    this.stats.hints++;
    const path = this.findDecomposition(target.text.toUpperCase());
    if (path && path.length > 0) {
      const first = path[0];
      const btn = this.dom.strandBoard.querySelector('[data-id="' + first.id + '"]');
      if (btn) {
        btn.classList.add('hinted');
        setTimeout(() => btn.classList.remove('hinted'), 2000);
      }
      this.showFeedback('Hint: try starting with the strand “' + first.text + '”.', 'info');
    } else {
      this.showFeedback('Hint: the answer starts with “' + target.text.charAt(0) + '”…', 'info');
    }
    this.updateStats();
  }
  /* ----- completion ----- */
  complete() {
    this.sound.complete();
    this.dom.victoryText.textContent =
      'You merged all ' + this.foundOrder.length + ' phrases in “' +
      this.currentPuzzle.theme + '” with ' + this.stats.merges +
      ' merge attempt' + (this.stats.merges === 1 ? '' : 's') +
      ' and ' + this.stats.hints + ' hint' + (this.stats.hints === 1 ? '' : 's') + '.';
    this.dom.victoryOverlay.classList.remove('hidden');
  }
  /* ----- decomposition search (DFS) ----- */
  /**
   * DFS: find an ordered set of unused strands concatenating to targetNorm.
   * @param {string} targetNorm - uppercase target with no spaces
   * @returns {Array<Object>|null} the strand path, or null if impossible
   */
  findDecomposition(targetNorm) {
    const unused = this.strands.filter(s => !s.used);
    const path = [];
    const dfs = (pos) => {
      if (pos === targetNorm.length) return true; // plain base case
      for (const s of unused) {
        if (path.includes(s)) continue; // no reuse within one target
        if (targetNorm.startsWith(s.textNorm, pos)) {
          path.push(s);
          if (dfs(pos + s.textNorm.length)) return true;
          path.pop();
        }
      }
      return false;
    };
    return dfs(0) ? path.slice() : null;
  }
  /* ----- progress / stats / feedback ----- */
  updateProgress() {
    const total = this.currentPuzzle.answers.length;
    const done = this.found.size;
    this.dom.progressText.textContent = done + ' / ' + total + ' phrases merged';
    const pct = total === 0 ? 0 : Math.round((done / total) * 100);
    this.dom.progressFill.style.width = pct + '%';
    // Answers list
    this.dom.answersList.innerHTML = '';
    if (this.foundOrder.length === 0) {
      const li = document.createElement('li');
      li.className = 'empty';
      li.textContent = 'No merges yet — select strands and press Merge.';
      this.dom.answersList.appendChild(li);
    } else {
      this.foundOrder.forEach((a) => {
        const li = document.createElement('li');
        li.className = a.spangram ? 'spangram' : '';
        li.textContent = (a.spangram ? '🌟 ' : '') + a.text;
        this.dom.answersList.appendChild(li);
      });
    }
  }
  updateStats() {
    this.dom.statsText.textContent =
      'Merges tried: ' + this.stats.merges +
      ' · Valid: ' + this.stats.valid +
      ' · Hints: ' + this.stats.hints;
  }
  showFeedback(msg, type) {
    this.dom.feedbackMessage.textContent = msg;
    this.dom.feedbackMessage.className = 'feedback-message ' + (type || 'info');
  }
  logFeedback(msg, type) {
    const li = document.createElement('li');
    li.className = type || 'info';
    li.textContent = msg;
    this.dom.feedbackLog.prepend(li);
    // Cap the log length.
    while (this.dom.feedbackLog.children.length > 8) {
      this.dom.feedbackLog.removeChild(this.dom.feedbackLog.lastChild);
    }
  }
  /* ----- navigation ----- */
  navPuzzle(dir) {
    const next = (this.puzzleIndex + dir + this.puzzles.length) % this.puzzles.length;
    this.loadPuzzle(next);
  }
  toggleSound() {
    this.sound.enabled = !this.sound.enabled;
    this.dom.soundToggleBtn.textContent = this.sound.enabled ? '🔊' : '🔇';
    this.showFeedback('Sound ' + (this.sound.enabled ? 'enabled' : 'muted') + '.', 'info');
    if (this.sound.enabled) this.sound.click();
  }
}