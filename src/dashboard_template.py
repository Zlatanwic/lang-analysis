"""HTML template for the interactive dashboard."""

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Programming Language Type System Knowledge Graph</title>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<style>
  :root {
    --bg: #0f1117;
    --card: #1a1d27;
    --border: #2a2d3a;
    --text: #e1e4ed;
    --text-dim: #8b8fa3;
    --accent: #6c8cff;
    --accent2: #ff6c8c;
    --accent3: #6cffa0;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
  }
  .header {
    text-align: center;
    padding: 40px 20px 20px;
    border-bottom: 1px solid var(--border);
  }
  .header h1 { font-size: 2rem; font-weight: 700; margin-bottom: 8px; }
  .header p { color: var(--text-dim); font-size: 0.95rem; max-width: 700px; margin: 0 auto; }
  .tabs {
    display: flex;
    justify-content: center;
    gap: 4px;
    padding: 20px;
    flex-wrap: wrap;
  }
  .tab {
    padding: 10px 24px;
    border: 1px solid var(--border);
    border-radius: 8px;
    cursor: pointer;
    background: var(--card);
    color: var(--text-dim);
    font-size: 0.9rem;
    transition: all 0.2s;
  }
  .tab:hover { border-color: var(--accent); color: var(--text); }
  .tab.active { background: var(--accent); color: #fff; border-color: var(--accent); }
  .panel { display: none; padding: 20px; max-width: 1400px; margin: 0 auto; }
  .panel.active { display: block; }
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
  }
  .card h2 { font-size: 1.2rem; margin-bottom: 12px; }
  .card p.desc { color: var(--text-dim); font-size: 0.85rem; margin-bottom: 16px; }

  /* Heatmap */
  #heatmap-container {
    border: 1px solid var(--border);
    border-radius: 16px;
    background:
      linear-gradient(180deg, rgba(108,140,255,0.08), rgba(108,140,255,0.01)),
      var(--card);
    overflow: hidden;
  }
  .matrix-shell { padding: 18px; }
  .matrix-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 16px;
  }
  .matrix-toolbar-copy {
    color: var(--text-dim);
    font-size: 0.82rem;
    max-width: 720px;
  }
  .matrix-toolbar-copy strong { color: var(--text); }
  .matrix-summary {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  .summary-pill {
    min-width: 112px;
    padding: 10px 12px;
    border: 1px solid rgba(108,140,255,0.14);
    border-radius: 12px;
    background: rgba(15,17,23,0.42);
  }
  .summary-pill strong {
    display: block;
    color: var(--text);
    font-size: 0.95rem;
    line-height: 1.2;
  }
  .summary-pill span {
    color: var(--text-dim);
    font-size: 0.72rem;
    letter-spacing: 0.03em;
    text-transform: uppercase;
  }
  .heatmap-scroll {
    overflow: auto;
    padding-bottom: 10px;
    scrollbar-color: rgba(108,140,255,0.45) rgba(255,255,255,0.04);
  }
  .heatmap-table {
    width: max-content;
    min-width: 100%;
    border-collapse: separate;
    border-spacing: 6px;
    table-layout: fixed;
  }
  .heatmap-table th, .heatmap-table td {
    padding: 0;
    text-align: center;
    font-size: 0.7rem;
    border: none;
    vertical-align: middle;
  }
  .heatmap-table thead th {
    position: sticky;
    top: 0;
    z-index: 3;
    color: var(--text-dim);
    font-weight: 600;
    font-size: 0.65rem;
    cursor: default;
  }
  .heatmap-table thead th:hover { color: var(--accent); }
  .heatmap-table th.lang-name,
  .heatmap-table td.lang-name {
    position: sticky;
    left: 0;
    z-index: 4;
  }
  .heatmap-table th.lang-name {
    min-width: 196px;
    padding-left: 0;
    text-align: left;
    font-size: 0.74rem;
  }
  .heatmap-table th.score-col,
  .heatmap-table td.score-col {
    position: sticky;
    right: 0;
    z-index: 4;
  }
  .heatmap-table th.score-col {
    min-width: 92px;
    font-size: 0.68rem;
  }
  .corner-card,
  .score-head-card,
  .feature-head-card,
  .lang-cell-card,
  .score-cell-card {
    border: 1px solid rgba(108,140,255,0.12);
    border-radius: 12px;
    background: rgba(15,17,23,0.76);
    backdrop-filter: blur(8px);
  }
  .corner-card,
  .score-head-card {
    min-height: 72px;
    padding: 10px 12px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .corner-card strong,
  .score-head-card strong {
    color: var(--text);
    font-size: 0.78rem;
    line-height: 1.2;
  }
  .corner-card span,
  .score-head-card span {
    color: var(--text-dim);
    font-size: 0.65rem;
    margin-top: 4px;
  }
  .feature-col {
    width: 64px;
    min-width: 64px;
  }
  .feature-head-card {
    min-height: 72px;
    padding: 8px 6px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 5px;
    transition: border-color 0.18s ease, transform 0.18s ease, background 0.18s ease;
  }
  .feature-head-card:hover {
    border-color: rgba(108,140,255,0.36);
    transform: translateY(-1px);
  }
  .feature-head-index {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 20px;
    border-radius: 999px;
    background: rgba(108,140,255,0.16);
    color: var(--accent);
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.04em;
  }
  .feature-head-short {
    color: var(--text);
    font-size: 0.62rem;
    line-height: 1.15;
    text-align: center;
    text-wrap: balance;
  }
  .heatmap-table td.lang-name {
    text-align: left;
    font-weight: 600;
    font-size: 0.75rem;
    white-space: nowrap;
  }
  .lang-cell-card {
    min-height: 46px;
    padding: 10px 12px;
  }
  .lang-title {
    color: var(--text);
    font-size: 0.75rem;
    font-weight: 650;
  }
  .lang-meta {
    display: block;
    margin-top: 2px;
    color: var(--text-dim);
    font-size: 0.62rem;
  }
  .heatmap-cell {
    width: 100%;
    min-width: 42px;
    height: 34px;
    display: grid;
    place-items: center;
    border-radius: 10px;
    transition: transform 0.16s ease, box-shadow 0.16s ease, color 0.16s ease;
    cursor: pointer;
    text-align: center;
    font-size: 0.72rem;
    color: rgba(255,255,255,0.5);
    font-weight: 700;
  }
  .heatmap-cell:hover {
    transform: translateY(-1px) scale(1.04);
    color: #fff;
    box-shadow: 0 8px 18px rgba(108,140,255,0.28);
  }
  .heatmap-score-td { padding: 2px 6px !important; }
  .score-cell-card {
    min-height: 46px;
    padding: 8px 10px;
    display: flex;
    justify-content: center;
  }
  .heatmap-score-bar {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text);
  }
  /* Feature index legend */
  .feat-index-legend {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 10px;
    margin-top: 18px;
    padding-top: 16px;
    border-top: 1px solid rgba(255,255,255,0.06);
  }
  .feat-legend-item {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    padding: 10px 12px;
    border: 1px solid rgba(108,140,255,0.12);
    border-radius: 12px;
    background: rgba(15,17,23,0.38);
  }
  .feat-legend-copy {
    min-width: 0;
  }
  .feat-legend-copy strong {
    display: block;
    color: var(--text);
    font-size: 0.75rem;
    line-height: 1.25;
    margin-bottom: 2px;
  }
  .feat-legend-copy small {
    display: block;
    color: var(--text-dim);
    font-size: 0.66rem;
    line-height: 1.35;
    white-space: normal;
  }
  .feat-index-legend .feat-idx {
    flex: 0 0 auto;
    display: inline-flex;
    width: 28px;
    height: 28px;
    align-items: center;
    justify-content: center;
    text-align: center;
    border-radius: 8px;
    font-size: 0.65rem;
    font-weight: 800;
    background: rgba(108,140,255,0.15);
    color: var(--accent);
  }
  /* Column highlight on hover */
  .heatmap-table td.col-hover .heatmap-cell {
    box-shadow: inset 0 0 0 1px rgba(108,140,255,0.35);
    transform: translateY(-1px);
  }
  .heatmap-table th.col-hover .feature-head-card {
    border-color: rgba(108,140,255,0.42);
    background: rgba(108,140,255,0.12);
  }
  .heatmap-table tbody tr:hover .lang-cell-card,
  .heatmap-table tbody tr:hover .score-cell-card {
    border-color: rgba(108,140,255,0.28);
  }

  /* Scoring legend */
  .score-legend {
    display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px;
    font-size: 0.8rem; color: var(--text-dim);
  }
  .score-legend-item {
    display: flex; align-items: center; gap: 4px;
  }
  .score-legend-swatch {
    width: 16px; height: 16px; border-radius: 3px; display: inline-block;
  }

  /* Radar selectors */
  .radar-controls { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; }
  .lang-chip {
    padding: 6px 14px;
    border: 1px solid var(--border);
    border-radius: 20px;
    cursor: pointer;
    font-size: 0.8rem;
    transition: all 0.2s;
    user-select: none;
  }
  .lang-chip:hover { border-color: var(--accent); }
  .lang-chip.selected { background: var(--accent); color: #fff; border-color: var(--accent); }

  /* Network */
  #network-svg { width: 100%; background: var(--card); border-radius: 12px; }
  .node-label { font-size: 11px; fill: var(--text); pointer-events: none; font-weight: 600; }
  .link { stroke-opacity: 0.4; }

  /* Timeline */
  #timeline-chart { width: 100%; height: 700px; }

  /* Popularity */
  #popularity-chart { width: 100%; height: 600px; }
  .pop-metric-btns { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
  .pop-metric-btn {
    padding: 6px 16px; border: 1px solid var(--border); border-radius: 8px;
    cursor: pointer; font-size: 0.8rem; background: var(--card); color: var(--text-dim);
    transition: all 0.2s;
  }
  .pop-metric-btn:hover { border-color: var(--accent); color: var(--text); }
  .pop-metric-btn.active { background: var(--accent); color: #fff; border-color: var(--accent); }

  /* Additional visualization panels */
  #diffusion-chart,
  #cluster-chart,
  #lineage-chart {
    width: 100%;
    height: 640px;
  }
  .viz-toolbar {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 18px;
  }
  .control-label {
    color: var(--text-dim);
    font-size: 0.78rem;
    font-weight: 600;
  }
  .control-select,
  .control-button {
    border: 1px solid var(--border);
    border-radius: 10px;
    background: rgba(15,17,23,0.8);
    color: var(--text);
    min-height: 40px;
    padding: 0 14px;
    font-size: 0.82rem;
    transition: border-color 0.18s ease, transform 0.18s ease;
  }
  .control-button {
    cursor: pointer;
  }
  .control-select:focus,
  .control-button:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 2px rgba(108,140,255,0.18);
  }
  .control-button:hover { border-color: var(--accent); transform: translateY(-1px); }
  .control-range {
    accent-color: var(--accent);
    min-width: 180px;
  }
  .control-note {
    color: var(--text-dim);
    font-size: 0.76rem;
    max-width: 560px;
  }
  .mini-dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 10px;
    margin-bottom: 16px;
  }
  .mini-dashboard-card {
    border: 1px solid rgba(108,140,255,0.14);
    border-radius: 14px;
    background: rgba(15,17,23,0.52);
    padding: 12px 14px;
  }
  .mini-dashboard-card strong {
    display: block;
    color: var(--text);
    font-size: 0.92rem;
    margin-bottom: 4px;
  }
  .mini-dashboard-card span {
    color: var(--text-dim);
    font-size: 0.72rem;
    line-height: 1.4;
  }
  .legend-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 14px;
  }
  .legend-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    min-height: 30px;
    padding: 0 10px;
    border-radius: 999px;
    background: rgba(255,255,255,0.05);
    color: var(--text);
    font-size: 0.72rem;
  }
  .legend-swatch {
    width: 12px;
    height: 12px;
    border-radius: 999px;
    display: inline-block;
    flex: 0 0 auto;
  }
  .recommendation-hero {
    grid-column: 1 / -1;
    border: 1px solid rgba(108,140,255,0.18);
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(108,140,255,0.18), rgba(15,17,23,0.72));
    padding: 14px 16px;
  }
  .recommendation-hero strong {
    display: block;
    font-size: 1rem;
    margin-bottom: 4px;
  }
  .recommendation-hero span {
    color: var(--text-dim);
    font-size: 0.76rem;
    line-height: 1.45;
  }
  .feature-filter-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 10px;
    margin-bottom: 18px;
  }
  .feature-toggle {
    border: 1px solid rgba(108,140,255,0.14);
    border-radius: 12px;
    background: rgba(15,17,23,0.52);
    color: var(--text);
    padding: 12px 12px 10px;
    cursor: pointer;
    text-align: left;
    transition: border-color 0.18s ease, background 0.18s ease, transform 0.18s ease;
  }
  .feature-toggle:hover {
    border-color: rgba(108,140,255,0.4);
    transform: translateY(-1px);
  }
  .feature-toggle.active {
    background: rgba(108,140,255,0.16);
    border-color: rgba(108,140,255,0.48);
  }
  .feature-toggle strong {
    display: block;
    font-size: 0.78rem;
    color: var(--text);
    margin-bottom: 3px;
  }
  .feature-toggle small {
    display: block;
    color: var(--text-dim);
    font-size: 0.68rem;
    line-height: 1.35;
  }
  .recommendation-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 14px;
  }
  .recommendation-card {
    border: 1px solid rgba(108,140,255,0.14);
    border-radius: 16px;
    background: linear-gradient(180deg, rgba(108,140,255,0.1), rgba(15,17,23,0.76));
    padding: 16px;
  }
  .recommendation-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 10px;
  }
  .recommendation-head h3 {
    font-size: 1rem;
    line-height: 1.2;
  }
  .recommendation-score {
    min-width: 56px;
    padding: 6px 8px;
    border-radius: 10px;
    background: rgba(108,140,255,0.18);
    text-align: center;
    font-size: 0.8rem;
    font-weight: 700;
  }
  .recommendation-meta,
  .recommendation-empty {
    color: var(--text-dim);
    font-size: 0.74rem;
    line-height: 1.45;
  }
  .recommendation-section {
    margin-top: 10px;
  }
  .recommendation-section strong {
    display: block;
    margin-bottom: 5px;
    font-size: 0.76rem;
  }
  .pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }
  .mini-pill {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    min-height: 24px;
    padding: 0 8px;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    color: var(--text);
    font-size: 0.68rem;
  }
  .mini-pill.missing {
    background: rgba(255,108,140,0.14);
    color: #ffb6c5;
  }
  .mini-pill.match {
    background: rgba(108,255,160,0.14);
    color: #b7ffd0;
  }

  /* Tooltip */
  .tooltip {
    position: fixed;
    background: #222538;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 0.8rem;
    pointer-events: none;
    z-index: 999;
    max-width: 350px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    display: none;
  }
  .complexity-bar {
    display: inline-block;
    height: 8px;
    border-radius: 4px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    vertical-align: middle;
    margin-left: 6px;
  }
  @media (max-width: 768px) {
    .header h1 { font-size: 1.4rem; }
    .tabs { gap: 6px; }
    .tab { padding: 8px 16px; font-size: 0.8rem; }
    .matrix-shell { padding: 14px; }
    .matrix-toolbar { align-items: stretch; }
    .summary-pill { min-width: 96px; flex: 1 1 96px; }
    .heatmap-table { border-spacing: 4px; }
    .heatmap-table th.lang-name { min-width: 148px; }
    .heatmap-table th.score-col { min-width: 76px; }
    .feature-col { width: 52px; min-width: 52px; }
    .feature-head-card { min-height: 68px; padding: 8px 4px; }
    .feature-head-short { font-size: 0.58rem; }
    .heatmap-cell { min-width: 36px; height: 30px; font-size: 0.68rem; }
    .lang-cell-card { padding: 8px 10px; }
    .lang-title { font-size: 0.7rem; }
    .lang-meta { font-size: 0.58rem; }
    .feat-index-legend { grid-template-columns: 1fr; }
    #diffusion-chart,
    #cluster-chart,
    #lineage-chart,
    #timeline-chart,
    #popularity-chart { height: 520px; }
    .control-note { max-width: 100%; }
    .control-range { min-width: 120px; width: 100%; }
    .mini-dashboard-grid { grid-template-columns: 1fr; }
    .feature-filter-grid,
    .recommendation-grid { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>

<div class="header">
  <h1>Programming Language Type System Knowledge Graph</h1>
  <p>An interactive exploration of type system features across <strong>26</strong> programming languages — featuring 0-5 fine-grained scoring, diffusion paths, clustering, lineage analysis, and guided language recommendations.</p>
</div>

<div class="tabs">
  <div class="tab active" data-panel="heatmap">Feature Matrix</div>
  <div class="tab" data-panel="radar">Radar Comparison</div>
  <div class="tab" data-panel="timeline">Feature Timeline</div>
  <div class="tab" data-panel="diffusion">Feature Diffusion</div>
  <div class="tab" data-panel="clusters">Domain Clusters</div>
  <div class="tab" data-panel="lineage">Lineage Graph</div>
  <div class="tab" data-panel="recommender">Feature Recommender</div>
  <div class="tab" data-panel="network">Similarity Network</div>
  <div class="tab" data-panel="popularity">Popularity Analysis</div>
</div>

<div class="tooltip" id="tooltip"></div>

<!-- Panel 1: Heatmap -->
<div class="panel active" id="panel-heatmap">
  <div class="card">
    <h2>Type System Feature Matrix</h2>
    <p class="desc">Rows sorted by total type system complexity score. Scoring: 0 (not supported) to 5 (full/reference implementation). Hover cells to inspect the full rationale without expanding the grid.</p>
    <div class="score-legend" id="score-legend"></div>
    <div id="heatmap-container"></div>
  </div>
</div>

<!-- Panel 2: Radar -->
<div class="panel" id="panel-radar">
  <div class="card">
    <h2>Radar Chart Comparison</h2>
    <p class="desc">Select 2-4 languages to overlay their type system "shapes" on a radar chart. Scale: 0-5.</p>
    <div class="radar-controls" id="radar-chips"></div>
    <div id="radar-chart" style="width:100%;height:550px;"></div>
  </div>
</div>

<!-- Panel 3: Timeline -->
<div class="panel" id="panel-timeline">
  <div class="card">
    <h2>Type Feature Evolution Timeline</h2>
    <p class="desc">When did each language adopt key type system features? Observe the "type system arms race" across decades.</p>
    <div id="timeline-chart"></div>
  </div>
</div>

<!-- Panel 4: Network -->
<div class="panel" id="panel-network">
  <div class="card">
    <h2>Language Similarity Network</h2>
    <p class="desc">Languages connected by cosine similarity of their feature vectors (threshold &ge; 0.65). Node size reflects type system complexity. Drag nodes to explore clusters.</p>
    <svg id="network-svg" height="600"></svg>
  </div>
</div>

<!-- Panel 5: Popularity -->
<div class="panel" id="panel-popularity">
  <div class="card">
    <h2>Type Complexity vs. Popularity</h2>
    <p class="desc">Does a richer type system correlate with popularity? Explore the trade-off between type system complexity (sum of feature scores) and language popularity metrics. Bubble size = StackOverflow "loved" percentage.</p>
    <div class="pop-metric-btns" id="pop-metric-btns">
      <div class="pop-metric-btn active" data-metric="tiobe_rank">TIOBE Rank</div>
      <div class="pop-metric-btn" data-metric="github_stars_rank">GitHub Stars Rank</div>
      <div class="pop-metric-btn" data-metric="stackoverflow_loved_pct">SO Loved %</div>
    </div>
    <div id="popularity-chart"></div>
  </div>
</div>

<!-- Panel 6: Diffusion -->
<div class="panel" id="panel-diffusion">
  <div class="card">
    <h2>Feature Diffusion Path</h2>
    <p class="desc">Track how one type-system idea propagates across languages over time. Use Play to animate the adoption path, or switch features to compare different diffusion patterns.</p>
    <div class="viz-toolbar">
      <label class="control-label" for="diffusion-feature-select">Feature</label>
      <select id="diffusion-feature-select" class="control-select"></select>
      <button id="diffusion-play-btn" class="control-button" type="button">Play</button>
      <label class="control-label" for="diffusion-progress">Progress</label>
      <input id="diffusion-progress" class="control-range" type="range" min="1" max="1" value="1">
      <span id="diffusion-progress-label" class="control-note">1 / 1</span>
      <span class="control-note">Chronological reveal from first recorded adoption to later mainstream uptake.</span>
    </div>
    <div id="diffusion-summary" class="mini-dashboard-grid"></div>
    <div id="diffusion-chart"></div>
  </div>
</div>

<!-- Panel 7: Clusters -->
<div class="panel" id="panel-clusters">
  <div class="card">
    <h2>Domain Cluster Analysis</h2>
    <p class="desc">Languages are projected into 2D from their feature vectors and clustered with k-means. Color shows cluster membership, while symbol shape preserves the top-level domain group.</p>
    <div class="viz-toolbar">
      <button id="cluster-label-toggle" class="control-button" type="button">Hide labels</button>
      <span class="control-note">Use the label toggle when you want a cleaner scatterplot for shape-level reading instead of point-level inspection.</span>
    </div>
    <div id="cluster-summary" class="mini-dashboard-grid"></div>
    <div id="cluster-chart"></div>
    <div id="cluster-legend" class="legend-row"></div>
  </div>
</div>

<!-- Panel 8: Lineage -->
<div class="panel" id="panel-lineage">
  <div class="card">
    <h2>Language Influence Lineage</h2>
    <p class="desc">A directed influence graph connecting roots, descendants, and cross-ecosystem ideas. This view emphasizes conceptual inheritance rather than strict implementation compatibility.</p>
    <div class="viz-toolbar">
      <label class="control-label" for="lineage-focus-select">Focus language</label>
      <select id="lineage-focus-select" class="control-select">
        <option value="__all__">Show all</option>
      </select>
      <button id="lineage-reset-btn" class="control-button" type="button">Reset focus</button>
      <span class="control-note">Focus mode highlights the local neighborhood so influence paths are easier to read in dense regions.</span>
    </div>
    <div id="lineage-summary" class="mini-dashboard-grid"></div>
    <div id="lineage-chart"></div>
  </div>
</div>

<!-- Panel 9: Recommender -->
<div class="panel" id="panel-recommender">
  <div class="card">
    <h2>Interactive Feature Recommender</h2>
    <p class="desc">Pick the type-system capabilities you need and set a minimum acceptable score. The configurator ranks languages by fit and shows which requirements are still missing.</p>
    <div class="viz-toolbar recommender-toolbar">
      <label class="control-label" for="recommender-threshold">Minimum score</label>
      <select id="recommender-threshold" class="control-select">
        <option value="2">2 / 5</option>
        <option value="3" selected>3 / 5</option>
        <option value="4">4 / 5</option>
      </select>
      <label class="control-label" for="recommender-domain-filter">Domain</label>
      <select id="recommender-domain-filter" class="control-select">
        <option value="__all__">All domains</option>
      </select>
      <button id="recommender-clear-btn" class="control-button" type="button">Clear filters</button>
      <span class="control-note">Recommendation score balances hard matches, partial coverage, and overall language complexity.</span>
    </div>
    <div id="recommender-summary" class="mini-dashboard-grid"></div>
    <div id="recommender-features" class="feature-filter-grid"></div>
    <div id="recommender-results" class="recommendation-grid"></div>
  </div>
</div>

<script>
// ====== DATA (injected by Python) ======
const DATA = __DASHBOARD_DATA__;

// ====== TAB SWITCHING ======
const tabs = document.querySelectorAll('.tab');
const panels = document.querySelectorAll('.panel');
tabs.forEach(tab => {
  tab.addEventListener('click', () => {
    tabs.forEach(t => t.classList.remove('active'));
    panels.forEach(p => p.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById('panel-' + tab.dataset.panel).classList.add('active');
    if (tab.dataset.panel === 'network') initNetwork();
    if (tab.dataset.panel === 'timeline') initTimeline();
    if (tab.dataset.panel === 'diffusion') initDiffusion();
    if (tab.dataset.panel === 'clusters') initClusters();
    if (tab.dataset.panel === 'lineage') initLineage();
    if (tab.dataset.panel === 'recommender') initRecommender();
    if (tab.dataset.panel === 'radar') initRadar();
    if (tab.dataset.panel === 'popularity') initPopularity();
  });
});

// ====== TOOLTIP ======
const tooltip = document.getElementById('tooltip');
function positionTip(evt) {
  const offset = 14;
  const maxLeft = Math.max(12, window.innerWidth - tooltip.offsetWidth - 12);
  const maxTop = Math.max(12, window.innerHeight - tooltip.offsetHeight - 12);
  tooltip.style.left = Math.min(evt.clientX + offset, maxLeft) + 'px';
  tooltip.style.top = Math.min(evt.clientY + offset, maxTop) + 'px';
}
function showTip(evt, html) {
  tooltip.innerHTML = html;
  tooltip.style.display = 'block';
  positionTip(evt);
}
function hideTip() { tooltip.style.display = 'none'; }
function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
function escapeAttr(value) {
  return escapeHtml(value);
}

// ====== COLORS ======
const maxScore = DATA.max_score || 5;
function scoreColor(score) {
  // 0-5 color scale: dark -> blue -> bright
  const colors = [
    '#1a1d27',  // 0: not supported
    '#2a3050',  // 1: minimal
    '#3b5998',  // 2: basic
    '#5070c0',  // 3: moderate
    '#6c8cff',  // 4: strong
    '#8eb4ff',  // 5: full
  ];
  return colors[Math.min(score, 5)] || colors[0];
}
function scoreLabel(score) {
  const labels = ['Not supported', 'Minimal', 'Basic', 'Moderate', 'Strong', 'Full'];
  return labels[Math.min(score, 5)] || labels[0];
}
const paradigmColors = {
  'Systems': '#ff6c8c',
  'Functional': '#6cffa0',
  'Multi-paradigm': '#6c8cff',
  'Imperative': '#ffa06c',
  'Object-oriented': '#c96cff',
};
const domainGroupSymbols = {
  'Systems': 'diamond',
  'Web': 'roundRect',
  'Academic': 'triangle',
  'Enterprise': 'rect',
  'General': 'circle',
  'Mobile': 'pin',
  'Scientific': 'arrow',
};
const clusterPalette = ['#6c8cff', '#ff8b6c', '#6cffa0', '#c96cff'];
const domainGroups = [...new Set(DATA.heatmap.map(lang => lang.domain.split(' / ')[0]))].sort();
const domainGroupColors = {
  'Academic': '#ffdb6c',
  'Enterprise': '#6c8cff',
  'General': '#9aa4bf',
  'Mobile': '#ff8b6c',
  'Scientific': '#6cffa0',
  'Systems': '#ff6c8c',
  'Web': '#6cffe0',
};

// ====== SCORING LEGEND ======
(function buildLegend() {
  const container = document.getElementById('score-legend');
  for (let i = 0; i <= 5; i++) {
    const item = document.createElement('span');
    item.className = 'score-legend-item';
    item.innerHTML = `<span class="score-legend-swatch" style="background:${scoreColor(i)}"></span>${i} — ${scoreLabel(i)}`;
    container.appendChild(item);
  }
})();

// ====== 1. HEATMAP ======
(function initHeatmap() {
  const features = DATA.features;
  const labels = DATA.feature_labels;
  const shortLabels = DATA.feature_short_labels || {};
  const langs = DATA.heatmap;
  const totalMax = features.length * maxScore;

  // Build table — headers are just column indices (1-based)
  let html = '<div class="matrix-shell">';
  html += '<div class="matrix-toolbar">';
  html += '<div class="matrix-toolbar-copy"><strong>Dense comparison matrix.</strong> The table stays compact by default. Hover any column header or score cell to inspect the full feature name and rationale.</div>';
  html += '<div class="matrix-summary">';
  html += `<div class="summary-pill"><strong>${langs.length}</strong><span>Languages</span></div>`;
  html += `<div class="summary-pill"><strong>${features.length}</strong><span>Features</span></div>`;
  html += `<div class="summary-pill"><strong>${totalMax}</strong><span>Max score</span></div>`;
  html += '</div></div>';
  html += '<div class="heatmap-scroll">';
  html += '<table class="heatmap-table"><thead><tr>';
  html += '<th class="lang-name"><div class="corner-card"><strong>Language</strong><span>Sorted by total type-system complexity</span></div></th>';
  features.forEach((f, i) => {
    const shortLabel = shortLabels[f] || labels[f];
    const featureTip = escapeAttr(`<b>#${i+1}</b> ${escapeHtml(labels[f])}`);
    html += `<th class="feature-col" data-col="${i}" data-tip-html="${featureTip}"><div class="feature-head-card"><span class="feature-head-index">${String(i + 1).padStart(2, '0')}</span><span class="feature-head-short">${shortLabel}</span></div></th>`;
  });
  html += '<th class="score-col"><div class="score-head-card"><strong>Total</strong><span>Aggregate feature score</span></div></th></tr></thead><tbody>';

  langs.forEach(lang => {
    html += `<tr><td class="lang-name"><div class="lang-cell-card"><span class="lang-title">${lang.name}</span><span class="lang-meta">${lang.year} / ${lang.paradigm}</span></div></td>`;
    lang.scores.forEach((s, i) => {
      const fl = labels[features[i]];
      const rationale = lang.rationale && lang.rationale[features[i]]
        ? '<br><em style="color:#aab">' + escapeHtml(lang.rationale[features[i]]) + '</em>'
        : '';
      const cellTip = escapeAttr(`<b>${escapeHtml(lang.name)}</b> &mdash; ${escapeHtml(fl)}<br>Score: ${s}/5 (${scoreLabel(s)})${rationale}`);
      html += `<td data-col="${i}"><span class="heatmap-cell" data-tip-html="${cellTip}" style="background:${scoreColor(s)}">${s}</span></td>`;
    });
    const pct = Math.round(lang.complexity / totalMax * 100);
    html += `<td class="heatmap-score-td score-col"><div class="score-cell-card"><span class="heatmap-score-bar">`
          + `<span class="complexity-bar" style="width:${pct}px"></span>${lang.complexity}</span></div></td>`;
    html += '</tr>';
  });
  html += '</tbody></table></div>';

  html += '</div>';

  document.getElementById('heatmap-container').innerHTML = html;

  document.querySelectorAll('#heatmap-container [data-tip-html]').forEach(node => {
    node.addEventListener('mouseenter', e => showTip(e, node.dataset.tipHtml));
    node.addEventListener('mousemove', e => positionTip(e));
    node.addEventListener('mouseleave', hideTip);
  });

  const table = document.querySelector('.heatmap-table');
  table.addEventListener('mouseover', e => {
    const td = e.target.closest('[data-col]');
    if (!td) return;
    const col = td.dataset.col;
    table.querySelectorAll('[data-col="'+col+'"]').forEach(c => c.classList.add('col-hover'));
  });
  table.addEventListener('mouseout', e => {
    const td = e.target.closest('[data-col]');
    if (!td) return;
    const col = td.dataset.col;
    table.querySelectorAll('[data-col="'+col+'"]').forEach(c => c.classList.remove('col-hover'));
  });
})();

// ====== 2. RADAR CHART ======
let radarChart = null;
const radarSelected = new Set();
const RADAR_COLORS = ['#6c8cff', '#ff6c8c', '#6cffa0', '#ffa06c'];

function initRadar() {
  if (!radarChart) {
    radarChart = echarts.init(document.getElementById('radar-chart'));
    window.addEventListener('resize', () => radarChart.resize());
  }
  updateRadar();
}

function updateRadar() {
  if (!radarChart) return;
  const features = DATA.features;
  const labels = DATA.feature_labels;
  const indicator = features.map(f => ({ name: labels[f].split('/')[0].split('(')[0].trim(), max: maxScore }));

  const selected = Array.from(radarSelected);
  const series = selected.map((name, i) => {
    const lang = DATA.heatmap.find(l => l.name === name);
    return {
      value: lang.scores,
      name: name,
      lineStyle: { width: 2 },
      areaStyle: { opacity: 0.15 },
      itemStyle: { color: RADAR_COLORS[i % RADAR_COLORS.length] },
    };
  });

  radarChart.setOption({
    tooltip: { trigger: 'item' },
    legend: { data: selected, bottom: 0, textStyle: { color: '#8b8fa3' } },
    radar: {
      indicator: indicator,
      shape: 'polygon',
      axisName: { color: '#8b8fa3', fontSize: 11 },
      splitArea: { areaStyle: { color: ['#1a1d27', '#1f2233'] } },
      splitLine: { lineStyle: { color: '#2a2d3a' } },
      axisLine: { lineStyle: { color: '#2a2d3a' } },
    },
    series: [{ type: 'radar', data: series }],
  }, true);
}

(function buildRadarChips() {
  const container = document.getElementById('radar-chips');
  const defaults = ['Rust', 'Haskell', 'Go'];
  DATA.heatmap.forEach(lang => {
    const chip = document.createElement('div');
    chip.className = 'lang-chip';
    chip.textContent = lang.name;
    if (defaults.includes(lang.name)) {
      chip.classList.add('selected');
      radarSelected.add(lang.name);
    }
    chip.addEventListener('click', () => {
      if (radarSelected.has(lang.name)) {
        radarSelected.delete(lang.name);
        chip.classList.remove('selected');
      } else if (radarSelected.size < 4) {
        radarSelected.add(lang.name);
        chip.classList.add('selected');
      }
      updateRadar();
    });
    container.appendChild(chip);
  });
})();

// ====== 3. TIMELINE (ECharts scatter) ======
let timelineChart = null;
function initTimeline() {
  if (timelineChart) { timelineChart.resize(); return; }
  timelineChart = echarts.init(document.getElementById('timeline-chart'));
  window.addEventListener('resize', () => timelineChart && timelineChart.resize());

  const events = DATA.timeline;
  const allLangs = [...new Set(events.map(e => e.language))];
  const allFeatures = [...new Set(events.map(e => e.feature))];
  const labels = DATA.feature_labels;

  // group by feature
  const seriesMap = {};
  const featureColors = {};
  const palette = ['#6c8cff','#ff6c8c','#6cffa0','#ffa06c','#c96cff','#ffdb6c',
                    '#6cffe0','#ff9e6c','#9e6cff','#6caaff','#ff6caa','#aaff6c','#ff6c6c','#6cffff'];
  allFeatures.forEach((f, i) => {
    featureColors[f] = palette[i % palette.length];
    seriesMap[f] = [];
  });

  events.forEach(e => {
    const langIdx = allLangs.indexOf(e.language);
    seriesMap[e.feature].push({
      value: [e.year, langIdx],
      language: e.language,
      feature_label: e.feature_label,
    });
  });

  const series = allFeatures.map(f => ({
    name: labels[f] ? labels[f].split('/')[0].split('(')[0].trim() : f,
    type: 'scatter',
    symbolSize: 14,
    data: seriesMap[f],
    itemStyle: { color: featureColors[f] },
  }));

  timelineChart.setOption({
    tooltip: {
      formatter: p => `<b>${p.data.language}</b><br>${p.data.feature_label}<br>Year: ${p.data.value[0]}`,
    },
    legend: {
      type: 'scroll',
      bottom: 0,
      textStyle: { color: '#8b8fa3', fontSize: 10 },
      pageTextStyle: { color: '#8b8fa3' },
    },
    grid: { left: 120, right: 30, top: 20, bottom: 80 },
    xAxis: {
      type: 'value',
      name: 'Year',
      min: 1985,
      max: 2026,
      axisLabel: { color: '#8b8fa3', formatter: v => String(v) },
      splitLine: { lineStyle: { color: '#2a2d3a' } },
    },
    yAxis: {
      type: 'category',
      data: allLangs,
      axisLabel: { color: '#e1e4ed', fontSize: 11 },
      splitLine: { lineStyle: { color: '#1f2233' } },
    },
    series: series,
  });
}

// ====== 4. FEATURE DIFFUSION ======
let diffusionChart = null;
let diffusionFeatureKey = null;
let diffusionRevealCount = 0;
let diffusionTimer = null;

function renderDiffusionSummary(featureData, visibleEvents) {
  const container = document.getElementById('diffusion-summary');
  if (!container) return;
  const origin = featureData.events[0];
  const latest = visibleEvents[visibleEvents.length - 1] || origin;
  const domainSpread = [...new Set(visibleEvents.map(event => event.domain_group))];
  container.innerHTML = `
    <div class="mini-dashboard-card">
      <strong>Origin</strong>
      <span>${origin.language} (${origin.year})<br>${origin.domain}</span>
    </div>
    <div class="mini-dashboard-card">
      <strong>Latest visible</strong>
      <span>${latest.language} (${latest.year})<br>Score ${latest.score}/5</span>
    </div>
    <div class="mini-dashboard-card">
      <strong>Coverage</strong>
      <span>${visibleEvents.length} of ${featureData.events.length} adoptions revealed<br>${domainSpread.join(', ') || 'No domains yet'}</span>
    </div>
  `;
}

function stopDiffusionAnimation() {
  if (diffusionTimer) {
    window.clearInterval(diffusionTimer);
    diffusionTimer = null;
  }
  const btn = document.getElementById('diffusion-play-btn');
  if (btn) btn.textContent = 'Play';
}

function renderDiffusion(featureKey, revealCount = null) {
  if (!diffusionChart) return;
  const featureData = DATA.diffusion.features[featureKey];
  if (!featureData) return;

  const events = featureData.events;
  const visibleCount = revealCount == null ? events.length : revealCount;
  const visibleEvents = events.slice(0, visibleCount);
  const categories = events.map(event => event.language);
  const latest = visibleEvents[visibleEvents.length - 1];
  const progress = document.getElementById('diffusion-progress');
  const progressLabel = document.getElementById('diffusion-progress-label');
  if (progress) {
    progress.max = String(events.length);
    progress.value = String(Math.max(1, visibleEvents.length));
  }
  if (progressLabel) {
    progressLabel.textContent = `${visibleEvents.length} / ${events.length}`;
  }
  renderDiffusionSummary(featureData, visibleEvents);

  diffusionChart.setOption({
    title: {
      text: featureData.label,
      left: 12,
      top: 10,
      textStyle: { color: '#e1e4ed', fontSize: 14, fontWeight: 700 },
      subtext: latest ? `Visible adoptions: ${visibleEvents.length}/${events.length} / Latest reveal: ${latest.language} (${latest.year})` : 'No adoption data',
      subtextStyle: { color: '#8b8fa3', fontSize: 11 },
    },
    tooltip: {
      trigger: 'item',
      formatter: params => {
        const event = params.data && params.data.meta ? params.data.meta : params.data;
        if (!event) return '';
        return `<b>${event.language}</b><br>${featureData.label}<br>Year: ${event.year}<br>Score: ${event.score}/5<br>Domain: ${event.domain}`;
      },
    },
    grid: { left: 120, right: 40, top: 70, bottom: 50 },
    xAxis: {
      type: 'value',
      min: Math.min(...events.map(event => event.year)) - 1,
      max: Math.max(...events.map(event => event.year)) + 1,
      axisLabel: { color: '#8b8fa3' },
      splitLine: { lineStyle: { color: '#2a2d3a' } },
    },
    yAxis: {
      type: 'category',
      data: categories,
      axisLabel: { color: '#e1e4ed', fontSize: 11 },
      splitLine: { lineStyle: { color: '#1f2233' } },
    },
    series: [
      {
        type: 'line',
        data: visibleEvents.map(event => ({
          value: [event.year, event.language],
          meta: event,
        })),
        smooth: false,
        symbol: 'circle',
        symbolSize: 10,
        lineStyle: { color: '#6c8cff', width: 3 },
        itemStyle: { color: '#6c8cff' },
      },
      {
        type: 'effectScatter',
        data: latest ? [{
          value: [latest.year, latest.language],
          meta: latest,
        }] : [],
        rippleEffect: { scale: 3, brushType: 'stroke' },
        symbolSize: 16,
        itemStyle: { color: '#ff6c8c' },
        z: 10,
      },
    ],
    animationDuration: 500,
  }, true);
}

function initDiffusion() {
  if (!diffusionChart) {
    diffusionChart = echarts.init(document.getElementById('diffusion-chart'));
    window.addEventListener('resize', () => diffusionChart && diffusionChart.resize());

    const select = document.getElementById('diffusion-feature-select');
    const features = Object.entries(DATA.diffusion.features);
    features.forEach(([featureKey, featureValue]) => {
      const option = document.createElement('option');
      option.value = featureKey;
      option.textContent = featureValue.label;
      select.appendChild(option);
    });

    diffusionFeatureKey = DATA.diffusion.default_feature;
    select.value = diffusionFeatureKey;
    select.addEventListener('change', () => {
      stopDiffusionAnimation();
      diffusionFeatureKey = select.value;
      diffusionRevealCount = DATA.diffusion.features[diffusionFeatureKey].events.length;
      renderDiffusion(diffusionFeatureKey, diffusionRevealCount);
    });

    document.getElementById('diffusion-play-btn').addEventListener('click', () => {
      const total = DATA.diffusion.features[diffusionFeatureKey].events.length;
      if (diffusionTimer) {
        stopDiffusionAnimation();
        return;
      }
      diffusionRevealCount = 1;
      renderDiffusion(diffusionFeatureKey, diffusionRevealCount);
      document.getElementById('diffusion-play-btn').textContent = 'Pause';
      diffusionTimer = window.setInterval(() => {
        diffusionRevealCount += 1;
        renderDiffusion(diffusionFeatureKey, diffusionRevealCount);
        if (diffusionRevealCount >= total) {
          stopDiffusionAnimation();
        }
      }, 850);
    });

    document.getElementById('diffusion-progress').addEventListener('input', event => {
      stopDiffusionAnimation();
      diffusionRevealCount = Number(event.target.value);
      renderDiffusion(diffusionFeatureKey, diffusionRevealCount);
    });
  }

  diffusionFeatureKey = diffusionFeatureKey || DATA.diffusion.default_feature;
  diffusionRevealCount = DATA.diffusion.features[diffusionFeatureKey].events.length;
  renderDiffusion(diffusionFeatureKey, diffusionRevealCount);
}

// ====== 5. DOMAIN CLUSTERS ======
let clusterChart = null;
let clusterLabelsVisible = true;

function renderClusterMeta() {
  const summary = document.getElementById('cluster-summary');
  const legend = document.getElementById('cluster-legend');
  if (summary) {
    const groups = [0, 1, 2].map(clusterIndex => {
      const clusterPoints = DATA.clusters.points.filter(point => point.cluster === clusterIndex);
      const dominantDomain = clusterPoints.reduce((acc, point) => {
        acc[point.domain_group] = (acc[point.domain_group] || 0) + 1;
        return acc;
      }, {});
      const topDomain = Object.entries(dominantDomain).sort((a, b) => b[1] - a[1])[0];
      return `
        <div class="mini-dashboard-card">
          <strong>${DATA.clusters.cluster_labels[String(clusterIndex)] || `Cluster ${clusterIndex + 1}`}</strong>
          <span>${clusterPoints.length} languages<br>Dominant domain: ${topDomain ? topDomain[0] : 'N/A'}</span>
        </div>
      `;
    });
    summary.innerHTML = groups.join('');
  }
  if (legend) {
    legend.innerHTML = domainGroups.map(group => `
      <span class="legend-chip">
        <span class="legend-swatch" style="background:${domainGroupColors[group] || '#8892b0'}"></span>
        ${group} domain
      </span>
    `).join('');
  }
}

function initClusters() {
  if (!clusterChart) {
    clusterChart = echarts.init(document.getElementById('cluster-chart'));
    window.addEventListener('resize', () => clusterChart && clusterChart.resize());
    document.getElementById('cluster-label-toggle').addEventListener('click', () => {
      clusterLabelsVisible = !clusterLabelsVisible;
      document.getElementById('cluster-label-toggle').textContent = clusterLabelsVisible ? 'Hide labels' : 'Show labels';
      initClusters();
    });
  }

  renderClusterMeta();
  const points = DATA.clusters.points;
  const series = [0, 1, 2].map(clusterIndex => ({
    name: DATA.clusters.cluster_labels[String(clusterIndex)] || `Cluster ${clusterIndex + 1}`,
    type: 'scatter',
    data: points
      .filter(point => point.cluster === clusterIndex)
      .map(point => ({
        value: [point.x, point.y, point.complexity],
        name: point.name,
        domain: point.domain,
        domain_group: point.domain_group,
        cluster_label: point.cluster_label,
        paradigm: point.paradigm,
        symbol: domainGroupSymbols[point.domain_group] || 'circle',
        symbolSize: Math.max(12, point.complexity / 2),
        itemStyle: { color: clusterPalette[clusterIndex % clusterPalette.length] },
      })),
    emphasis: { focus: 'series' },
    label: {
      show: clusterLabelsVisible,
      formatter: params => params.data.name,
      position: 'top',
      color: '#aeb6d1',
      fontSize: 10,
    },
  }));

  clusterChart.setOption({
    tooltip: {
      formatter: params => `<b>${params.data.name}</b><br>${params.data.cluster_label}<br>Domain: ${params.data.domain}<br>Paradigm: ${params.data.paradigm}<br>Complexity: ${params.data.value[2]}`,
    },
    legend: {
      bottom: 0,
      textStyle: { color: '#8b8fa3' },
    },
    grid: { left: 60, right: 30, top: 30, bottom: 70 },
    xAxis: {
      type: 'value',
      name: 'Principal Component 1',
      axisLabel: { color: '#8b8fa3' },
      splitLine: { lineStyle: { color: '#2a2d3a' } },
    },
    yAxis: {
      type: 'value',
      name: 'Principal Component 2',
      axisLabel: { color: '#8b8fa3' },
      splitLine: { lineStyle: { color: '#2a2d3a' } },
    },
    series,
  }, true);
}

// ====== 6. LINEAGE GRAPH ======
let lineageChart = null;
let lineageFocus = '__all__';

function renderLineageSummary(focusName) {
  const summary = document.getElementById('lineage-summary');
  if (!summary) return;

  if (focusName === '__all__') {
    const rootCount = DATA.lineage.nodes.filter(node => node.virtual).length;
    summary.innerHTML = `
      <div class="mini-dashboard-card">
        <strong>Roots</strong>
        <span>${rootCount} virtual lineage anchors</span>
      </div>
      <div class="mini-dashboard-card">
        <strong>Influence edges</strong>
        <span>${DATA.lineage.edges.length} directed relationships in the current map</span>
      </div>
      <div class="mini-dashboard-card">
        <strong>How to read</strong>
        <span>Select a language to highlight only its immediate upstream and downstream influences.</span>
      </div>
    `;
    return;
  }

  const incoming = DATA.lineage.edges.filter(edge => edge.target === focusName);
  const outgoing = DATA.lineage.edges.filter(edge => edge.source === focusName);
  summary.innerHTML = `
    <div class="mini-dashboard-card">
      <strong>Focused language</strong>
      <span>${focusName}</span>
    </div>
    <div class="mini-dashboard-card">
      <strong>Influenced by</strong>
      <span>${incoming.length ? incoming.map(edge => edge.source).join(', ') : 'No incoming links in the current map'}</span>
    </div>
    <div class="mini-dashboard-card">
      <strong>Influenced</strong>
      <span>${outgoing.length ? outgoing.map(edge => edge.target).join(', ') : 'No outgoing links in the current map'}</span>
    </div>
  `;
}

function renderLineage() {
  if (!lineageChart) return;
  const categories = [
    ...new Set(DATA.lineage.nodes.map(node => node.virtual ? 'Root lineage' : node.domain_group)),
  ].map(name => ({ name }));
  const highlighted = new Set();
  if (lineageFocus !== '__all__') {
    highlighted.add(lineageFocus);
    DATA.lineage.edges.forEach(edge => {
      if (edge.source === lineageFocus || edge.target === lineageFocus) {
        highlighted.add(edge.source);
        highlighted.add(edge.target);
      }
    });
  }
  renderLineageSummary(lineageFocus);

  lineageChart.setOption({
    tooltip: {
      formatter: params => {
        if (params.dataType === 'edge') {
          return `<b>${params.data.source}</b> -> <b>${params.data.target}</b><br>${params.data.reason}`;
        }
        const node = params.data;
        return `<b>${node.name}</b><br>${node.virtual ? 'Virtual lineage root' : `${node.paradigm} / ${node.domain}`}<br>Year: ${node.year}`;
      },
    },
    legend: {
      bottom: 0,
      textStyle: { color: '#8b8fa3' },
    },
    series: [{
      type: 'graph',
      layout: 'force',
      roam: true,
      draggable: true,
      force: {
        repulsion: 220,
        edgeLength: 140,
        gravity: 0.08,
      },
      label: {
        show: true,
        color: '#e1e4ed',
        fontSize: 11,
      },
      categories,
      edgeSymbol: ['none', 'arrow'],
      edgeSymbolSize: [0, 10],
      lineStyle: {
        color: '#5e6788',
        width: 1.6,
        curveness: 0.14,
        opacity: 0.75,
      },
      data: DATA.lineage.nodes.map(node => {
        const active = lineageFocus === '__all__' || highlighted.has(node.name);
        return {
          ...node,
          category: categories.findIndex(category => category.name === (node.virtual ? 'Root lineage' : node.domain_group)),
          symbolSize: node.virtual ? 34 : Math.max(20, Math.min(46, node.complexity)),
          itemStyle: {
            color: node.virtual ? '#ffdb6c' : (paradigmColors[node.paradigm] || '#6c8cff'),
            opacity: active ? (node.virtual ? 0.96 : 0.9) : 0.18,
          },
          label: { opacity: active ? 1 : 0.22 },
        };
      }),
      links: DATA.lineage.edges.map(edge => {
        const active = lineageFocus === '__all__' || edge.source === lineageFocus || edge.target === lineageFocus;
        return {
          ...edge,
          lineStyle: {
            color: active ? '#7e96ff' : '#4c5370',
            opacity: active ? 0.92 : 0.12,
            width: active ? 2.4 : 1.2,
            curveness: 0.14,
          },
        };
      }),
    }],
  }, true);
}

function initLineage() {
  if (!lineageChart) {
    lineageChart = echarts.init(document.getElementById('lineage-chart'));
    window.addEventListener('resize', () => lineageChart && lineageChart.resize());
    const focusSelect = document.getElementById('lineage-focus-select');
    DATA.lineage.nodes
      .filter(node => !node.virtual)
      .sort((a, b) => a.name.localeCompare(b.name))
      .forEach(node => {
        const option = document.createElement('option');
        option.value = node.name;
        option.textContent = node.name;
        focusSelect.appendChild(option);
      });
    focusSelect.addEventListener('change', event => {
      lineageFocus = event.target.value;
      renderLineage();
    });
    document.getElementById('lineage-reset-btn').addEventListener('click', () => {
      lineageFocus = '__all__';
      focusSelect.value = '__all__';
      renderLineage();
    });
  }

  renderLineage();
}

// ====== 7. NETWORK (D3 force) ======
let networkInited = false;
function initNetwork() {
  if (networkInited) return;
  networkInited = true;

  const svg = d3.select('#network-svg');
  const width = svg.node().getBoundingClientRect().width;
  const height = 600;

  const nodes = DATA.network.nodes.map(d => ({...d, id: d.name}));
  const links = DATA.network.edges.map(d => ({
    source: d.source,
    target: d.target,
    value: d.similarity,
  }));

  const maxComplexity = d3.max(nodes, d => d.complexity);
  const rScale = d3.scaleSqrt().domain([0, maxComplexity]).range([6, 24]);

  const sim = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(d => (1 - d.value) * 250))
    .force('charge', d3.forceManyBody().strength(-200))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(d => rScale(d.complexity) + 4));

  const link = svg.append('g')
    .selectAll('line')
    .data(links)
    .join('line')
    .attr('class', 'link')
    .attr('stroke', '#4a4d5a')
    .attr('stroke-width', d => d.value * 3);

  const nodeG = svg.append('g')
    .selectAll('g')
    .data(nodes)
    .join('g')
    .call(d3.drag()
      .on('start', (e, d) => { if (!e.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
      .on('drag', (e, d) => { d.fx = e.x; d.fy = e.y; })
      .on('end', (e, d) => { if (!e.active) sim.alphaTarget(0); d.fx = null; d.fy = null; })
    );

  nodeG.append('circle')
    .attr('r', d => rScale(d.complexity))
    .attr('fill', d => paradigmColors[d.paradigm] || '#6c8cff')
    .attr('fill-opacity', 0.8)
    .attr('stroke', '#fff')
    .attr('stroke-width', 1.5)
    .on('mouseenter', (evt, d) => {
      showTip(evt, `<b>${d.name}</b><br>Paradigm: ${d.paradigm}<br>Domain: ${d.domain}<br>Complexity: ${d.complexity}`);
    })
    .on('mouseleave', hideTip);

  nodeG.append('text')
    .attr('class', 'node-label')
    .attr('dy', d => rScale(d.complexity) + 14)
    .attr('text-anchor', 'middle')
    .text(d => d.name);

  sim.on('tick', () => {
    link
      .attr('x1', d => d.source.x).attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
    nodeG.attr('transform', d => `translate(${d.x},${d.y})`);
  });
}

// ====== 8. RECOMMENDER ======
let recommenderReady = false;
const selectedRecommenderFeatures = new Set();

function renderRecommendations() {
  const container = document.getElementById('recommender-results');
  const summary = document.getElementById('recommender-summary');
  const threshold = Number(document.getElementById('recommender-threshold').value);
  const domainFilter = document.getElementById('recommender-domain-filter').value;
  const selected = Array.from(selectedRecommenderFeatures);
  const shortLabels = DATA.feature_short_labels || {};
  const domainFiltered = DATA.heatmap.filter(lang => {
    const group = lang.domain.split(' / ')[0];
    return domainFilter === '__all__' || group === domainFilter;
  });

  if (!selected.length) {
    const topByComplexity = [...domainFiltered].slice(0, 6);
    if (summary) {
      summary.innerHTML = `
        <div class="recommendation-hero">
          <strong>Start by choosing capabilities</strong>
          <span>${domainFilter === '__all__' ? 'All domain groups are currently visible.' : `${domainFilter} languages are currently visible.`} Once you pick features, the recommender will score hard matches and surface trade-offs.</span>
        </div>
      `;
    }
    container.innerHTML = topByComplexity.map(lang => `
      <div class="recommendation-card">
        <div class="recommendation-head">
          <div>
            <h3>${lang.name}</h3>
            <div class="recommendation-meta">${lang.year} / ${lang.paradigm} / ${lang.domain}</div>
          </div>
          <div class="recommendation-score">${lang.complexity}</div>
        </div>
        <div class="recommendation-empty">Select one or more features above to turn this into a constraint-based recommender. Until then, this view shows the most feature-rich languages in the dataset.</div>
      </div>
    `).join('');
    return;
  }

  const ranked = domainFiltered.map(lang => {
    const matched = [];
    const missing = [];
    let score = 0;
    selected.forEach(feature => {
      const index = DATA.features.indexOf(feature);
      const value = lang.scores[index];
      if (value >= threshold) {
        matched.push({ feature, value });
        score += 10 + value;
      } else {
        missing.push({ feature, value });
        score += value;
      }
    });
    score += lang.complexity / 10;
    return { lang, matched, missing, score };
  }).sort((a, b) => {
    if (b.matched.length !== a.matched.length) return b.matched.length - a.matched.length;
    if (b.score !== a.score) return b.score - a.score;
    return b.lang.complexity - a.lang.complexity;
  });
  const best = ranked[0];
  if (summary) {
    summary.innerHTML = `
      <div class="recommendation-hero">
        <strong>${best ? `Best current match: ${best.lang.name}` : 'No matching languages in this slice'}</strong>
        <span>${best ? `${best.matched.length} of ${selected.length} selected capabilities meet the ${threshold}/5 threshold${domainFilter === '__all__' ? '' : ` within the ${domainFilter} slice`}.` : 'Try widening the domain filter or lowering the threshold.'}</span>
      </div>
      <div class="mini-dashboard-card">
        <strong>Selected features</strong>
        <span>${selected.map(feature => shortLabels[feature] || DATA.feature_labels[feature]).join(', ')}</span>
      </div>
      <div class="mini-dashboard-card">
        <strong>Threshold</strong>
        <span>${threshold} / 5 minimum acceptable implementation depth</span>
      </div>
      <div class="mini-dashboard-card">
        <strong>Domain filter</strong>
        <span>${domainFilter === '__all__' ? 'All domain groups' : domainFilter}</span>
      </div>
    `;
  }

  container.innerHTML = ranked.slice(0, 8).map(({ lang, matched, missing, score }) => `
    <div class="recommendation-card">
      <div class="recommendation-head">
        <div>
          <h3>${lang.name}</h3>
          <div class="recommendation-meta">${lang.year} / ${lang.paradigm} / ${lang.domain}</div>
        </div>
        <div class="recommendation-score">${matched.length}/${selected.length}</div>
      </div>
      <div class="recommendation-meta">Recommendation score: ${score.toFixed(1)} / Total complexity: ${lang.complexity}</div>
      <div class="recommendation-section">
        <strong>Matches</strong>
        <div class="pill-row">${matched.length ? matched.map(item => `<span class="mini-pill match">${shortLabels[item.feature] || DATA.feature_labels[item.feature]} ${item.value}/5</span>`).join('') : '<span class="recommendation-empty">No features meet the threshold yet.</span>'}</div>
      </div>
      <div class="recommendation-section">
        <strong>Missing or weak</strong>
        <div class="pill-row">${missing.length ? missing.map(item => `<span class="mini-pill missing">${shortLabels[item.feature] || DATA.feature_labels[item.feature]} ${item.value}/5</span>`).join('') : '<span class="mini-pill match">All selected requirements are covered</span>'}</div>
      </div>
    </div>
  `).join('');
}

function initRecommender() {
  if (!recommenderReady) {
    recommenderReady = true;
    const featureContainer = document.getElementById('recommender-features');
    const domainFilter = document.getElementById('recommender-domain-filter');
    domainGroups.forEach(group => {
      const option = document.createElement('option');
      option.value = group;
      option.textContent = group;
      domainFilter.appendChild(option);
    });
    DATA.features.forEach(feature => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'feature-toggle';
      button.innerHTML = `<strong>${DATA.feature_short_labels[feature] || DATA.feature_labels[feature]}</strong><small>${DATA.feature_labels[feature]}</small>`;
      button.addEventListener('click', () => {
        if (selectedRecommenderFeatures.has(feature)) {
          selectedRecommenderFeatures.delete(feature);
          button.classList.remove('active');
        } else {
          selectedRecommenderFeatures.add(feature);
          button.classList.add('active');
        }
        renderRecommendations();
      });
      featureContainer.appendChild(button);
    });

    document.getElementById('recommender-threshold').addEventListener('change', renderRecommendations);
    document.getElementById('recommender-domain-filter').addEventListener('change', renderRecommendations);
    document.getElementById('recommender-clear-btn').addEventListener('click', () => {
      selectedRecommenderFeatures.clear();
      document.querySelectorAll('.feature-toggle').forEach(button => button.classList.remove('active'));
      document.getElementById('recommender-domain-filter').value = '__all__';
      document.getElementById('recommender-threshold').value = '3';
      renderRecommendations();
    });
  }

  renderRecommendations();
}

// ====== 9. POPULARITY ANALYSIS ======
let popChart = null;
let currentMetric = 'tiobe_rank';

function initPopularity() {
  if (!popChart) {
    popChart = echarts.init(document.getElementById('popularity-chart'));
    window.addEventListener('resize', () => popChart && popChart.resize());
  }
  updatePopularity();
}

function updatePopularity() {
  if (!popChart) return;
  const popData = DATA.popularity;

  const metricConfig = {
    tiobe_rank: { name: 'TIOBE Rank', invert: true, axisLabel: 'Rank (lower = more popular)' },
    github_stars_rank: { name: 'GitHub Stars Rank', invert: true, axisLabel: 'Rank (lower = more popular)' },
    stackoverflow_loved_pct: { name: 'SO Loved %', invert: false, axisLabel: 'Loved % (higher = more loved)' },
  };
  const cfg = metricConfig[currentMetric];

  const seriesData = popData.map(d => {
    const yVal = d[currentMetric] || 0;
    return {
      value: [d.complexity, yVal],
      name: d.name,
      paradigm: d.paradigm,
      notes: d.notes,
      symbolSize: Math.max(10, (d.stackoverflow_loved_pct || 50) / 3),
      itemStyle: { color: paradigmColors[d.paradigm] || '#6c8cff' },
    };
  });

  popChart.setOption({
    tooltip: {
      formatter: p => {
        const d = p.data;
        return `<b>${d.name}</b><br>Paradigm: ${d.paradigm}<br>Complexity: ${d.value[0]}<br>${cfg.name}: ${d.value[1]}<br><em style="color:#aab">${d.notes}</em>`;
      },
    },
    grid: { left: 80, right: 40, top: 40, bottom: 60 },
    xAxis: {
      type: 'value',
      name: 'Type Complexity Score',
      nameLocation: 'center',
      nameGap: 35,
      axisLabel: { color: '#8b8fa3' },
      splitLine: { lineStyle: { color: '#2a2d3a' } },
    },
    yAxis: {
      type: 'value',
      name: cfg.axisLabel,
      nameLocation: 'center',
      nameGap: 55,
      inverse: cfg.invert,
      axisLabel: { color: '#8b8fa3' },
      splitLine: { lineStyle: { color: '#2a2d3a' } },
    },
    series: [{
      type: 'scatter',
      data: seriesData,
      label: {
        show: true,
        formatter: p => p.data.name,
        position: 'right',
        color: '#8b8fa3',
        fontSize: 10,
      },
    }],
  }, true);
}

// Popularity metric buttons
document.querySelectorAll('.pop-metric-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.pop-metric-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentMetric = btn.dataset.metric;
    updatePopularity();
  });
});
</script>
</body>
</html>
"""
