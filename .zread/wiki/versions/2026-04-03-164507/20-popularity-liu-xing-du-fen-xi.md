Popularity 面板是类型系统知识图谱仪表板的**信号层（Signal Layer）**，用于将语言的类型系统复杂度与外部生态系统的流行度指标进行交叉对比。该面板揭示了一个核心张力：**开发者喜爱度（TIOBE 指数、GitHub 星标排名、Stack Overflow Loved %）与类型系统复杂性之间的关系**。

Sources: [PopularityAnalysisPanel.vue](frontend/src/components/panels/PopularityAnalysisPanel.vue#L1-L99)

## 数据架构

### PopularityPoint 数据结构

流行度分析的数据点包含语言的多维度信息，通过 `build_popularity_data()` 函数从原始 JSON 中提取并与复杂度计算合并：

```typescript
interface PopularityPoint {
  name: string           // 语言名称
  paradigm: string      // 编程范式
  domain: string        // 应用领域
  complexity: number     // 类型复杂度得分（所有特性评分之和）
  tiobe_rank?: number    // TIOBE 指数排名
  github_stars_rank?: number  // GitHub 星标排名
  stackoverflow_loved_pct?: number  // Stack Overflow 喜爱度百分比
  notes?: string        // 备注信息
}
```

Sources: [dashboard.ts](frontend/src/types/dashboard.ts#L42-L51)

### Python 数据处理管道

`build_popularity_data()` 函数遍历所有语言，提取其 `popularity` 字段并计算类型复杂度：

```python
def build_popularity_data(data: dict) -> list[dict]:
    """Extract popularity data for the complexity-vs-popularity analysis."""
    result = []
    for lang in data["languages"]:
        pop = lang.get("popularity", {})
        if not pop:
            continue
        complexity = compute_type_complexity_score(lang)
        result.append({
            "name": lang["name"],
            "paradigm": lang["paradigm"],
            "domain": lang["domain"],
            "complexity": complexity,
            "tiobe_rank": pop.get("tiobe_rank"),
            "github_stars_rank": pop.get("github_stars_rank"),
            "stackoverflow_loved_pct": pop.get("stackoverflow_loved_pct"),
            "notes": pop.get("notes", ""),
        })
    return result
```

Sources: [data_processing.py](src/data_processing.py#L200-L218)

复杂度计算函数将语言所有 14 个类型系统特性的评分求和：

```python
def compute_type_complexity_score(lang: dict) -> int:
    """Sum of all feature scores as a rough complexity metric."""
    return sum(lang["features"].values())
```

Sources: [data_processing.py](src/data_processing.py#L118-L120)

## 三维指标体系

面板提供了三个可切换的流行度指标，每个指标从不同维度反映语言的市场表现：

| 指标 | 数据来源 | 可视化方式 | 语义说明 |
|------|----------|-----------|----------|
| **TIOBE Rank** | TIOBE Index | Y轴（反向） | 商业/企业采用度 |
| **GitHub Stars Rank** | GitHub 仓库星标 | Y轴（反向） | 开源社区活跃度 |
| **Stack Overflow Loved %** | SO 调查问卷 | Y轴 + 气泡大小 | 开发者主观满意度 |

Sources: [PopularityAnalysisPanel.vue](frontend/src/components/panels/PopularityAnalysisPanel.vue#L13-L19)

### 指标配置

```typescript
const metricConfig = {
  tiobe_rank: { 
    name: 'TIOBE Rank', 
    invert: true,  // 排名越低越好
    axisLabel: 'Rank (lower is better)' 
  },
  github_stars_rank: { 
    name: 'GitHub Stars Rank', 
    invert: true, 
    axisLabel: 'Rank (lower is better)' 
  },
  stackoverflow_loved_pct: { 
    name: 'Stack Overflow Loved %', 
    invert: false,  // 百分比越高越好
    axisLabel: 'Loved % (higher is better)' 
  },
}
```

## 可视化实现

### ECharts 散点图配置

面板使用 ECharts 的 scatter 类型实现交互式二维散点图：

```typescript
const chartOption = computed<EChartsOption>(() => ({
  tooltip: {
    formatter: (params: any) =>
      `<b>${params.data.name}</b><br>Complexity: ${params.data.value[0]}<br>${metricConfig[metric.value].name}: ${params.data.value[1]}<br><em>${params.data.notes ?? ''}</em>`,
  },
  grid: { left: 86, right: 40, top: 40, bottom: 70 },
  xAxis: {
    type: 'value',
    name: 'Type complexity',
    nameLocation: 'middle',
    nameGap: 34,
  },
  yAxis: {
    type: 'value',
    name: metricConfig[metric.value].axisLabel,
    nameLocation: 'middle',
    nameGap: 52,
    inverse: metricConfig[metric.value].invert,  // 根据指标决定是否反转
  },
  series: [{
    type: 'scatter',
    data: props.data.popularity.map((point) => ({
      value: [point.complexity, point[metric.value] ?? 0],
      name: point.name,
      notes: point.notes,
      symbolSize: Math.max(10, (point.stackoverflow_loved_pct ?? 50) / 3),
      itemStyle: { color: paradigmColors[point.paradigm] ?? '#7e96ff' },
    })),
  }],
}))
```

Sources: [PopularityAnalysisPanel.vue](frontend/src/components/panels/PopularityAnalysisPanel.vue#L21-L63)

### 视觉编码

| 视觉通道 | 映射维度 | 说明 |
|---------|---------|------|
| **X 坐标** | Type Complexity | 类型系统复杂度（0-70 分范围） |
| **Y 坐标** | 流行度指标 | 根据选择的指标动态切换 |
| **气泡大小** | stackoverflow_loved_pct | SO 喜爱度作为辅助维度 |
| **颜色** | Paradigm | 编程范式区分（函数式/多范式/系统级/面向对象） |

Sources: [PopularityAnalysisPanel.vue](frontend/src/components/panels/PopularityAnalysisPanel.vue#L51-L52), [constants.ts](frontend/src/constants.ts#L1-L8)

## 范式颜色映射

```typescript
export const paradigmColors: Record<string, string> = {
  Functional: '#6fe0b7',       // 绿色 — 函数式语言
  'Multi-paradigm': '#7e96ff', // 蓝色 — 多范式语言
  Systems: '#ffcf7a',          // 橙色 — 系统级语言
  ObjectOriented: '#ff8aa1',   // 粉色 — 纯面向对象语言
  'Object-oriented': '#ff8aa1',
  Procedural: '#9bd6ff',       // 浅蓝 — 过程式语言
}
```

Sources: [constants.ts](frontend/src/constants.ts#L1-L8)

## 交互设计

### 指标切换按钮

面板顶部的三个按钮允许用户实时切换 Y 轴指标：

```vue
<button
  class="metric-button"
  :class="{ active: metric === 'tiobe_rank' }"
  @click="metric = 'tiobe_rank'"
>
  TIOBE
</button>
<button
  class="metric-button"
  :class="{ active: metric === 'github_stars_rank' }"
  @click="metric = 'github_stars_rank'"
>
  GitHub
</button>
<button
  class="metric-button"
  :class="{ active: metric === 'stackoverflow_loved_pct' }"
  @click="metric = 'stackoverflow_loved_pct'"
>
  Loved %
</button>
```

Sources: [PopularityAnalysisPanel.vue](frontend/src/components/panels/PopularityAnalysisPanel.vue#L72-L94)

## 数据样本分析

根据 `languages.json` 中的数据，典型语言在复杂度-流行度图中的位置呈现明显模式：

| 语言 | 复杂度 | TIOBE | GitHub | SO Loved % | 特征 |
|------|--------|-------|--------|------------|------|
| Rust | 33 | 14 | 8 | 87% | 高复杂度 + 高喜爱度 |
| TypeScript | 29 | 7 | 3 | 73% | 中高复杂度 + 极高流行度 |
| Haskell | 38 | 30 | 22 | 58% | 最高复杂度 + 中等流行度 |
| Elixir | 15 | 33 | 20 | 68% | 低复杂度 + 稳定社区 |
| Ruby | 9 | 16 | 13 | 45% | 最低复杂度 + 中等流行度 |

Sources: [languages.json](data/languages.json#L30-L75), [languages.json](data/languages.json#L117-L123), [languages.json](data/languages.json#L164-L169)

## 关键洞察

该面板揭示了类型系统设计的**现实权衡**：

1. **满意度悖论**：高类型复杂度的语言（如 Rust）往往获得更高的开发者满意度，但采用率较低
2. **实用性优势**：中等复杂度的语言（TypeScript、Kotlin）往往获得最广泛的采用
3. **极简策略**：动态类型语言虽然特性少，但在特定领域（Web 脚本、数据处理）保持稳定地位

## 下一步探索

完成流行度分析后，建议继续探索以下面板以深入理解语言特性与市场表现的关系：

- **[Feature Matrix 特性矩阵](11-feature-matrix-te-xing-ju-zhen)** — 深入了解各语言的具体特性评分
- **[Feature Recommender 语言推荐器](21-feature-recommender-yu-yan-tui-jian-qi)** — 基于约束条件选择适合的语言
- **[Lineage Graph 谱系图](19-lineage-graph-pu-xi-tu)** — 追溯语言的设计影响脉络