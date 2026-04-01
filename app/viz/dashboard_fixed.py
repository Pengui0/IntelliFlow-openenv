"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IntelliFlow — Traffic Operations Centre</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Fraunces:opsz,wght@9..144,700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/babylonjs/6.26.0/babylon.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babylonjs-materials/6.26.0/babylonjs.materials.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babylonjs-procedural-textures/6.26.0/babylonjs.proceduralTextures.min.js"></script>
<style>
:root{
  --bg:#111318;--bg-panel:#181c23;--bg-card:#1e2330;--bg-raised:#242938;--bg-input:#141720;
  --border:rgba(255,255,255,0.07);--border-mid:rgba(255,255,255,0.12);--border-str:rgba(255,255,255,0.18);
  --sand:#d4a84b;--sand-lt:#e8c068;--sand-dim:rgba(212,168,75,0.12);
  --green:#3ecf8e;--green-dim:rgba(62,207,142,0.12);
  --red:#e5534b;--red-dim:rgba(229,83,75,0.12);
  --blue:#58a6ff;--blue-dim:rgba(88,166,255,0.10);
  --purple:#a78bfa;--purple-dim:rgba(167,139,250,0.12);
  --text:#cdd5e0;--text-dim:#6e7b8e;--text-faint:#3a4252;
  --shadow:0 2px 12px rgba(0,0,0,0.4);--shadow-lg:0 8px 32px rgba(0,0,0,0.5);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{font-size:13px;}
body{font-family:'Sora',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden;}
.shell{max-width:1700px;margin:0 auto;padding:16px 20px 32px;}
.header{display:flex;align-items:center;justify-content:space-between;padding-bottom:14px;margin-bottom:16px;border-bottom:1px solid var(--border);}
.brand{display:flex;align-items:center;gap:12px;}
.brand-mark{width:38px;height:38px;border-radius:9px;background:linear-gradient(135deg,#2a3040,#1e2330);border:1px solid var(--border-mid);display:flex;align-items:center;justify-content:center;box-shadow:var(--shadow);flex-shrink:0;}
.brand-mark svg{width:20px;height:20px;}
.brand-name{font-family:'Fraunces',serif;font-size:19px;font-weight:700;color:#e8e8ea;letter-spacing:-0.01em;line-height:1;}
.brand-sub{font-size:10px;color:var(--text-dim);margin-top:2px;letter-spacing:0.04em;}
.header-right{display:flex;align-items:center;gap:20px;}
.live-pill{display:flex;align-items:center;gap:7px;background:var(--green-dim);border:1px solid rgba(62,207,142,0.2);border-radius:20px;padding:4px 11px 4px 8px;font-size:11px;font-weight:500;color:var(--green);}
.live-dot{width:6px;height:6px;border-radius:50%;background:var(--green);animation:breathe 2s ease-in-out infinite;}
@keyframes breathe{0%,100%{opacity:1;transform:scale(1);}50%{opacity:0.3;transform:scale(0.6);}}
.clock{text-align:right;}
.clock-t{font-family:'JetBrains Mono',monospace;font-size:17px;font-weight:500;color:#e8e8ea;letter-spacing:0.04em;line-height:1;}
.clock-d{font-size:10px;color:var(--text-dim);margin-top:2px;}
.ctrl-bar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:var(--bg-panel);border:1px solid var(--border);border-radius:10px;padding:10px 14px;margin-bottom:16px;box-shadow:var(--shadow);}
.ctrl-lbl{font-size:10px;font-weight:500;color:var(--text-dim);letter-spacing:0.05em;white-space:nowrap;}
.ctrl-sep{width:1px;height:20px;background:var(--border);flex-shrink:0;}
select,input[type=number]{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--text);background:var(--bg-input);border:1px solid var(--border-mid);border-radius:7px;padding:6px 10px;outline:none;appearance:none;transition:border-color .15s;cursor:pointer;}
select{padding-right:26px;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%236e7b8e'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 8px center;}
select:focus,input:focus{border-color:var(--sand);}
.btn{font-family:'Sora',sans-serif;font-size:11px;font-weight:600;letter-spacing:0.03em;border:none;border-radius:7px;padding:7px 14px;cursor:pointer;transition:all .15s;display:flex;align-items:center;gap:5px;white-space:nowrap;}
.btn-primary{background:var(--sand);color:#111318;box-shadow:0 2px 8px rgba(212,168,75,0.25);}
.btn-primary:hover{background:var(--sand-lt);transform:translateY(-1px);}
.btn-green{background:var(--green);color:#0d1f16;}
.btn-green:hover{background:#5edaa8;transform:translateY(-1px);}
.btn-purple{background:var(--purple);color:#0f0d1f;box-shadow:0 2px 8px rgba(167,139,250,0.25);}
.btn-purple:hover{background:#bda9ff;transform:translateY(-1px);}
.btn-ghost{background:var(--bg-raised);color:var(--text-dim);border:1px solid var(--border-mid);}
.btn-ghost:hover{background:var(--bg-card);color:var(--text);}
.status-pill{margin-left:auto;font-size:11px;color:var(--text-dim);background:var(--bg-input);border:1px solid var(--border);border-radius:20px;padding:4px 12px;font-family:'JetBrains Mono',monospace;min-width:200px;text-align:center;}
.kpi-strip{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:14px;}
.kpi{background:var(--bg-panel);border:1px solid var(--border);border-radius:10px;padding:14px 16px;position:relative;overflow:hidden;transition:border-color .2s;}
.kpi:hover{border-color:var(--border-mid);}
.kpi-accent{position:absolute;bottom:0;left:16px;right:16px;height:2px;border-radius:2px 2px 0 0;background:var(--kpi-c,var(--sand));opacity:0.6;}
.kpi-lbl{font-size:9px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:var(--text-dim);margin-bottom:8px;}
.kpi-val{font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:500;color:var(--text);line-height:1;letter-spacing:-0.02em;}
.kpi-val.lg{font-size:28px;}
.kpi-sub{font-size:10px;color:var(--text-dim);margin-top:5px;}
.phase-tag{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:500;padding:3px 9px;border-radius:5px;margin-bottom:4px;}
.ph-NS_GREEN{background:var(--green-dim);color:var(--green);border:1px solid rgba(62,207,142,0.22);}
.ph-EW_GREEN{background:var(--blue-dim);color:var(--blue);border:1px solid rgba(88,166,255,0.22);}
.ph-ALL_RED{background:var(--red-dim);color:var(--red);border:1px solid rgba(229,83,75,0.22);}
.ph-NS_MINOR{background:var(--sand-dim);color:var(--sand);border:1px solid rgba(212,168,75,0.22);}
@keyframes kpi-pop{0%{opacity:0.5;}50%{color:var(--sand);}100%{opacity:1;}}
.pop{animation:kpi-pop .4s ease;}
.main-grid{display:grid;grid-template-columns:1fr 310px;gap:14px;}
.left-col{display:flex;flex-direction:column;gap:14px;}
.right-col{display:flex;flex-direction:column;gap:14px;}
.panel{background:var(--bg-panel);border:1px solid var(--border);border-radius:12px;padding:18px;box-shadow:var(--shadow);}
.panel-hd{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;}
.panel-title{font-size:10px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:var(--text-dim);}
.panel-tag{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--text-faint);background:var(--bg-raised);border:1px solid var(--border);border-radius:4px;padding:2px 7px;}
.intersection-wrap{display:flex;gap:12px;align-items:flex-start;}
.map-canvas-wrap{flex-shrink:0;position:relative;width:580px;height:580px;border-radius:14px;overflow:hidden;border:1px solid var(--border-mid);box-shadow:0 0 0 1px rgba(255,255,255,0.04),0 8px 32px rgba(0,0,0,0.6);}
canvas#sat-canvas{position:absolute;inset:0;width:100%;height:100%;}
canvas#road-canvas{position:absolute;inset:0;width:100%;height:100%;}
canvas#car-canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;}
canvas#booth-hint-canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:5;}
.map-aside{flex:1;display:flex;flex-direction:column;gap:8px;min-width:0;}
.sig-panel{background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:14px;}
.sig-lbl{font-size:9px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:var(--text-dim);margin-bottom:10px;}
.sig-row{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;}
.sig-cell{display:flex;flex-direction:column;align-items:center;gap:5px;}
.sig-dir{font-family:'JetBrains Mono',monospace;font-size:9px;color:var(--text-dim);}
.lamp{width:30px;height:30px;border-radius:50%;background:var(--bg-raised);border:1.5px solid var(--border-mid);position:relative;overflow:hidden;transition:box-shadow .3s,background .3s;}
.lamp.green{background:#1a4a30;box-shadow:0 0 0 3px rgba(62,207,142,0.15),0 0 14px rgba(62,207,142,0.5);}
.lamp.green::after{content:'';position:absolute;inset:5px;border-radius:50%;background:var(--green);opacity:0.9;}
.lamp.red{background:#3a1518;}
.lamp.red::after{content:'';position:absolute;inset:5px;border-radius:50%;background:var(--red);opacity:0.5;}
.prog-block{background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:14px;}
.prog-row{display:flex;justify-content:space-between;margin-bottom:8px;font-size:10px;}
.prog-lbl{font-weight:500;color:var(--text-dim);}
.prog-nums{font-family:'JetBrains Mono',monospace;color:var(--text);}
.prog-track{height:5px;background:var(--bg-raised);border-radius:3px;overflow:hidden;}
.prog-fill{height:100%;background:linear-gradient(90deg,var(--sand),var(--sand-lt));border-radius:3px;transition:width .5s cubic-bezier(.4,0,.2,1);}
.score-block{background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:14px;display:flex;align-items:center;gap:14px;}
.ring-wrap{flex-shrink:0;width:78px;height:78px;position:relative;}
.ring-wrap svg{width:100%;height:100%;}
.ring-center{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.ring-val{font-family:'JetBrains Mono',monospace;font-size:16px;font-weight:500;color:var(--text);line-height:1;}
.ring-lbl-sm{font-size:9px;color:var(--text-dim);margin-top:1px;}
.score-info{flex:1;}
.score-stars{font-size:18px;letter-spacing:3px;margin-bottom:5px;}
.score-note{font-size:11px;color:var(--text-dim);line-height:1.5;}
.los-panel{display:grid;grid-template-columns:repeat(6,1fr);gap:0;border:1px solid var(--border);border-radius:8px;overflow:hidden;}
.los-cell{padding:10px 6px;text-align:center;border-right:1px solid var(--border);position:relative;transition:background .3s;}
.los-cell:last-child{border-right:none;}
.los-cell.active{background:var(--los-bg,var(--bg-raised));}
.los-letter{font-family:'JetBrains Mono',monospace;font-size:18px;font-weight:500;color:var(--text-faint);transition:color .3s;}
.los-cell.active .los-letter{color:var(--los-c,var(--text));text-shadow:0 0 12px var(--los-glow,transparent);}
.los-delay{font-size:9px;color:var(--text-dim);margin-top:3px;font-family:'JetBrains Mono',monospace;}
.los-bar{position:absolute;bottom:0;left:0;right:0;height:3px;background:var(--los-c,transparent);opacity:0;transition:opacity .3s;}
.los-cell.active .los-bar{opacity:1;}
.sparkline-wrap{width:100%;height:60px;}
canvas.sparkline{width:100%;height:100%;display:block;}
.lane-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px 20px;}
.lane-item{display:flex;flex-direction:column;gap:3px;}
.lane-label{display:flex;justify-content:space-between;font-size:10px;}
.lane-name{color:var(--text-dim);font-weight:500;}
.lane-pct{font-family:'JetBrains Mono',monospace;color:var(--text);font-size:10px;}
.lane-track{height:4px;background:var(--bg-raised);border-radius:2px;overflow:hidden;}
.lane-fill{height:100%;border-radius:2px;transition:width .35s ease,background .35s ease;}
.metric-list{display:flex;flex-direction:column;}
.mrow{display:flex;align-items:center;justify-content:space-between;padding:7px 0;border-bottom:1px solid var(--border);}
.mrow:last-child{border-bottom:none;}
.mkey{font-size:11px;color:var(--text-dim);}
.mval{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--text);}
.mval.g{color:var(--green);}.mval.a{color:var(--sand);}.mval.r{color:var(--red);}.mval.p{color:var(--purple);}
.log-box{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--text-dim);line-height:1.9;overflow-y:auto;max-height:320px;scrollbar-width:thin;}
.log-row{display:flex;gap:10px;border-bottom:1px solid var(--border);padding:1px 0;}
.log-ts{color:var(--text-faint);flex-shrink:0;}
.log-msg{color:var(--text);}
.log-msg.ok{color:var(--green);}.log-msg.warn{color:var(--sand);}.log-msg.err{color:var(--red);}.log-msg.rl{color:var(--purple);}
.dir-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px 20px;}
.dir-block{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:12px;}
.dir-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;}
.dir-lbl{font-size:10px;font-weight:600;letter-spacing:0.06em;}
.dir-total{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--text-dim);}
.dlane{display:flex;align-items:center;gap:7px;margin-bottom:5px;}
.dlane:last-child{margin-bottom:0;}
.dlane-nm{font-size:9px;color:var(--text-dim);width:52px;flex-shrink:0;}
.dlane-track{flex:1;height:7px;background:var(--bg-raised);border-radius:3px;overflow:hidden;}
.dlane-fill{height:100%;border-radius:3px;transition:width .35s ease,background .3s;}
.dlane-pct{font-family:'JetBrains Mono',monospace;font-size:9px;width:26px;text-align:right;flex-shrink:0;}
.corner-score{position:absolute;top:0;width:148px;background:rgba(8,11,18,0.85);border:1px solid rgba(255,255,255,0.12);z-index:20;display:flex;flex-direction:column;align-items:center;padding:10px 12px 12px;gap:4px;pointer-events:none;backdrop-filter:blur(6px);}
.corner-score.left{left:0;border-radius:0 0 10px 0;border-top:none;border-left:none;}
.corner-score.right{right:0;border-radius:0 0 0 10px;border-top:none;border-right:none;}
.cs-label{font-size:8px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:rgba(255,255,255,0.4);}
.cs-val{font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:500;line-height:1;}
.cs-val.green{color:#3ecf8e;}.cs-val.red{color:#e5534b;}
.cs-delta{font-family:'JetBrains Mono',monospace;font-size:11px;height:14px;transition:opacity .4s;}
.cs-delta.green{color:#3ecf8e;}.cs-delta.red{color:#e5534b;}
.cs-bar-track{width:112px;height:4px;background:rgba(255,255,255,0.1);border-radius:2px;overflow:hidden;}
.cs-bar-fill{height:100%;border-radius:2px;transition:width .35s ease;}
.cs-bar-fill.green{background:#3ecf8e;}.cs-bar-fill.red{background:#e5534b;}
.vol-bar{position:absolute;top:0;bottom:0;width:18px;display:flex;flex-direction:column;justify-content:flex-end;padding:8px 3px;gap:2px;z-index:10;pointer-events:none;background:rgba(5,8,15,0.6);backdrop-filter:blur(4px);}
.vol-bar.left{left:0;border-right:1px solid rgba(255,255,255,0.07);}
.vol-bar.right{right:0;border-left:1px solid rgba(255,255,255,0.07);}
.vol-seg{width:12px;height:6px;border-radius:1px;margin:0 auto;background:rgba(255,255,255,0.05);transition:background 0.15s;}
.map-coord{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);font-family:'JetBrains Mono',monospace;font-size:9px;color:rgba(255,255,255,0.5);background:rgba(0,0,0,0.55);padding:2px 8px;border-radius:3px;pointer-events:none;z-index:15;letter-spacing:0.06em;backdrop-filter:blur(4px);}
.decision-panel{background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:14px;}
.decision-phase{display:flex;align-items:center;gap:8px;margin-bottom:10px;}
.decision-reason-list{display:flex;flex-direction:column;gap:5px;}
.decision-reason{display:flex;align-items:flex-start;gap:7px;font-size:10px;color:var(--text-dim);line-height:1.4;}
.decision-reason-dot{width:5px;height:5px;border-radius:50%;flex-shrink:0;margin-top:4px;}
.decision-reason-dot.green{background:var(--green);}.decision-reason-dot.red{background:var(--red);}
.decision-reason-dot.sand{background:var(--sand);}.decision-reason-dot.blue{background:var(--blue);}.decision-reason-dot.purple{background:var(--purple);}
.decision-predicted{margin-top:10px;padding-top:10px;border-top:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;}
.decision-predicted-lbl{font-size:9px;color:var(--text-dim);}
.decision-predicted-val{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--green);}
.trend-panel{background:var(--bg-panel);border:1px solid var(--border);border-radius:12px;padding:18px;box-shadow:var(--shadow);}
.trend-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;}
.trend-chart-wrap{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:10px;}
.trend-chart-hd{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;}
.trend-chart-lbl{font-size:9px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--text-dim);}
.trend-chart-val{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--text);}
canvas.trend-canvas{width:100%;height:54px;display:block;border-radius:4px;}
.sat-row{display:flex;align-items:center;gap:6px;margin-top:4px;}
.sat-label{font-size:9px;color:var(--text-faint);width:32px;flex-shrink:0;}
.sat-track{flex:1;height:3px;background:var(--bg-raised);border-radius:2px;overflow:hidden;}
.sat-fill{height:100%;border-radius:2px;transition:width .35s ease,background .3s;}
.sat-val{font-family:'JetBrains Mono',monospace;font-size:9px;width:28px;text-align:right;color:var(--text-dim);}
.summary-card{background:var(--bg-panel);border:1px solid var(--border);border-radius:10px;padding:14px 18px;margin-bottom:14px;}
.summary-card-title{font-size:9px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--text-faint);margin-bottom:12px;}
.summary-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:0;}
.summary-item{padding:0 14px;border-right:1px solid var(--border);}
.summary-item:first-child{padding-left:0;}
.summary-item:last-child{border-right:none;}
.summary-item-lbl{font-size:9px;color:var(--text-faint);letter-spacing:0.05em;text-transform:uppercase;margin-bottom:4px;}
.summary-item-val{font-family:'JetBrains Mono',monospace;font-size:15px;font-weight:500;color:var(--text);line-height:1;}
.summary-item-sub{font-size:9px;color:var(--text-faint);margin-top:3px;}
.booth-tooltip{position:absolute;transform:translateX(-50%);background:rgba(0,0,0,0.85);border:1px solid rgba(212,168,75,0.35);color:#d4a84b;font-family:'JetBrains Mono',monospace;font-size:10px;padding:5px 10px;border-radius:5px;pointer-events:none;white-space:nowrap;backdrop-filter:blur(8px);opacity:0;transition:opacity .2s;z-index:30;}
.booth-tooltip.show{opacity:1;}

/* ── RL AGENT PANEL ── */
.rl-panel{background:linear-gradient(135deg,rgba(167,139,250,0.06),rgba(88,166,255,0.04));border:1px solid rgba(167,139,250,0.2);border-radius:12px;padding:16px;margin-bottom:14px;}
.rl-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;}
.rl-title{font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--purple);display:flex;align-items:center;gap:7px;}
.rl-dot{width:6px;height:6px;border-radius:50%;background:var(--purple);animation:breathe 1.5s ease-in-out infinite;}
.rl-badge{font-family:'JetBrains Mono',monospace;font-size:9px;padding:2px 8px;border-radius:4px;background:var(--purple-dim);color:var(--purple);border:1px solid rgba(167,139,250,0.25);}
.rl-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:10px;}
.rl-metric{background:var(--bg-card);border:1px solid var(--border);border-radius:7px;padding:9px 10px;}
.rl-metric-lbl{font-size:8px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:var(--text-dim);margin-bottom:5px;}
.rl-metric-val{font-family:'JetBrains Mono',monospace;font-size:14px;color:var(--purple);}
.rl-network{display:flex;align-items:center;gap:12px;background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:10px 14px;margin-bottom:10px;}
.rl-network-lbl{font-size:9px;color:var(--text-dim);flex-shrink:0;}
.rl-network-arch{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--text);}
.rl-qvals{display:flex;gap:6px;margin-left:auto;}
.rl-qval{display:flex;flex-direction:column;align-items:center;gap:2px;}
.rl-qval-lbl{font-size:8px;color:var(--text-faint);}
.rl-qval-num{font-family:'JetBrains Mono',monospace;font-size:10px;}
.rl-qval-num.best{color:var(--green);}.rl-qval-num.other{color:var(--text-dim);}
.rl-train-bar-wrap{display:flex;align-items:center;gap:8px;}
.rl-train-bar-lbl{font-size:9px;color:var(--text-dim);width:80px;flex-shrink:0;}
.rl-train-bar-track{flex:1;height:5px;background:var(--bg-raised);border-radius:3px;overflow:hidden;}
.rl-train-bar-fill{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--purple),#7c3aed);transition:width .4s ease;}
.rl-train-bar-val{font-family:'JetBrains Mono',monospace;font-size:9px;color:var(--purple);width:40px;text-align:right;flex-shrink:0;}
canvas#rl-loss-canvas{display:block;width:100%;height:40px;border-radius:4px;background:var(--bg-card);border:1px solid var(--border);margin-top:8px;}

/* BABYLON OVERLAY */
#babylon-overlay{display:none;position:fixed;inset:0;z-index:9999;background:#050810;opacity:0;transition:opacity 0.4s ease;flex-direction:column;}
#babylon-overlay.open{display:flex;}
#babylon-overlay.visible{opacity:1;}
#babylon-canvas-wrap{flex:1;position:relative;overflow:hidden;}
#babylonCanvas{width:100%;height:100%;display:block;outline:none;touch-action:none;}
#bab-hud{position:absolute;top:0;left:0;right:0;height:60px;background:linear-gradient(180deg,rgba(2,4,12,0.97) 0%,rgba(2,4,12,0.0) 100%);display:flex;align-items:stretch;z-index:30;pointer-events:none;}
.bab-metric{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 22px;border-right:1px solid rgba(255,255,255,0.06);flex:1;gap:2px;}
.bab-metric:last-child{border-right:none;}
.bab-mlbl{font-size:8px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:rgba(255,255,255,0.32);}
.bab-mval{font-family:'JetBrains Mono',monospace;font-size:20px;font-weight:500;line-height:1;color:#cdd5e0;}
.bab-mval.green{color:#3ecf8e;}.bab-mval.red{color:#e5534b;}.bab-mval.sand{color:#d4a84b;}.bab-mval.purple{color:#a78bfa;}
#bab-controls{position:absolute;bottom:0;left:0;right:0;padding:14px 20px;background:linear-gradient(0deg,rgba(2,4,12,0.97) 0%,rgba(2,4,12,0.0) 100%);display:flex;align-items:center;gap:10px;z-index:30;pointer-events:all;}
.bab-btn{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:500;background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.14);color:rgba(255,255,255,0.55);border-radius:6px;padding:8px 16px;cursor:pointer;transition:all .15s;white-space:nowrap;}
.bab-btn:hover{background:rgba(255,255,255,0.14);color:#fff;}
.bab-btn.active{background:rgba(212,168,75,0.18);border-color:rgba(212,168,75,0.5);color:#d4a84b;}
.bab-sep{width:1px;height:28px;background:rgba(255,255,255,0.08);}
.bab-phase-btn{font-family:'JetBrains Mono',monospace;font-size:10px;background:transparent;border:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.35);border-radius:6px;padding:8px 14px;cursor:pointer;transition:all .15s;}
.bab-phase-btn:hover{border-color:rgba(255,255,255,0.25);color:rgba(255,255,255,0.7);}
.bab-phase-btn.ns-on{border-color:rgba(62,207,142,0.55);color:#3ecf8e;background:rgba(62,207,142,0.08);}
.bab-phase-btn.ew-on{border-color:rgba(212,168,75,0.55);color:#d4a84b;background:rgba(212,168,75,0.08);}
.bab-phase-btn.rl-on{border-color:rgba(167,139,250,0.55);color:#a78bfa;background:rgba(167,139,250,0.08);}
.bab-exit{margin-left:auto;font-family:'Sora',sans-serif;font-size:10px;font-weight:600;background:rgba(229,83,75,0.1);border:1px solid rgba(229,83,75,0.28);color:rgba(229,83,75,0.75);border-radius:6px;padding:8px 18px;cursor:pointer;transition:all .15s;}
.bab-exit:hover{background:rgba(229,83,75,0.22);color:#e5534b;}
#bab-compass{position:absolute;right:20px;top:76px;width:52px;height:52px;z-index:30;pointer-events:none;}
#bab-compass svg{width:100%;height:100%;}
#bab-info{position:absolute;left:20px;top:76px;background:rgba(2,5,14,0.9);border:1px solid rgba(212,168,75,0.18);border-radius:10px;padding:14px 16px;z-index:30;min-width:200px;backdrop-filter:blur(16px);box-shadow:0 0 30px rgba(212,168,75,0.06),0 8px 32px rgba(0,0,0,0.6);pointer-events:none;}
.bab-info-title{font-size:8px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:rgba(212,168,75,0.55);margin-bottom:10px;display:flex;align-items:center;gap:6px;}
.bab-live-dot{width:5px;height:5px;border-radius:50%;background:#d4a84b;box-shadow:0 0 6px rgba(212,168,75,0.8);animation:breathe 2s ease-in-out infinite;}
.bab-row{display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.04);}
.bab-row:last-child{border-bottom:none;}
.bab-key{font-size:9px;color:rgba(255,255,255,0.3);}
.bab-val{font-family:'JetBrains Mono',monospace;font-size:10px;color:#e8d5a0;}
.bab-val.g{color:#3ecf8e;}.bab-val.r{color:#e5534b;}.bab-val.s{color:#d4a84b;}.bab-val.p{color:#a78bfa;}
.bab-phase-pill{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:9px;padding:2px 8px;border-radius:4px;margin-bottom:8px;}
#bab-crosshair{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:20px;height:20px;pointer-events:none;z-index:20;opacity:0.4;}
#bab-crosshair::before,#bab-crosshair::after{content:'';position:absolute;background:rgba(255,255,255,0.7);}
#bab-crosshair::before{width:1px;height:100%;left:50%;top:0;}
#bab-crosshair::after{width:100%;height:1px;top:50%;left:0;}
#bab-coords{position:absolute;bottom:80px;left:50%;transform:translateX(-50%);font-family:'JetBrains Mono',monospace;font-size:9px;color:rgba(255,255,255,0.35);background:rgba(0,0,0,0.45);padding:3px 12px;border-radius:4px;pointer-events:none;z-index:20;letter-spacing:0.08em;backdrop-filter:blur(6px);}
#bab-hint{position:absolute;bottom:66px;right:20px;font-family:'JetBrains Mono',monospace;font-size:9px;color:rgba(255,255,255,0.2);line-height:1.8;text-align:right;pointer-events:none;z-index:30;}
#bab-loading{position:absolute;inset:0;z-index:50;background:#050810;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;transition:opacity 0.5s;}
#bab-loading.done{opacity:0;pointer-events:none;}
.bab-spinner{width:40px;height:40px;border:2px solid rgba(212,168,75,0.15);border-top-color:#d4a84b;border-radius:50%;animation:spin 0.8s linear infinite;}
@keyframes spin{to{transform:rotate(360deg);}}
.bab-loading-txt{font-family:'JetBrains Mono',monospace;font-size:11px;color:rgba(212,168,75,0.6);letter-spacing:0.1em;}

::-webkit-scrollbar{width:4px;}::-webkit-scrollbar-track{background:transparent;}::-webkit-scrollbar-thumb{background:var(--border-str);border-radius:2px;}
@keyframes fadeUp{from{opacity:0;transform:translateY(6px);}to{opacity:1;transform:translateY(0);}}
.shell>*{animation:fadeUp .35s ease both;}
.shell>*:nth-child(1){animation-delay:.05s;}.shell>*:nth-child(2){animation-delay:.1s;}
.shell>*:nth-child(3){animation-delay:.15s;}.shell>*:nth-child(4){animation-delay:.2s;}
@media(max-width:1100px){.main-grid{grid-template-columns:1fr;}.kpi-strip{grid-template-columns:repeat(3,1fr);}.trend-grid{grid-template-columns:1fr 1fr;}.summary-grid{grid-template-columns:repeat(2,1fr);gap:10px;}.rl-metrics{grid-template-columns:repeat(2,1fr);}}
@media(max-width:700px){.kpi-strip{grid-template-columns:repeat(2,1fr);}.intersection-wrap{flex-direction:column;}.map-canvas-wrap{width:100%;height:340px;}.trend-grid{grid-template-columns:1fr;}}

/* ── BATTLE PANEL ── */
.battle-panel{background:var(--bg-panel);border:1px solid rgba(212,168,75,0.18);border-radius:14px;padding:20px 22px 24px;margin-top:14px;box-shadow:0 0 40px rgba(212,168,75,0.04),var(--shadow-lg);}
.battle-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:10px;}
.battle-title{font-size:11px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--sand);display:flex;align-items:center;gap:8px;}
.battle-subtitle{font-size:10px;color:var(--text-dim);}
.winner-banner{display:flex;align-items:center;justify-content:center;gap:12px;background:linear-gradient(135deg,rgba(212,168,75,0.12),rgba(212,168,75,0.04));border:1px solid rgba(212,168,75,0.3);border-radius:10px;padding:12px 20px;margin-bottom:16px;animation:fadeUp .4s ease;}
.winner-icon{font-size:22px;}
.winner-text{font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:500;color:var(--sand);letter-spacing:0.06em;}
.battle-grid{display:grid;grid-template-columns:1fr 90px 1fr;gap:14px;align-items:start;}
.battle-side{background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:14px;transition:border-color .3s,box-shadow .3s;}
.battle-side.winning{border-color:rgba(62,207,142,0.4);box-shadow:0 0 20px rgba(62,207,142,0.08);}
.battle-side.losing{border-color:rgba(229,83,75,0.2);opacity:0.85;}
.battle-side-header{display:flex;align-items:center;gap:8px;margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid var(--border);}
.battle-side-label{font-size:11px;font-weight:700;letter-spacing:0.06em;flex:1;}
.fixed-header .battle-side-label{color:var(--text-dim);}
.ai-header .battle-side-label{color:var(--purple);}
.battle-side-tag{font-size:9px;color:var(--text-faint);font-family:'JetBrains Mono',monospace;}
.battle-status-dot{width:7px;height:7px;border-radius:50%;background:var(--text-faint);flex-shrink:0;transition:background .3s,box-shadow .3s;}
.battle-status-dot.active{background:var(--green);box-shadow:0 0 6px rgba(62,207,142,0.7);animation:breathe 1.5s ease-in-out infinite;}
.battle-metrics{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;}
.bm-card{background:var(--bg-raised);border:1px solid var(--border);border-radius:7px;padding:8px 10px;}
.bm-label{font-size:8px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:var(--text-dim);margin-bottom:4px;}
.bm-val{font-family:'JetBrains Mono',monospace;font-size:16px;font-weight:500;color:var(--text);line-height:1;margin-bottom:5px;}
.bm-los{font-size:20px;}
.bm-sub{font-size:9px;color:var(--text-faint);}
.bm-bar-track{height:3px;background:var(--bg-panel);border-radius:2px;overflow:hidden;}
.bm-bar-fill{height:100%;border-radius:2px;transition:width .4s ease;}
.fixed-fill{background:linear-gradient(90deg,var(--text-dim),var(--text-dim));}
.ai-fill{background:linear-gradient(90deg,var(--purple),#7c3aed);}
.battle-chart-wrap{position:relative;}
.battle-chart{width:100%;height:52px;display:block;border-radius:5px;background:var(--bg-raised);}
.battle-chart-lbl{font-size:8px;color:var(--text-faint);margin-top:3px;text-align:center;font-family:'JetBrains Mono',monospace;letter-spacing:0.06em;}
.battle-vs{display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding-top:48px;gap:12px;}
.vs-ring{width:52px;height:52px;border-radius:50%;border:2px solid rgba(212,168,75,0.4);display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;color:var(--sand);background:var(--bg-card);box-shadow:0 0 20px rgba(212,168,75,0.08);}
.vs-delta-wrap{display:flex;flex-direction:column;gap:5px;width:100%;}
.vs-delta-row{display:flex;flex-direction:column;align-items:center;gap:1px;}
.vs-delta-lbl{font-size:7px;color:var(--text-faint);letter-spacing:0.08em;text-transform:uppercase;}
.vs-delta-val{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:500;color:var(--text);}
.vs-delta-val.ai-ahead{color:var(--green);}
.vs-delta-val.fixed-ahead{color:var(--red);}
.vs-step-badge{font-family:'JetBrains Mono',monospace;font-size:8px;padding:3px 8px;border-radius:4px;background:var(--bg-raised);border:1px solid var(--border);color:var(--text-faint);text-align:center;letter-spacing:0.06em;}
@media(max-width:900px){.battle-grid{grid-template-columns:1fr;}.battle-vs{flex-direction:row;padding-top:0;}.vs-delta-wrap{flex-direction:row;justify-content:center;}.vs-ring{width:40px;height:40px;font-size:11px;}}
</style>
</head>
<body>

<!-- BABYLON OVERLAY -->
<div id="babylon-overlay">
  <div id="babylon-canvas-wrap">
    <div id="bab-loading"><div class="bab-spinner"></div><div class="bab-loading-txt">BUILDING 3D ENVIRONMENT…</div></div>
    <canvas id="babylonCanvas"></canvas>
    <div id="bab-hud">
      <div class="bab-metric"><span class="bab-mlbl">Efficiency</span><span class="bab-mval sand" id="bab-eff">—%</span></div>
      <div class="bab-metric"><span class="bab-mlbl">Cleared</span><span class="bab-mval green" id="bab-cleared">0</span></div>
      <div class="bab-metric"><span class="bab-mlbl">Crashes</span><span class="bab-mval red" id="bab-crash">0</span></div>
      <div class="bab-metric"><span class="bab-mlbl">Phase</span><span class="bab-mval" id="bab-phase" style="font-size:13px;letter-spacing:.04em;">NS_GREEN</span></div>
      <div class="bab-metric"><span class="bab-mlbl">Avg Wait</span><span class="bab-mval" id="bab-wait">0.0s</span></div>
      <div class="bab-metric"><span class="bab-mlbl">RL Q-val</span><span class="bab-mval purple" id="bab-qval">—</span></div>
      <div class="bab-metric"><span class="bab-mlbl">ε Explore</span><span class="bab-mval purple" id="bab-eps">1.00</span></div>
    </div>
    <div id="bab-info">
      <div class="bab-info-title"><span class="bab-live-dot"></span>Live Intel · Ground View</div>
      <div id="bab-phase-pill" class="bab-phase-pill ph-NS_GREEN">NS_GREEN</div>
      <div class="bab-row"><span class="bab-key">Throughput</span><span class="bab-val g" id="bab-thru">0 veh</span></div>
      <div class="bab-row"><span class="bab-key">Avg Wait</span><span class="bab-val" id="bab-avgwait">0.0s</span></div>
      <div class="bab-row"><span class="bab-key">NS Queue</span><span class="bab-val g" id="bab-ns2">0 veh</span></div>
      <div class="bab-row"><span class="bab-key">EW Queue</span><span class="bab-val s" id="bab-ew2">0 veh</span></div>
      <div class="bab-row"><span class="bab-key">LOS</span><span class="bab-val" id="bab-los">—</span></div>
      <div class="bab-row"><span class="bab-key">RL Action</span><span class="bab-val p" id="bab-rl-action">—</span></div>
      <div class="bab-row"><span class="bab-key">DQN Loss</span><span class="bab-val p" id="bab-rl-loss">—</span></div>
    </div>
    <div id="bab-compass"><svg viewBox="0 0 52 52" fill="none"><circle cx="26" cy="26" r="24" fill="rgba(2,5,14,0.7)" stroke="rgba(212,168,75,0.3)" stroke-width="1"/><polygon points="26,6 29,24 26,22 23,24" fill="#e5534b"/><polygon points="26,46 29,28 26,30 23,28" fill="rgba(255,255,255,0.4)"/><text x="26" y="18" text-anchor="middle" font-family="monospace" font-size="7" fill="rgba(229,83,75,0.9)">N</text><circle cx="26" cy="26" r="2" fill="rgba(212,168,75,0.6)"/></svg></div>
    <div id="bab-crosshair"></div>
    <div id="bab-coords">LAT 12.9716° N · LON 77.5946° E · ALT 8.4m · GROUND LEVEL</div>
    <div id="bab-hint">Mouse drag · Rotate view<br>Scroll · Zoom in/out<br>WASD · Move camera<br>Right-drag · Pan</div>
    <div id="bab-controls">
      <span class="bab-mlbl" style="color:rgba(255,255,255,0.22);font-size:8px;letter-spacing:.16em;">CAMERA</span>
      <button class="bab-btn active" id="bab-cam-ground" onclick="babSetCam('ground')">🚶 Ground Level</button>
      <button class="bab-btn" id="bab-cam-elevated" onclick="babSetCam('elevated')">🏗 Elevated</button>
      <button class="bab-btn" id="bab-cam-cinematic" onclick="babSetCam('cinematic')">🎬 Cinematic</button>
      <button class="bab-btn" id="bab-cam-overhead" onclick="babSetCam('overhead')">🛸 Overhead</button>
      <div class="bab-sep"></div>
      <span class="bab-mlbl" style="color:rgba(255,255,255,0.22);font-size:8px;letter-spacing:.16em;">PHASE</span>
      <button class="bab-phase-btn" id="bab-force-ns" onclick="babForcePhase('NS_GREEN')">Force N/S Green</button>
      <button class="bab-phase-btn" id="bab-force-ew" onclick="babForcePhase('EW_GREEN')">Force E/W Green</button>
      <div class="bab-sep"></div>
      <button class="bab-phase-btn" id="bab-mode-rl" onclick="setOpMode('rl')">🧠 DQN Policy</button>
      <button class="bab-phase-btn" id="bab-mode-fixed" onclick="setOpMode('fixed')">⏱ Fixed Timer</button>
      <button class="bab-exit" onclick="closeBabylon()">✕ Exit 3D View</button>
    </div>
  </div>
</div>

<!-- MAIN DASHBOARD -->
<div class="shell">
<header class="header">
  <div class="brand">
    <div class="brand-mark">
      <svg viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="7" height="7" rx="1.5" fill="#d4a84b" opacity="0.9"/><rect x="14" y="3" width="7" height="7" rx="1.5" fill="#3ecf8e" opacity="0.5"/><rect x="3" y="14" width="7" height="7" rx="1.5" fill="#3ecf8e" opacity="0.5"/><rect x="14" y="14" width="7" height="7" rx="1.5" fill="#d4a84b" opacity="0.9"/></svg>
    </div>
    <div>
      <div class="brand-name">IntelliFlow</div>
      <div class="brand-sub">Adaptive Traffic Control · DQN Reinforcement Learning · Live Training</div>
    </div>
  </div>
  <div class="header-right">
    <div class="live-pill"><div class="live-dot"></div>Live Environment</div>
<button onclick="toggleFullscreen()" id="btn-fs" style="font-family:'Sora',sans-serif;font-size:10px;font-weight:600;background:var(--bg-raised);border:1px solid var(--border-mid);color:var(--text-dim);border-radius:7px;padding:5px 12px;cursor:pointer;display:flex;align-items:center;gap:5px;transition:all .15s;">
  <svg width="11" height="11" viewBox="0 0 11 11" fill="none"><path d="M1 4V1h3M7 1h3v3M10 7v3H7M4 10H1V7" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <span id="fs-label">Fullscreen</span>
</button>
    <div class="clock"><div class="clock-t" id="clock-t">--:--:--</div><div class="clock-d" id="clock-d">---</div></div>
  </div>
</header>

<div class="ctrl-bar">
  <span class="ctrl-lbl">Scenario</span>
  <select id="task-sel">
    <option value="task_suburban_steady">Easy — Suburban Steady Flow</option>
    <option value="task_urban_stochastic">Medium — Urban Stochastic Rush</option>
    <option value="task_rush_hour_crisis">Hard — Rush Hour Crisis</option>
  </select>
  <div class="ctrl-sep"></div>
  <span class="ctrl-lbl">Seed</span>
  <input type="number" id="seed-in" placeholder="random" style="width:82px">
  <div class="ctrl-sep"></div>
  <button class="btn btn-primary" id="btn-reset">
    <svg width="11" height="11" viewBox="0 0 12 12" fill="none"><path d="M2 6a4 4 0 1 1 1 2.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M2 9V6h3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    New Episode
  </button>
  <button class="btn btn-purple" id="btn-run-rl">
    <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><polygon points="2,1 9,5 2,9" fill="currentColor"/></svg>
    Run DQN Agent
  </button>
  <button class="btn btn-green" id="btn-run">
    <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><polygon points="2,1 9,5 2,9" fill="currentColor"/></svg>
    Run Pressure Policy
  </button>
  <button class="btn btn-ghost" id="btn-stop">
    <svg width="9" height="9" viewBox="0 0 9 9" fill="none"><rect x="1" y="1" width="7" height="7" rx="1.5" fill="currentColor"/></svg>
    Stop
  </button>
  <div class="status-pill" id="status-txt">Standby — press New Episode to begin</div>
</div>

<!-- RL AGENT PANEL -->
<div class="rl-panel" id="rl-panel">
  <div class="rl-header">
    <div class="rl-title"><span class="rl-dot"></span>Deep Q-Network Agent</div>
    <span class="rl-badge" id="rl-status-badge">INITIALISING</span>
  </div>
  <div class="rl-metrics">
    <div class="rl-metric"><div class="rl-metric-lbl">Episodes Trained</div><div class="rl-metric-val" id="rl-episodes">0</div></div>
    <div class="rl-metric"><div class="rl-metric-lbl">Replay Buffer</div><div class="rl-metric-val" id="rl-buffer">0 / 2000</div></div>
    <div class="rl-metric"><div class="rl-metric-lbl">ε Epsilon</div><div class="rl-metric-val" id="rl-epsilon">1.000</div></div>
    <div class="rl-metric"><div class="rl-metric-lbl">Avg Loss</div><div class="rl-metric-val" id="rl-loss-val">—</div></div>
  </div>
  <div class="rl-network">
    <span class="rl-network-lbl">Architecture:</span>
    <span class="rl-network-arch">Input(32) → Dense(128,ReLU) → Dense(128,ReLU) → Dense(64,ReLU) → Q(3)</span>
    <div class="rl-qvals" id="rl-qvals">
      <div class="rl-qval"><span class="rl-qval-lbl">HOLD</span><span class="rl-qval-num other" id="rl-q0">—</span></div>
      <div class="rl-qval"><span class="rl-qval-lbl">SWITCH</span><span class="rl-qval-num other" id="rl-q1">—</span></div>
      <div class="rl-qval"><span class="rl-qval-lbl">EXTEND</span><span class="rl-qval-num other" id="rl-q2">—</span></div>
    </div>
  </div>
  <div class="rl-train-bar-wrap" style="margin-bottom:6px;">
    <span class="rl-train-bar-lbl">Training Progress</span>
    <div class="rl-train-bar-track"><div class="rl-train-bar-fill" id="rl-train-bar" style="width:0%"></div></div>
    <span class="rl-train-bar-val" id="rl-train-pct">0%</span>
  </div>
  <div class="rl-train-bar-wrap">
    <span class="rl-train-bar-lbl">Reward (rolling)</span>
    <div class="rl-train-bar-track"><div class="rl-train-bar-fill" id="rl-reward-bar" style="width:0%;background:linear-gradient(90deg,var(--green),#22c55e)"></div></div>
    <span class="rl-train-bar-val" id="rl-reward-val" style="color:var(--green)">0.0</span>
  </div>
  <canvas id="rl-loss-canvas"></canvas>
</div>

<div class="summary-card">
  <div class="summary-card-title">System Summary</div>
  <div class="summary-grid">
    <div class="summary-item"><div class="summary-item-lbl">Total Vehicles Processed</div><div class="summary-item-val" id="sum-total">—</div><div class="summary-item-sub" id="sum-total-sub">arrived / cleared</div></div>
    <div class="summary-item"><div class="summary-item-lbl">Avg Network Delay</div><div class="summary-item-val" id="sum-delay">—</div><div class="summary-item-sub" id="sum-delay-sub">seconds per vehicle</div></div>
    <div class="summary-item"><div class="summary-item-lbl">Peak Congestion</div><div class="summary-item-val" id="sum-peak">—</div><div class="summary-item-sub" id="sum-peak-sub">max queue observed</div></div>
    <div class="summary-item"><div class="summary-item-lbl">CO₂ Estimate</div><div class="summary-item-val" id="sum-co2">—</div><div class="summary-item-sub">kg (COPERT idle proxy)</div></div>
  </div>
</div>

<div class="kpi-strip">
  <div class="kpi" style="--kpi-c:var(--sand)"><div class="kpi-lbl">Signal Phase</div><div id="phase-tag" class="phase-tag ph-NS_GREEN">NS_GREEN</div><div class="kpi-sub" id="phase-el">Elapsed 0s</div><div class="kpi-accent"></div></div>
  <div class="kpi" style="--kpi-c:var(--blue)"><div class="kpi-lbl">Episode Step</div><div class="kpi-val lg" id="kpi-step">0</div><div class="kpi-sub" id="kpi-hor">of — total</div><div class="kpi-accent"></div></div>
  <div class="kpi" style="--kpi-c:var(--green)"><div class="kpi-lbl">Efficiency Index</div><div class="kpi-val lg" id="kpi-score">—</div><div class="kpi-sub" id="kpi-score-lbl">not evaluated</div><div class="kpi-accent"></div></div>
  <div class="kpi" style="--kpi-c:var(--sand)"><div class="kpi-lbl">Flow Rate (veh/s)</div><div class="kpi-val lg" id="kpi-thru">0</div><div class="kpi-sub">vehicles cleared</div><div class="kpi-accent"></div></div>
  <div class="kpi" style="--kpi-c:var(--red)"><div class="kpi-lbl">Avg Wait Time</div><div class="kpi-val lg" id="kpi-delay">0.0s</div><div class="kpi-sub">per vehicle (HCM)</div><div class="kpi-accent"></div></div>
  <div class="kpi" style="--kpi-c:var(--green)"><div class="kpi-lbl">Level of Service</div><div class="kpi-val lg" id="kpi-los" style="font-size:32px;">—</div><div class="kpi-sub" id="kpi-los-sub">—</div><div class="kpi-accent"></div></div>
</div>

<div class="main-grid">
  <div class="left-col">
    <div class="panel">
      <div class="panel-hd">
        <div class="panel-title">Live Intersection</div>
        <div style="display:flex;gap:8px;align-items:center;">
          <span class="panel-tag" id="map-tag">PHASE: —</span>
          <button class="btn btn-ghost" id="btn-fullscreen" style="padding:4px 10px;font-size:10px;background:linear-gradient(135deg,rgba(212,168,75,0.15),rgba(212,168,75,0.05));border-color:rgba(212,168,75,0.3);color:#d4a84b;" onclick="openBabylon()">
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M1 4V1h3M6 1h3v3M9 6v3H6M4 9H1V6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>
            Enter 3D Ground View
          </button>
        </div>
      </div>
      <div class="intersection-wrap">
        <div class="map-canvas-wrap" id="map-canvas-wrap">
          <canvas id="sat-canvas" width="860" height="860"></canvas>
          <canvas id="road-canvas" width="860" height="860"></canvas>
          <canvas id="car-canvas"  width="860" height="860"></canvas>
          <canvas id="booth-hint-canvas" width="860" height="860"></canvas>
          <div class="corner-score left" id="cs-tl"><span class="cs-label">Flow Rate</span><span class="cs-val green" id="cs-tl-val">+0</span><span class="cs-delta green" id="cs-tl-delta">&nbsp;</span><div class="cs-bar-track"><div class="cs-bar-fill green" id="cs-tl-bar" style="width:0%"></div></div></div>
          <div class="corner-score right" id="cs-tr"><span class="cs-label">Crashes</span><span class="cs-val red" id="cs-tr-val">-0</span><span class="cs-delta red" id="cs-tr-delta">&nbsp;</span><div class="cs-bar-track"><div class="cs-bar-fill red" id="cs-tr-bar" style="width:0%"></div></div></div>
          <div class="vol-bar left" id="vol-left"></div>
          <div class="vol-bar right" id="vol-right"></div>
          <div class="map-coord">LAT 12.9716° N · LON 77.5946° E · ZOOM 18</div>
          <div class="booth-tooltip" id="booth-tooltip" style="bottom:52%;left:50%;">🏙 Enter 3D Ground View</div>
        </div>
        <div class="map-aside">
          <div class="sig-panel">
            <div class="sig-lbl">Signal State</div>
            <div id="sig-phase-tag" class="phase-tag ph-NS_GREEN" style="font-size:11px;margin-bottom:10px;">NS_GREEN</div>
            <div class="sig-row">
              <div class="sig-cell"><div class="lamp red" id="lamp-N"></div><div class="sig-dir">N</div></div>
              <div class="sig-cell"><div class="lamp red" id="lamp-S"></div><div class="sig-dir">S</div></div>
              <div class="sig-cell"><div class="lamp red" id="lamp-E"></div><div class="sig-dir">E</div></div>
              <div class="sig-cell"><div class="lamp red" id="lamp-W"></div><div class="sig-dir">W</div></div>
            </div>
          </div>
          <div class="prog-block">
            <div class="prog-row"><span class="prog-lbl">Episode Progress</span><span class="prog-nums"><span id="prog-step">0</span> / <span id="prog-hor">—</span></span></div>
            <div class="prog-track"><div class="prog-fill" id="prog-fill" style="width:0%"></div></div>
          </div>
          <div class="score-block">
            <div class="ring-wrap">
              <svg viewBox="0 0 90 90"><circle cx="45" cy="45" r="34" fill="none" stroke="#242938" stroke-width="8"/><circle id="score-ring" cx="45" cy="45" r="34" fill="none" stroke="#d4a84b" stroke-width="8" stroke-linecap="round" stroke-dasharray="0 213.6" stroke-dashoffset="53.4" style="transition:stroke-dasharray .6s cubic-bezier(.4,0,.2,1),stroke .4s;"/></svg>
              <div class="ring-center"><div class="ring-val" id="ring-val">—</div><div class="ring-lbl-sm">eff. idx</div></div>
            </div>
            <div class="score-info"><div class="score-stars" id="score-stars">☆☆☆</div><div class="score-note" id="score-note">Run a policy to evaluate performance.</div></div>
          </div>
          <div class="decision-panel">
            <div class="decision-phase">
              <div class="sig-lbl" style="margin-bottom:0;">Current Decision</div>
              <div id="dec-phase-tag" class="phase-tag ph-NS_GREEN" style="font-size:10px;margin-bottom:0;padding:2px 7px;">NS_GREEN</div>
            </div>
            <div class="decision-reason-list" id="dec-reason-list">
              <div class="decision-reason"><div class="decision-reason-dot sand"></div><span style="color:var(--text-faint);">Awaiting episode data…</span></div>
            </div>
            <div class="decision-predicted"><span class="decision-predicted-lbl">Predicted throughput gain</span><span class="decision-predicted-val" id="dec-gain">—</span></div>
          </div>
          <div class="panel" style="padding:12px;background:var(--bg-card);">
            <div class="metric-list">
              <div class="mrow"><div class="mkey">NS Queue Length</div><div class="mval g" id="m-ns">0 veh</div></div>
              <div class="mrow"><div class="mkey">EW Queue Length</div><div class="mval a" id="m-ew">0 veh</div></div>
              <div class="mrow"><div class="mkey">Efficiency Index</div><div class="mval" id="m-viz-score" style="color:#d4a84b;">0%</div></div>
              <div class="mrow"><div class="mkey">Crashes</div><div class="mval r" id="m-crashes">0</div></div>
              <div class="mrow"><div class="mkey">Vehicles Cleared</div><div class="mval g" id="m-smooth">0</div></div>
              <div class="mrow"><div class="mkey">CO₂ est.</div><div class="mval" id="m-co2">0 kg</div></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="panel">
      <div class="panel-hd"><div class="panel-title">Approach Queue Occupancy &amp; Saturation</div><span class="panel-tag" id="spill-tag">SPILLBACK: 0 lanes</span></div>
      <div class="dir-grid" id="dir-grid"></div>
    </div>
    <div class="trend-panel">
      <div class="panel-hd"><div class="panel-title">Trend Over Time</div><span class="panel-tag">Last 200 steps</span></div>
      <div class="trend-grid">
        <div class="trend-chart-wrap"><div class="trend-chart-hd"><span class="trend-chart-lbl">Avg Wait Time (s)</span><span class="trend-chart-val" id="trend-delay-val">—</span></div><canvas class="trend-canvas" id="trend-delay-canvas"></canvas></div>
        <div class="trend-chart-wrap"><div class="trend-chart-hd"><span class="trend-chart-lbl">Throughput (veh/step)</span><span class="trend-chart-val" id="trend-thru-val">—</span></div><canvas class="trend-canvas" id="trend-thru-canvas"></canvas></div>
        <div class="trend-chart-wrap"><div class="trend-chart-hd"><span class="trend-chart-lbl">Queue Buildup (veh)</span><span class="trend-chart-val" id="trend-queue-val">—</span></div><canvas class="trend-canvas" id="trend-queue-canvas"></canvas></div>
      </div>
    </div>
  </div>
  <div class="right-col">
    <div class="panel">
      <div class="panel-hd"><div class="panel-title">Level of Service — HCM 2010</div><span class="panel-tag" id="los-tag">LOS —</span></div>
      <div class="los-panel">
        <div class="los-cell" id="los-A" style="--los-c:#3ecf8e;--los-bg:rgba(62,207,142,0.08);--los-glow:rgba(62,207,142,0.5)"><div class="los-letter">A</div><div class="los-delay">≤10s</div><div class="los-bar"></div></div>
        <div class="los-cell" id="los-B" style="--los-c:#5ec4a0;--los-bg:rgba(94,196,160,0.08);--los-glow:rgba(94,196,160,0.4)"><div class="los-letter">B</div><div class="los-delay">≤20s</div><div class="los-bar"></div></div>
        <div class="los-cell" id="los-C" style="--los-c:#b8c44a;--los-bg:rgba(184,196,74,0.08);--los-glow:rgba(184,196,74,0.4)"><div class="los-letter">C</div><div class="los-delay">≤35s</div><div class="los-bar"></div></div>
        <div class="los-cell" id="los-D" style="--los-c:#d4a84b;--los-bg:rgba(212,168,75,0.08);--los-glow:rgba(212,168,75,0.4)"><div class="los-letter">D</div><div class="los-delay">≤55s</div><div class="los-bar"></div></div>
        <div class="los-cell" id="los-E" style="--los-c:#e08840;--los-bg:rgba(224,136,64,0.08);--los-glow:rgba(224,136,64,0.4)"><div class="los-letter">E</div><div class="los-delay">≤80s</div><div class="los-bar"></div></div>
        <div class="los-cell" id="los-F" style="--los-c:#e5534b;--los-bg:rgba(229,83,75,0.08);--los-glow:rgba(229,83,75,0.4)"><div class="los-letter">F</div><div class="los-delay">&gt;80s</div><div class="los-bar"></div></div>
      </div>
      <div style="margin-top:14px;">
        <div class="panel-hd" style="margin-bottom:8px;"><div class="panel-title">Clearance per Step</div><span class="panel-tag" id="spark-latest">— veh</span></div>
        <div class="sparkline-wrap"><canvas class="sparkline" id="spark-canvas"></canvas></div>
        <div style="display:flex;gap:14px;margin-top:6px;">
          <div style="display:flex;align-items:center;gap:5px;font-size:10px;color:var(--text-dim);"><div style="width:14px;height:2px;background:#3ecf8e;border-radius:1px;"></div>NS</div>
          <div style="display:flex;align-items:center;gap:5px;font-size:10px;color:var(--text-dim);"><div style="width:14px;height:2px;background:#d4a84b;border-radius:1px;"></div>EW</div>
        </div>
      </div>
    </div>
    <div class="panel"><div class="panel-hd"><div class="panel-title">Lane Occupancy</div><span class="panel-tag">12 LANES</span></div><div class="lane-grid" id="lane-grid"></div></div>
    <div class="panel">
      <div class="panel-hd"><div class="panel-title">Episode Metrics</div></div>
      <div class="metric-list">
        <div class="mrow"><div class="mkey">Efficiency Ratio</div><div class="mval g" id="dm-eff">—</div></div>
        <div class="mrow"><div class="mkey">Rolling Throughput</div><div class="mval" id="dm-rtp">—</div></div>
        <div class="mrow"><div class="mkey">Peak Wait Time</div><div class="mval r" id="dm-pdly">—</div></div>
        <div class="mrow"><div class="mkey">Peak Queue Length</div><div class="mval a" id="dm-pq">—</div></div>
        <div class="mrow"><div class="mkey">DQN Avg Q-Value</div><div class="mval p" id="dm-qval">—</div></div>
        <div class="mrow"><div class="mkey">Step Cleared</div><div class="mval g" id="dm-sc">—</div></div>
      </div>
    </div>
    <div class="panel" style="flex:1;"><div class="panel-hd"><div class="panel-title">Event Log</div><span class="panel-tag" id="log-count">0 entries</span></div><div class="log-box" id="log-box"></div></div>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     BATTLE PANEL — Fixed Timer vs DQN AI
════════════════════════════════════════════════════════════════ -->
<div class="battle-panel" id="battle-panel">
  <div class="battle-header">
    <div class="battle-title">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1l1.5 3.5L12 5l-2.5 2.5.5 3.5L7 9.5 4 11l.5-3.5L2 5l3.5-.5z" fill="#d4a84b" opacity="0.9"/></svg>
      BATTLE MODE — Fixed Timer vs Your DQN AI
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
      <span class="battle-subtitle">Both running same episode · same seed · same scenario</span>
      <button class="btn btn-primary" id="btn-battle-start" style="font-size:10px;padding:5px 14px;">
        <svg width="9" height="9" viewBox="0 0 10 10" fill="none"><polygon points="2,1 9,5 2,9" fill="currentColor"/></svg>
        Start Battle
      </button>
      <button class="btn btn-ghost" id="btn-battle-stop" style="font-size:10px;padding:5px 12px;display:none;">Stop</button>
    </div>
  </div>

  <!-- Winner banner -->
  <div class="winner-banner" id="winner-banner" style="display:none;">
    <span class="winner-icon" id="winner-icon">🏆</span>
    <span class="winner-text" id="winner-text">—</span>
  </div>

  <!-- Two columns -->
  <div class="battle-grid">

    <!-- LEFT: Fixed Timer -->
    <div class="battle-side" id="battle-left">
      <div class="battle-side-header fixed-header">
        <div class="battle-side-label">⏱ Fixed Timer</div>
        <div class="battle-side-tag">30s cycle · no intelligence</div>
        <div class="battle-status-dot" id="fixed-dot"></div>
      </div>
      <div class="battle-metrics">
        <div class="bm-card">
          <div class="bm-label">Efficiency</div>
          <div class="bm-val" id="fixed-eff">—</div>
          <div class="bm-bar-track"><div class="bm-bar-fill fixed-fill" id="fixed-eff-bar" style="width:0%"></div></div>
        </div>
        <div class="bm-card">
          <div class="bm-label">Avg Wait</div>
          <div class="bm-val" id="fixed-wait">—</div>
          <div class="bm-bar-track"><div class="bm-bar-fill fixed-fill" id="fixed-wait-bar" style="width:0%"></div></div>
        </div>
        <div class="bm-card">
          <div class="bm-label">Vehicles Cleared</div>
          <div class="bm-val" id="fixed-cleared">—</div>
          <div class="bm-bar-track"><div class="bm-bar-fill fixed-fill" id="fixed-cleared-bar" style="width:0%"></div></div>
        </div>
        <div class="bm-card">
          <div class="bm-label">LOS</div>
          <div class="bm-val bm-los" id="fixed-los">—</div>
          <div class="bm-sub" id="fixed-step">Step 0</div>
        </div>
      </div>
      <!-- Mini queue chart -->
      <div class="battle-chart-wrap">
        <canvas id="fixed-chart" class="battle-chart"></canvas>
        <div class="battle-chart-lbl">Queue over time</div>
      </div>
    </div>

    <!-- MIDDLE: VS divider -->
    <div class="battle-vs">
      <div class="vs-ring">VS</div>
      <div class="vs-delta-wrap">
        <div class="vs-delta-row"><span class="vs-delta-lbl">Eff. gap</span><span class="vs-delta-val" id="vs-eff-delta">—</span></div>
        <div class="vs-delta-row"><span class="vs-delta-lbl">Wait gap</span><span class="vs-delta-val" id="vs-wait-delta">—</span></div>
        <div class="vs-delta-row"><span class="vs-delta-lbl">Cleared gap</span><span class="vs-delta-val" id="vs-cleared-delta">—</span></div>
      </div>
      <div class="vs-step-badge" id="vs-step-badge">STANDBY</div>
    </div>

    <!-- RIGHT: DQN AI -->
    <div class="battle-side" id="battle-right">
      <div class="battle-side-header ai-header">
        <div class="battle-side-label">🧠 DQN AI</div>
        <div class="battle-side-tag">Your trained model · ε=0 exploit</div>
        <div class="battle-status-dot" id="ai-dot"></div>
      </div>
      <div class="battle-metrics">
        <div class="bm-card">
          <div class="bm-label">Efficiency</div>
          <div class="bm-val" id="ai-eff">—</div>
          <div class="bm-bar-track"><div class="bm-bar-fill ai-fill" id="ai-eff-bar" style="width:0%"></div></div>
        </div>
        <div class="bm-card">
          <div class="bm-label">Avg Wait</div>
          <div class="bm-val" id="ai-wait">—</div>
          <div class="bm-bar-track"><div class="bm-bar-fill ai-fill" id="ai-wait-bar" style="width:0%"></div></div>
        </div>
        <div class="bm-card">
          <div class="bm-label">Vehicles Cleared</div>
          <div class="bm-val" id="ai-cleared">—</div>
          <div class="bm-bar-track"><div class="bm-bar-fill ai-fill" id="ai-cleared-bar" style="width:0%"></div></div>
        </div>
        <div class="bm-card">
          <div class="bm-label">LOS</div>
          <div class="bm-val bm-los" id="ai-los">—</div>
          <div class="bm-sub" id="ai-step">Step 0</div>
        </div>
      </div>
      <!-- Mini queue chart -->
      <div class="battle-chart-wrap">
        <canvas id="ai-chart" class="battle-chart"></canvas>
        <div class="battle-chart-lbl">Queue over time</div>
      </div>
    </div>

  </div><!-- /battle-grid -->
</div><!-- /battle-panel -->

</div><!-- /shell -->

<script>
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

</script>
</body>
</html>"""

DASHBOARD_HTML = __doc__

def render_dashboard():
    return DASHBOARD_HTML