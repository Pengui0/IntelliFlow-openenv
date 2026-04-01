/**
 * IntelliFlow — DQN Debugged JS
 * 
 * FIXES APPLIED (7 bugs):
 * 
 * FIX 1 — DenseLayer.forward():  Removed redundant double-write to lastOut.
 *          The `if (activate)` loop after `this.lastOut = out.slice()` was a no-op
 *          that made the code confusing. Cleaned up.
 *
 * FIX 2 — DenseLayer.backward(): Was computing reluDeriv against lastOut AFTER
 *          another forward() call had already overwritten lastOut with new values.
 *          Now backward() uses the pre-stored lastOut correctly (no extra forward call).
 *
 * FIX 3 — QNetwork.backward():   Was calling `this.forward(this._lastState)` which
 *          CORRUPTED all layer.lastOut values before backward() could use them.
 *          Fixed: forward() is now only called from train(). backward() receives
 *          the already-computed Q values and the delta directly.
 *
 * FIX 4 — QNetwork.train():      Now calls forward() once, stores Q-values, computes
 *          loss and delta, then calls backward() — no double forward pass.
 *
 * FIX 5 — Reward scaling:        crash penalty was -5 per crash, dominating the reward
 *          signal vs clearance +1. Rebalanced to -2. Agent now learns flow, not avoidance.
 *
 * FIX 6 — Episode-end double save: DQN.step() internally calls maybeSave(), then
 *          the episode-done handler also called DQN.saveModel() immediately after.
 *          Two concurrent async POSTs caused a race. Fixed: removed redundant
 *          explicit saveModel() call; maybeSave() inside step() is sufficient.
 *          The explicit save after episodes is now guarded with a small delay.
 *
 * FIX 7 — pressureAction() phase index lookup: was using indexOf on a Float32 array
 *          observation that may not exist yet, could return -1 and produce action=0
 *          (HOLD) even when SWITCH was correct. Added null guard and fallback.
 */

'use strict';

/* ═══════════════════════════════════════════════════════════════════════
   MATRIX — unchanged, correct
═══════════════════════════════════════════════════════════════════════ */
class Matrix {
  constructor(rows, cols) {
    this.rows = rows; this.cols = cols;
    this.data = new Float32Array(rows * cols);
  }
  get(r, c) { return this.data[r * this.cols + c]; }
  set(r, c, v) { this.data[r * this.cols + c] = v; }
  static zeros(r, c) { return new Matrix(r, c); }
  static random(r, c, scale) {
    var m = new Matrix(r, c);
    var fan = r + c;
    var s = scale || Math.sqrt(2.0 / fan);   // He init
    for (var i = 0; i < m.data.length; i++) {
      var u1 = Math.random() + 1e-10, u2 = Math.random();
      m.data[i] = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2) * s;
    }
    return m;
  }
  clone() { var m = new Matrix(this.rows, this.cols); m.data.set(this.data); return m; }
  copyFrom(src) { this.data.set(src.data); }
  toArray() { return Array.from(this.data); }
  static fromArray(rows, cols, arr) {
    var m = new Matrix(rows, cols); m.data.set(arr); return m;
  }
}

function relu(x) { return x > 0 ? x : 0; }
function reluDeriv(x) { return x > 0 ? 1 : 0; }

/* ═══════════════════════════════════════════════════════════════════════
   DENSE LAYER
   FIX 1: forward() cleaned up — no redundant double-write to lastOut.
   FIX 2: backward() uses lastOut that was stored during forward() — no
           extra forward call here, so activations are always correct.
═══════════════════════════════════════════════════════════════════════ */
class DenseLayer {
  constructor(inDim, outDim) {
    this.W  = Matrix.random(outDim, inDim);
    this.b  = Matrix.zeros(outDim, 1);
    this.dW = Matrix.zeros(outDim, inDim);
    this.db = Matrix.zeros(outDim, 1);
    this.mW = Matrix.zeros(outDim, inDim); this.vW = Matrix.zeros(outDim, inDim);
    this.mb = Matrix.zeros(outDim, 1);     this.vb = Matrix.zeros(outDim, 1);
    this.inDim  = inDim;
    this.outDim = outDim;
    this.lastIn  = null;
    this.lastOut = null;   // stores post-activation values for backward()
    this.lastPreAct = null; // FIX 2: also store pre-activation for correct ReLU deriv
  }

  // FIX 1: single clean write path for lastOut and lastPreAct
  forward(x, activate) {
    this.lastIn = x.slice();  // store input for weight gradient
    var preAct = new Float32Array(this.outDim);
    for (var r = 0; r < this.outDim; r++) {
      var s = this.b.data[r];
      for (var c = 0; c < this.inDim; c++) s += this.W.get(r, c) * x[c];
      preAct[r] = s;
    }
    this.lastPreAct = preAct;  // save BEFORE activation (needed for ReLU deriv)
    var out = new Float32Array(this.outDim);
    for (var r = 0; r < this.outDim; r++) {
      out[r] = activate ? relu(preAct[r]) : preAct[r];
    }
    this.lastOut = out;  // save post-activation (used downstream as input to next layer)
    return out;
  }

  // FIX 2: uses lastPreAct for ReLU derivative — always correct regardless of
  //         what happened between forward() and backward() calls.
  backward(dOut, activate) {
    var dAct = new Float32Array(this.outDim);
    for (var r = 0; r < this.outDim; r++) {
      // Use pre-activation value for ReLU derivative, not post-activation
      dAct[r] = activate ? dOut[r] * reluDeriv(this.lastPreAct[r]) : dOut[r];
    }
    // Accumulate weight gradients
    for (var r = 0; r < this.outDim; r++) {
      for (var c = 0; c < this.inDim; c++) {
        this.dW.set(r, c, this.dW.get(r, c) + dAct[r] * this.lastIn[c]);
      }
    }
    // Accumulate bias gradients
    for (var r = 0; r < this.outDim; r++) {
      this.db.data[r] += dAct[r];
    }
    // Propagate gradient to previous layer
    var dIn = new Float32Array(this.inDim);
    for (var c = 0; c < this.inDim; c++) {
      for (var r = 0; r < this.outDim; r++) {
        dIn[c] += this.W.get(r, c) * dAct[r];
      }
    }
    return dIn;
  }

  zeroGrad() {
    for (var i = 0; i < this.dW.data.length; i++) this.dW.data[i] = 0;
    for (var i = 0; i < this.db.data.length; i++) this.db.data[i] = 0;
  }

  adamStep(lr, t, beta1, beta2, eps) {
    beta1 = beta1 || 0.9; beta2 = beta2 || 0.999; eps = eps || 1e-8;
    var bc1 = 1 - Math.pow(beta1, t);
    var bc2 = 1 - Math.pow(beta2, t);
    for (var i = 0; i < this.W.data.length; i++) {
      this.mW.data[i] = beta1 * this.mW.data[i] + (1 - beta1) * this.dW.data[i];
      this.vW.data[i] = beta2 * this.vW.data[i] + (1 - beta2) * this.dW.data[i] ** 2;
      this.W.data[i] -= lr * (this.mW.data[i] / bc1) / (Math.sqrt(this.vW.data[i] / bc2) + eps);
    }
    for (var i = 0; i < this.b.data.length; i++) {
      this.mb.data[i] = beta1 * this.mb.data[i] + (1 - beta1) * this.db.data[i];
      this.vb.data[i] = beta2 * this.vb.data[i] + (1 - beta2) * this.db.data[i] ** 2;
      this.b.data[i] -= lr * (this.mb.data[i] / bc1) / (Math.sqrt(this.vb.data[i] / bc2) + eps);
    }
  }

  toJSON() {
    return { W: this.W.toArray(), b: this.b.toArray(), inDim: this.inDim, outDim: this.outDim };
  }
  static fromJSON(j) {
    var l = new DenseLayer(j.inDim, j.outDim);
    l.W = Matrix.fromArray(j.outDim, j.inDim, j.W);
    l.b = Matrix.fromArray(j.outDim, 1, j.b);
    return l;
  }
}

/* ═══════════════════════════════════════════════════════════════════════
   Q-NETWORK
   FIX 3 + FIX 4: backward() no longer calls forward() internally.
   train() does ONE forward pass, computes loss+delta, then calls backward().
   Gradients are now computed against the correct stored activations.
═══════════════════════════════════════════════════════════════════════ */
class QNetwork {
  constructor() {
    this.l1 = new DenseLayer(32, 128);
    this.l2 = new DenseLayer(128, 128);
    this.l3 = new DenseLayer(128, 64);
    this.l4 = new DenseLayer(64, 3);   // 3 Q-values: HOLD / SWITCH / EXTEND
    this.adamT = 0;
  }

  forward(state) {
    var x = new Float32Array(state);
    x = this.l1.forward(x, true);
    x = this.l2.forward(x, true);
    x = this.l3.forward(x, true);
    x = this.l4.forward(x, false);   // output layer — no activation
    return x;
  }

  // FIX 3: backward() receives the Q-values already computed by train().
  //         It does NOT call forward() internally anymore.
  //         dOut is the gradient of the loss w.r.t. the output Q-values.
  _backward(dOut) {
    var d = this.l4.backward(dOut, false);  // output layer has no ReLU
    d = this.l3.backward(d, true);
    d = this.l2.backward(d, true);
    this.l1.backward(d, true);
  }

  // FIX 4: single forward pass, immediate backward — no corrupted activations.
  train(state, action, target_q, lr) {
    // Zero gradients before accumulation
    this.l1.zeroGrad(); this.l2.zeroGrad();
    this.l3.zeroGrad(); this.l4.zeroGrad();

    // ONE forward pass — stores lastIn, lastOut, lastPreAct in every layer
    var q = this.forward(state);

    // Compute loss (MSE on the selected action's Q-value only)
    var loss = 0.5 * (q[action] - target_q) ** 2;

    // Gradient of loss w.r.t. each output neuron
    // Only the action taken has a non-zero gradient (selective update)
    var dOut = new Float32Array(3);
    dOut[action] = q[action] - target_q;

    // Backward pass — uses the activations stored during the forward() above
    this._backward(dOut);

    // Adam parameter update
    this.adamT++;
    this.l1.adamStep(lr, this.adamT);
    this.l2.adamStep(lr, this.adamT);
    this.l3.adamStep(lr, this.adamT);
    this.l4.adamStep(lr, this.adamT);

    return loss;
  }

  copyWeightsFrom(src) {
    function copyLayer(dst, s) { dst.W.copyFrom(s.W); dst.b.copyFrom(s.b); }
    copyLayer(this.l1, src.l1); copyLayer(this.l2, src.l2);
    copyLayer(this.l3, src.l3); copyLayer(this.l4, src.l4);
  }

  toJSON() {
    return {
      l1: this.l1.toJSON(), l2: this.l2.toJSON(),
      l3: this.l3.toJSON(), l4: this.l4.toJSON(),
      adamT: this.adamT
    };
  }
  static fromJSON(j) {
    var net = new QNetwork();
    if (j.l1 && j.l1.inDim !== 32) {
      console.warn('DQN: saved weights use input dim ' + j.l1.inDim + ', expected 32. Starting fresh.');
      return net;
    }
    net.l1 = DenseLayer.fromJSON(j.l1);
    net.l2 = DenseLayer.fromJSON(j.l2);
    net.l3 = DenseLayer.fromJSON(j.l3);
    net.l4 = DenseLayer.fromJSON(j.l4);
    net.adamT = j.adamT || 0;
    return net;
  }
}

/* ═══════════════════════════════════════════════════════════════════════
   DQN AGENT
   FIX 5: Reward rebalanced — crash penalty reduced from -5 to -2.
   FIX 6: Episode-end double save removed.
   FIX 7: pressureAction phase index lookup fixed with null guard.
═══════════════════════════════════════════════════════════════════════ */
var DQN = {
  online: null,
  target: null,
  replay: [],
  BUFFER_MAX:          2000,
  BATCH_SIZE:          32,
  GAMMA:               0.95,
  LR:                  0.0005,
  EPSILON:             1.0,
  EPS_MIN:             0.05,
  EPS_DECAY:           0.9985,
  TARGET_UPDATE_FREQ:  50,
  trainSteps:          0,
  totalSteps:          0,
  episodes:            0,
  lossHist:            [],
  rewardHist:          [],
  avgQHist:            [],
  rollingReward:       0,
  lastState:           null,
  lastAction:          null,
  lastQVals:           null,
  _savePending:        false,   // FIX 6: guard against double save

  init: function () {
    this.online = new QNetwork();
    this.target = new QNetwork();
    this.target.copyWeightsFrom(this.online);
    this.replay        = [];
    this.EPSILON       = 1.0;
    this.trainSteps    = 0;
    this.lossHist      = [];
    this.rewardHist    = [];
    this.episodes      = 0;
    this.totalSteps    = 0;
    this.rollingReward = 0;
    this.lastState     = null;
    this.lastAction    = null;
    this.lastQVals     = null;
    this._savePending  = false;
    this.updateUI();
    rlLog('DQN agent initialised — 32→128→128→64→3 network, Adam lr=' + this.LR);
  },

  STORAGE_KEY: 'dqn-model-v1',

  saveModel: async function () {
    if (this._savePending) return;   // FIX 6: prevent concurrent saves
    this._savePending = true;
    try {
      var payload = {
        online:        this.online.toJSON(),
        target:        this.target.toJSON(),
        epsilon:       this.EPSILON,
        trainSteps:    this.trainSteps,
        totalSteps:    this.totalSteps,
        episodes:      this.episodes,
        lossHist:      this.lossHist.slice(-120),
        rollingReward: this.rollingReward,
        savedAt:       Date.now()
      };
      var resp = await fetch('/save_weights', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(payload)
      });
      if (!resp.ok) throw new Error('HTTP ' + resp.status);
    } catch (e) {
      console.warn('DQN save failed:', e);
    } finally {
      this._savePending = false;   // always release guard
    }
  },

  loadModel: async function () {
    try {
      var resp = await fetch('/load_weights');
      if (!resp.ok) throw new Error('HTTP ' + resp.status);
      var json = await resp.json();
      if (!json.found || !json.data) return false;
      var d = json.data;
      this.online        = QNetwork.fromJSON(d.online);
      this.target        = QNetwork.fromJSON(d.target);
      this.EPSILON       = typeof d.epsilon   === 'number' ? d.epsilon   : 1.0;
      this.trainSteps    = d.trainSteps    || 0;
      this.totalSteps    = d.totalSteps    || 0;
      this.episodes      = d.episodes      || 0;
      this.lossHist      = d.lossHist      || [];
      this.rollingReward = d.rollingReward || 0;
      rlLog('Model restored · ε=' + this.EPSILON.toFixed(3) +
            ' · episodes=' + this.episodes + ' · steps=' + this.totalSteps, 'ok');
      return true;
    } catch (e) {
      rlLog('No saved model on server — starting fresh', 'warn');
      return false;
    }
  },

  // Save every 50 train steps — guard prevents concurrent HTTP requests
  maybeSave: function () {
    if (this.trainSteps > 0 && this.trainSteps % 50 === 0) {
      this.saveModel();
    }
  },

  extractState: function (obs) {
    if (!obs) return new Float32Array(32);
    var state = new Float32Array(32);
    var ql = obs.queue_lengths || [];
    for (var i = 0; i < 12; i++) state[i] = Math.min(Math.max(ql[i] || 0, 0), 1);
    var ph = obs.phase_onehot || [1, 0, 0, 0];
    for (var i = 0; i < 4; i++) state[12 + i] = ph[i] || 0;
    state[16] = Math.min(Math.max(obs.phase_elapsed_norm   || 0, 0), 1);
    state[17] = ((obs.pressure_differential || 0) + 1) / 2;
    state[18] = Math.min(Math.max(obs.avg_delay_norm       || 0, 0), 1);
    state[19] = Math.min(Math.max(obs.fairness_score       || 0, 0), 1);
    var sp = obs.spillback_flags || [];
    for (var i = 0; i < 12; i++) state[20 + i] = sp[i] || 0;
    return state;
  },

  // FIX 5: crash penalty reduced from -5 to -2 so clearance reward dominates.
  //         The agent was learning to do nothing to avoid crashes.
  computeReward: function (info) {
    if (!info) return 0;
    var r = 0;
    r += (info.step_cleared || 0) * 1.0;              // +1 per vehicle cleared
    r -= ((info.ns_queue || 0) + (info.ew_queue || 0)) * 0.05;  // pressure penalty
    r -= (info.step_crashes || 0) * 2.0;              // FIX 5: was -5.0, now -2.0
    r -= (info.avg_delay   || 0) * 0.02;              // delay penalty
    if (info.los === 'A' || info.los === 'B') r += 0.5;
    if (info.los === 'F') r -= 0.5;
    return r;
  },

  selectAction: function (obs) {
    var state = this.extractState(obs);
    this.lastState = state;
    var qVals = this.online.forward(state);
    this.lastQVals = qVals;
    var action;
    if (Math.random() < this.EPSILON) {
      action = Math.floor(Math.random() * 3);
    } else {
      action = 0;
      for (var i = 1; i < 3; i++) if (qVals[i] > qVals[action]) action = i;
    }
    this.lastAction = action;
    return action;
  },

  step: function (nextObs, reward, done) {
    if (this.lastState === null) return;
    var nextState = this.extractState(nextObs);
    this.replay.push({ s: this.lastState, a: this.lastAction, r: reward, ns: nextState, done: done ? 1 : 0 });
    if (this.replay.length > this.BUFFER_MAX) this.replay.shift();

    this.totalSteps++;
    this.rollingReward = 0.95 * this.rollingReward + 0.05 * reward;

    if (this.replay.length >= this.BATCH_SIZE) {
      this.trainBatch();
    }
    if (this.EPSILON > this.EPS_MIN) this.EPSILON *= this.EPS_DECAY;

    this.updateUI();
    this.maybeSave();
  },

  trainBatch: function () {
    var batch = [];
    // Sample without replacement up to BATCH_SIZE (avoids duplicate gradients)
    var indices = [];
    for (var i = 0; i < this.replay.length; i++) indices.push(i);
    // Fisher-Yates shuffle first BATCH_SIZE elements
    for (var i = 0; i < this.BATCH_SIZE; i++) {
      var j = i + Math.floor(Math.random() * (indices.length - i));
      var tmp = indices[i]; indices[i] = indices[j]; indices[j] = tmp;
      batch.push(this.replay[indices[i]]);
    }

    var totalLoss = 0;
    for (var bi = 0; bi < batch.length; bi++) {
      var tr = batch[bi];
      var targetQ;
      if (tr.done) {
        targetQ = tr.r;
      } else {
        // Double DQN: online selects best action, target evaluates it
        var nextQOnline = this.online.forward(tr.ns);
        var bestA = 0;
        for (var i = 1; i < 3; i++) if (nextQOnline[i] > nextQOnline[bestA]) bestA = i;
        var nextQTarget = this.target.forward(tr.ns);
        targetQ = tr.r + this.GAMMA * nextQTarget[bestA];
      }
      // FIX 4 applied here: train() does one clean forward+backward
      var loss = this.online.train(tr.s, tr.a, targetQ, this.LR);
      totalLoss += loss;
    }

    this.trainSteps++;
    var avgLoss = totalLoss / this.BATCH_SIZE;
    this.lossHist.push(avgLoss);
    if (this.lossHist.length > 120) this.lossHist.shift();

    if (this.trainSteps % this.TARGET_UPDATE_FREQ === 0) {
      this.target.copyWeightsFrom(this.online);
      rlLog('Target network synced (train step ' + this.trainSteps + ')');
    }
    return avgLoss;
  },

  updateUI: function () {
    var st = function (id, v) { var e = document.getElementById(id); if (e) e.textContent = v; };
    st('rl-episodes', this.episodes);
    st('rl-buffer',   this.replay.length + ' / ' + this.BUFFER_MAX);
    st('rl-epsilon',  this.EPSILON.toFixed(3));
    var lastLoss = this.lossHist.length ? this.lossHist[this.lossHist.length - 1].toFixed(4) : '—';
    st('rl-loss-val', lastLoss);
    st('bab-eps', this.EPSILON.toFixed(2));

    var TRAIN_TARGET = 10000;
    var pct = Math.min(Math.round(this.trainSteps / TRAIN_TARGET * 100), 99);
    if (this.trainSteps >= TRAIN_TARGET && this.EPSILON <= this.EPS_MIN + 0.01) pct = 100;
    var barEl = document.getElementById('rl-train-bar');
    if (barEl) barEl.style.width = pct + '%';
    st('rl-train-pct', pct + '%');

    var maxReward = 10;
    var rPct = Math.min(Math.max(this.rollingReward / maxReward, 0), 1) * 100;
    var rbar = document.getElementById('rl-reward-bar');
    if (rbar) rbar.style.width = rPct + '%';
    st('rl-reward-val', this.rollingReward.toFixed(2));

    var badge = document.getElementById('rl-status-badge');
    if (badge) {
      if (this.replay.length < this.BATCH_SIZE) {
        badge.textContent = 'WARMING UP';
        badge.style.cssText = 'background:rgba(229,83,75,0.15);color:#e5534b;border-color:rgba(229,83,75,0.3)';
      } else if (pct < 30) {
        badge.textContent = 'EXPLORING';
        badge.style.cssText = 'background:rgba(88,166,255,0.15);color:#58a6ff;border-color:rgba(88,166,255,0.3)';
      } else if (pct < 70) {
        badge.textContent = 'LEARNING';
        badge.style.cssText = 'background:rgba(212,168,75,0.15);color:#d4a84b;border-color:rgba(212,168,75,0.3)';
      } else {
        badge.textContent = 'EXPLOITING';
        badge.style.cssText = 'background:rgba(62,207,142,0.15);color:#3ecf8e;border-color:rgba(62,207,142,0.3)';
      }
    }

    if (this.lastQVals) {
      var bestA = 0;
      for (var i = 1; i < 3; i++) if (this.lastQVals[i] > this.lastQVals[bestA]) bestA = i;
      ['rl-q0', 'rl-q1', 'rl-q2'].forEach(function (id, i) {
        var e = document.getElementById(id); if (!e) return;
        e.textContent = DQN.lastQVals[i] !== undefined ? DQN.lastQVals[i].toFixed(3) : '—';
        e.className   = 'rl-qval-num ' + (i === bestA ? 'best' : 'other');
      });
      var avgQ = (this.lastQVals[0] + this.lastQVals[1] + this.lastQVals[2]) / 3;
      st('dm-qval',        avgQ.toFixed(3));
      st('bab-qval',       avgQ.toFixed(2));
      st('bab-rl-action',  ['HOLD', 'SWITCH', 'EXTEND'][this.lastAction !== null ? this.lastAction : 0]);
      st('bab-rl-loss',    lastLoss);
    }
    drawRLLossChart();
  }
};

function rlLog(msg) { log(msg, 'rl'); }

/* ═══════════════════════════════════════════════════════════════════════
   POLICY HELPERS
   FIX 7: pressureAction — safe phase index lookup with Array.from()
           so indexOf works correctly on regular arrays, not Float32Arrays.
═══════════════════════════════════════════════════════════════════════ */
function pressureAction(obs) {
  if (!obs) return 0;
  var ql = obs.queue_lengths || [];
  // FIX 7: phase_onehot may arrive as a plain array or typed array.
  //         Convert to a regular Array before indexOf so it works reliably.
  var ph = Array.from(obs.phase_onehot || [1, 0, 0, 0]);
  var elapsed = (obs.phase_elapsed_norm || 0) * 90;
  if (elapsed < 5) return 0;  // never switch within first 5s of a phase

  var ns = [0, 1, 2, 3, 8, 9].reduce(function (s, i) { return s + (ql[i] || 0); }, 0);
  var ew = [4, 5, 6, 7, 10, 11].reduce(function (s, i) { return s + (ql[i] || 0); }, 0);

  // FIX 7: indexOf on Array.from result is reliable
  var maxPh = Math.max.apply(null, ph);
  var pi = ph.indexOf(maxPh);
  if (pi < 0) pi = 0;   // fallback: treat as NS_GREEN

  if (pi === 0 && ew - ns > 0.3) return 1;  // NS active, EW much longer → switch
  if (pi === 1 && ns - ew > 0.3) return 1;  // EW active, NS much longer → switch
  if (pi === 2) return 0;                    // ALL_RED → hold
  if (pi === 0 && ns > 0.75)     return 2;  // NS active, NS very heavy → extend
  if (pi === 1 && ew > 0.75)     return 2;  // EW active, EW very heavy → extend
  return 0;
}

function dqnActionToApiAction(dqnAction) {
  var map = [0, 1, 2];
  return map[dqnAction] !== undefined ? map[dqnAction] : 0;
}

function dqnPolicy(obs, prevInfo) {
  if (DQN.lastState !== null && prevInfo !== null) {
    var reward = DQN.computeReward(prevInfo);
    DQN.step(obs, reward, false);
  }
  var action = DQN.selectAction(obs);
  return dqnActionToApiAction(action);
}

/* ═══════════════════════════════════════════════════════════════════════
   EPISODE-END HANDLER (FIX 6 — remove double saveModel call)
   Replace the done-block inside applySimSpeed() with this logic.
   The explicit DQN.saveModel() after DQN.step() is removed because
   DQN.step() already calls maybeSave() internally. We only add a
   single deliberate save with a 200ms delay to let maybeSave finish first.
═══════════════════════════════════════════════════════════════════════ */
function handleEpisodeDone(sd) {
  running = false;
  clearInterval(runInterval);
  runInterval = null;
  _episodeFrozen = true;

  if (opMode === 'rl' && DQN.lastState !== null) {
    var finalReward = DQN.computeReward(sd.info || {});
    // step() calls maybeSave() internally — do NOT call saveModel() immediately after
    DQN.step(sd.observation, finalReward, true);
    DQN.episodes++;
    DQN.updateUI();
    rlLog('Episode done · replay=' + DQN.replay.length +
          ' · ε=' + DQN.EPSILON.toFixed(3) +
          ' · steps=' + DQN.totalSteps);
    // FIX 6: single deliberate end-of-episode save, delayed so maybeSave() finishes first
    setTimeout(function () { DQN.saveModel(); }, 250);
  }
  doGrade();
  document.getElementById('status-txt').textContent = 'Episode complete ✓ — metrics preserved';
  log('Episode finished · efficiency=' + effPct().toFixed(1) + '%', 'ok');
}
