相似性网络是类型系统知识图谱仪表板的核心可视化模块之一，通过力导向图（Force-Directed Graph）直观展示编程语言在类型系统特性维度上的相似性聚类关系。该面板允许开发者从宏观视角观察语言间的类型系统设计趋同与分化模式，发现跨范式影响与技术创新扩散路径。

## 架构设计

相似性网络的实现采用前后端分离架构，数据生成与可视化渲染职责明确划分。

```mermaid
flowchart LR
    subgraph Backend["后端数据生成 Python"]
        A[原始语言数据] --> B[特征向量提取]
        B --> C[余弦相似度计算]
        C --> D[阈值过滤]
        D --> E[网络数据结构]
    end
    
    subgraph DataFile["数据文件"]
        E --> F[dashboard-data.json]
    end
    
    subgraph Frontend["前端可视化 Vue 3 + ECharts"]
        F --> G[useDashboardData]
        G --> H[SimilarityNetworkPanel]
        H --> I[Force-directed Graph]
    end
```

**数据生成管道**位于 `src/data_processing.py` 的 `prepare_dashboard_data` 函数中，第 584-594 行处理网络节点与边的构建逻辑。该管道首先调用 `compute_similarity_edges` 函数计算所有语言两两之间的余弦相似度，然后以 0.65 为阈值过滤出高相似度连接。

Sources: [data_processing.py#L584-L594](src/data_processing.py#L584-L594)

## 核心算法

### 余弦相似度计算

相似性网络的边权重基于余弦相似度（Cosine Similarity）算法计算。该算法衡量两个特征向量在方向上的一致性，忽略向量长度的影响。

```python
def cosine_similarity(a: list[int], b: list[int]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)
```

该函数计算两个 14 维特征向量（对应 14 种类型系统特性）的点积，然后除以各自模长的乘积。计算结果范围为 [-1, 1]，在类型系统评分场景下，由于评分均为非负值，相似度范围为 [0, 1]。

Sources: [data_processing.py#L60-L67](src/data_processing.py#L60-L67)

### 边过滤策略

```python
def compute_similarity_edges(data: dict, threshold: float = 0.6) -> list[dict]:
    """Compute similarity edges for the network graph."""
    vectors = get_feature_vectors(data)
    names = list(vectors.keys())
    edges = []
    for i, name_a in enumerate(names):
        for j, name_b in enumerate(names):
            if i < j:
                sim = cosine_similarity(vectors[name_a], vectors[name_b])
                if sim >= threshold:
                    edges.append({
                        "source": name_a,
                        "target": name_b,
                        "similarity": round(sim, 4),
                    })
    return edges
```

实际使用中将阈值调整为 0.65 以平衡网络密度与可读性。默认的 `prepare_dashboard_data` 函数在第 585 行调用此函数时指定了 `threshold=0.65`，确保仅展示类型系统设计高度相似的语言对。

Sources: [data_processing.py#L100-L115](src/data_processing.py#L100-L115)
Sources: [data_processing.py#L585](src/data_processing.py#L585)

## 数据结构

### 类型定义

网络数据结构由节点与边两部分组成，在 TypeScript 类型定义中明确规范了数据结构。

```typescript
export interface NetworkNode {
  name: string
  paradigm: string
  domain: string
  complexity: number
}

export interface NetworkEdge {
  source: string
  target: string
  similarity: number
}
```

节点包含语言的名称、所属范式、应用领域以及类型复杂度评分（14 个特性评分的总和）。边结构记录相似语言对的连接关系与相似度数值。

Sources: [types/dashboard.ts#L29-L40](frontend/src/types/dashboard.ts#L29-L40)

### 完整数据格式

```json
{
  "network": {
    "nodes": [
      {
        "name": "Rust",
        "paradigm": "Systems",
        "domain": "Systems programming",
        "complexity": 32
      }
    ],
    "edges": [
      {
        "source": "Rust",
        "target": "Haskell",
        "similarity": 0.7371
      }
    ]
  }
}
```

实际数据包含 27 个语言节点，基于 0.65 阈值筛选出约 80 条边。例如 Rust 与 Swift 的相似度高达 0.9583（几乎相同的类型系统设计），而 Rust 与 C 的相似度仅为 0.7024，反映出 C 的类型系统极度简洁。

Sources: [dashboard-data.json#L894-L1157](frontend/public/dashboard-data.json#L894-L1157)

## 前端组件实现

### 组件结构

`SimilarityNetworkPanel.vue` 组件负责将网络数据渲染为交互式力导向图。

```vue
<script setup lang="ts">
const props = defineProps<{
  data: DashboardData
}>()

const chartOption = computed<EChartsOption>(() => ({
  tooltip: {
    formatter: (params: any) => {
      if (params.dataType === 'edge') {
        return `<b>${params.data.source}</b> - <b>${params.data.target}</b><br>Similarity: ${params.data.value}`
      }
      return `<b>${params.data.name}</b><br>${params.data.paradigm}<br>${params.data.domain}<br>Complexity: ${params.data.complexity}`
    },
  },
  series: [
    {
      type: 'graph',
      layout: 'force',
      roam: true,
      draggable: true,
      force: { repulsion: 240, edgeLength: 150, gravity: 0.08 },
      // ...
    }
  ]
}))
</script>
```

组件接收 `DashboardData` 类型的数据作为属性，通过计算属性动态生成 ECharts 配置对象。

Sources: [SimilarityNetworkPanel.vue#L9-L69](frontend/src/components/panels/SimilarityNetworkPanel.vue#L9-L69)

### 可视化映射

| 视觉维度 | 数据映射 | 映射规则 |
|---------|---------|---------|
| 节点颜色 | `paradigm` | 范式分类对应固定配色：Functional=#6fe0b7, Multi-paradigm=#7e96ff, Systems=#ffcf7a |
| 节点大小 | `complexity` | 复杂度评分映射至 [18, 46] 像素范围 |
| 边的粗细 | `similarity` | 相似度乘以 3，范围约 [1.95, 3] |
| 边的透明度 | 固定 | 0.55，营造层次感 |

节点大小计算函数 `nodeSize` 确保节点既不会过小难以点击，也不会过大遮挡其他节点：

```typescript
function nodeSize(complexity: number) {
  return Math.max(18, Math.min(46, complexity))
}
```

Sources: [SimilarityNetworkPanel.vue#L13-L15](frontend/src/components/panels/SimilarityNetworkPanel.vue#L13-L15)
Sources: [constants.ts#L1-L8](frontend/src/constants.ts#L1-L8)

### 力导向布局参数

ECharts 的 force 布局使用以下物理参数控制图形布局行为：

| 参数 | 值 | 作用 |
|-----|-----|------|
| repulsion | 240 | 节点间的斥力强度，影响整体密度 |
| edgeLength | 150 | 边的理想长度 |
| gravity | 0.08 | 中心引力，防止节点漂移过远 |

`roam: true` 和 `draggable: true` 参数启用用户交互式平移、缩放和拖拽节点功能。

Sources: [SimilarityNetworkPanel.vue#L37](frontend/src/components/panels/SimilarityNetworkPanel.vue#L37)

## 交互功能

### 悬停提示

Tooltip 根据鼠标悬停对象类型动态格式化显示内容：

**节点悬停**：显示语言名称、范式分类、应用领域、类型复杂度评分

**边悬停**：显示相连两种语言的名称及精确相似度数值（保留两位小数）

```typescript
formatter: (params: any) => {
  if (params.dataType === 'edge') {
    return `<b>${params.data.source}</b> - <b>${params.data.target}</b><br>Similarity: ${params.data.value}`
  }
  return `<b>${params.data.name}</b><br>${params.data.paradigm}<br>${params.data.domain}<br>Complexity: ${params.data.complexity}`
}
```

### 图例过滤

底部图例展示所有范式分类，支持点击切换显示/隐藏特定范式的语言节点，实现跨范式对比分析。

Sources: [SimilarityNetworkPanel.vue#L26-L29](frontend/src/components/panels/SimilarityNetworkPanel.vue#L26-L29)

## 技术栈集成

### 图表渲染引擎

ECharts 是百度开源的可视化图表库，`EChartPanel.vue` 组件封装了图表初始化、响应式调整和资源清理逻辑。

```typescript
onMounted(() => {
  if (!root.value) return
  chart.value = echarts.init(root.value)
  renderChart(props.option)
})
```

组件通过 `useResizeObserver` 监听容器尺寸变化，自动调用 `chart.resize()` 保持图表适配。

Sources: [EChartPanel.vue#L20-L24](frontend/src/components/EChartPanel.vue#L20-L24)
Sources: [EChartPanel.vue#L34-L36](frontend/src/components/EChartPanel.vue#L34-L36)

### 数据获取

`useDashboardData.ts` composable 提供统一的仪表板数据获取接口，通过 `@vueuse/core` 的 `useFetch` 封装异步请求逻辑。

```typescript
export function useDashboardData() {
  const baseUrl = import.meta.env.BASE_URL.endsWith('/')
    ? import.meta.env.BASE_URL
    : `${import.meta.env.BASE_URL}/`
  const dataUrl = `${baseUrl}dashboard-data.json`
  const { data, error, isFetching, isFinished } = useFetch(dataUrl)
    .get()
    .json<DashboardData>()
  // ...
}
```

Sources: [useDashboardData.ts#L6-L12](frontend/src/composables/useDashboardData.ts#L6-L12)

## 典型聚类模式

基于 0.65 相似度阈值，相似性网络展现出以下典型聚类模式：

**ML 函数式家族**（Haskell-Scala-Idris-PureScript）：以强类型系统、纯函数式编程、模式匹配为核心特征，成员间相似度普遍超过 0.95。

**系统编程家族**（Rust-Swift-Nim-Zig）：以内存安全、所有权系统、现代语言设计为共同特征，Rust 与 Swift 的相似度高达 0.9583。

**Web 开发家族**（TypeScript-Elm-Gleam-PureScript）：以函数式与类型安全的融合为特征，TypeScript 通过渐进式类型系统连接传统动态语言与现代函数式语言。

**企业级语言家族**（Java-C#-Kotlin）：以面向对象为基础，逐步引入函数式特性，Java 与 C# 的相似度为 0.8879。

## 下一步探索

完成相似性网络分析后，建议深入以下相关模块：

- **[特性共现分析](13-feature-co-occurrence-te-xing-gong-xian)**：探究类型系统特性之间的协同出现规律，理解为何某些特性倾向于同时出现
- **[领域聚类](18-domain-clusters-ling-yu-ju-lei)**：通过 PCA 降维与 K-means 聚类验证相似性网络的聚类假设
- **[谱系图](19-lineage-graph-pu-xi-tu)**：追溯语言间的设计影响脉络，区分相似是源自趋同进化还是亲缘遗传