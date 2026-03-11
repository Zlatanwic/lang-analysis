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
  #heatmap-container { overflow-x: auto; }
  .heatmap-table { border-collapse: collapse; width: 100%; min-width: 900px; }
  .heatmap-table th, .heatmap-table td {
    padding: 6px 4px;
    text-align: center;
    font-size: 0.75rem;
    border: 1px solid var(--border);
  }
  .heatmap-table th { color: var(--text-dim); font-weight: 500; white-space: nowrap; }
  .heatmap-table th.lang-name { text-align: left; padding-left: 12px; min-width: 100px; }
  .heatmap-table td.lang-name {
    text-align: left; padding-left: 12px; font-weight: 600;
    white-space: nowrap; position: sticky; left: 0; background: var(--card); z-index: 1;
  }
  .heatmap-cell {
    width: 36px; height: 36px; display: inline-block; border-radius: 4px;
    transition: transform 0.15s;
    cursor: pointer;
  }
  .heatmap-cell:hover { transform: scale(1.3); }

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
  }
</style>
</head>
<body>

<div class="header">
  <h1>Programming Language Type System Knowledge Graph</h1>
  <p>An interactive exploration of type system features across <strong>25</strong> programming languages — featuring 0-5 fine-grained scoring, popularity analysis, and scoring rationale.</p>
</div>

<div class="tabs">
  <div class="tab active" data-panel="heatmap">Feature Matrix</div>
  <div class="tab" data-panel="radar">Radar Comparison</div>
  <div class="tab" data-panel="timeline">Feature Timeline</div>
  <div class="tab" data-panel="network">Similarity Network</div>
  <div class="tab" data-panel="popularity">Popularity Analysis</div>
</div>

<div class="tooltip" id="tooltip"></div>

<!-- Panel 1: Heatmap -->
<div class="panel active" id="panel-heatmap">
  <div class="card">
    <h2>Type System Feature Matrix</h2>
    <p class="desc">Rows sorted by total type system complexity score. Scoring: 0 (not supported) to 5 (full/reference implementation). Click cells to see scoring rationale.</p>
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
    if (tab.dataset.panel === 'radar') initRadar();
    if (tab.dataset.panel === 'popularity') initPopularity();
  });
});

// ====== TOOLTIP ======
const tooltip = document.getElementById('tooltip');
function showTip(evt, html) {
  tooltip.innerHTML = html;
  tooltip.style.display = 'block';
  tooltip.style.left = (evt.clientX + 14) + 'px';
  tooltip.style.top = (evt.clientY + 14) + 'px';
}
function hideTip() { tooltip.style.display = 'none'; }

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
  const langs = DATA.heatmap;
  const totalMax = features.length * maxScore;
  let html = '<table class="heatmap-table"><thead><tr><th class="lang-name">Language</th>';
  features.forEach(f => {
    const short = labels[f].split('/')[0].split('(')[0].trim();
    html += `<th title="${labels[f]}">${short.length > 16 ? short.slice(0, 15) + '\u2026' : short}</th>`;
  });
  html += '<th>Score</th></tr></thead><tbody>';
  langs.forEach(lang => {
    html += `<tr><td class="lang-name">${lang.name} <span style="color:var(--text-dim);font-size:0.7rem">(${lang.year})</span></td>`;
    lang.scores.forEach((s, i) => {
      const fl = labels[features[i]];
      const rationale = lang.rationale && lang.rationale[features[i]]
        ? '<br><em style="color:#aab">' + lang.rationale[features[i]] + '</em>'
        : '';
      html += `<td><span class="heatmap-cell" style="background:${scoreColor(s)}" `
            + `onmouseenter="showTip(event,'<b>${lang.name}</b> &mdash; ${fl}<br>Score: ${s}/5 (${scoreLabel(s)})${rationale}')" `
            + `onmouseleave="hideTip()"></span></td>`;
    });
    const pct = Math.round(lang.complexity / totalMax * 100);
    html += `<td><span class="complexity-bar" style="width:${pct}px"></span> ${lang.complexity}/${totalMax}</td>`;
    html += '</tr>';
  });
  html += '</tbody></table>';
  document.getElementById('heatmap-container').innerHTML = html;
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

// ====== 4. NETWORK (D3 force) ======
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

// ====== 5. POPULARITY ANALYSIS ======
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
