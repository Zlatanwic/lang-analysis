<script setup lang="ts">
import { computed, shallowRef, ref, watch } from 'vue'
import type { EChartsOption } from 'echarts'
import PanelCard from '../PanelCard.vue'
import EChartPanel from '../EChartPanel.vue'
import type { DashboardData } from '../../types/dashboard'
import { paradigmColors } from '../../constants'

const props = defineProps<{
  data: DashboardData
}>()

const similarityThreshold = ref(0.3)
const thresholdDisplay = computed(() => similarityThreshold.value.toFixed(2))

function nodeSize(complexity: number) {
  return Math.max(18, Math.min(46, complexity))
}

const filteredEdges = computed(() => {
  return props.data.network.edges.filter((edge) => edge.similarity >= similarityThreshold.value)
})

const chartOption = shallowRef<EChartsOption>({} as EChartsOption)

function updateChart() {
  chartOption.value = {
    tooltip: {
      formatter: (params: any) => {
        if (params.dataType === 'edge') {
          return `<b>${params.data.source}</b> - <b>${params.data.target}</b><br>相似度：${params.data.value}`
        }
        return `<b>${params.data.name}</b><br>${params.data.paradigm}<br>${params.data.domain}<br>复杂度：${params.data.complexity}`
      },
    },
    legend: {
      bottom: 0,
      textStyle: { color: '#454745' },
      data: [...new Set(props.data.network.nodes.map((node) => node.paradigm))],
    },
    series: [
      {
        type: 'graph',
        layout: 'force',
        roam: true,
        draggable: true,
        force: { repulsion: 240, edgeLength: 150, gravity: 0.08 },
        edgeSymbol: ['none', 'none'],
        lineStyle: {
          width: 1.8,
          opacity: 0.55,
          color: '#868685',
        },
        label: {
          show: true,
          color: '#0e0f0c',
          fontSize: 11,
        },
        data: props.data.network.nodes.map((node) => ({
          ...node,
          symbolSize: nodeSize(node.complexity),
          category: node.paradigm,
          itemStyle: {
            color: paradigmColors[node.paradigm] ?? '#7e96ff',
          },
        })),
        categories: [...new Set(props.data.network.nodes.map((node) => node.paradigm))].map((name) => ({ name })),
        links: filteredEdges.value.map((edge) => ({
          ...edge,
          value: edge.similarity.toFixed(2),
          lineStyle: {
            width: Math.max(1.4, edge.similarity * 3),
            color: '#868685',
            opacity: 0.55,
          },
        })),
      },
    ],
  } as EChartsOption
}

// Initialize
updateChart()

// Watch for threshold changes
watch(similarityThreshold, updateChart)
</script>

<template>
  <PanelCard
    eyebrow="映射"
    title="相似性网络"
    description="一旦比较语言间的特性配置文件，就会聚类的力导向视图。"
  >
    <template #actions>
      <label class="tag">
        相似度阈值
        <input
          :value="similarityThreshold"
          type="range"
          min="0"
          max="1"
          step="0.05"
          @input="similarityThreshold = parseFloat(($event.target as HTMLInputElement).value)"
        />
        {{ thresholdDisplay }}
      </label>
    </template>

    <div class="stack">
      <div class="mini-grid">
        <div class="mini-card">
          <strong>{{ filteredEdges.length }}</strong>
          <span>条连接 / {{ data.network.edges.length }} 条总数</span>
        </div>
      </div>
      <EChartPanel :option="chartOption" />
    </div>
  </PanelCard>
</template>
