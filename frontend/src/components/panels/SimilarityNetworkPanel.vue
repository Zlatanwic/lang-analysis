<script setup lang="ts">
import { computed } from 'vue'
import type { EChartsOption } from 'echarts'
import PanelCard from '../PanelCard.vue'
import EChartPanel from '../EChartPanel.vue'
import type { DashboardData } from '../../types/dashboard'
import { paradigmColors } from '../../constants'

const props = defineProps<{
  data: DashboardData
}>()

function nodeSize(complexity: number) {
  return Math.max(18, Math.min(46, complexity))
}

const chartOption = computed<EChartsOption>(() => ({
  tooltip: {
    formatter: (params: any) => {
      if (params.dataType === 'edge') {
        return `<b>${params.data.source}</b> - <b>${params.data.target}</b><br>Similarity: ${params.data.value}`
      }
      return `<b>${params.data.name}</b><br>${params.data.paradigm}<br>${params.data.domain}<br>Complexity: ${params.data.complexity}`
    },
  },
  legend: {
    bottom: 0,
    textStyle: { color: '#98a4c6' },
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
        color: '#4f608d',
      },
      label: {
        show: true,
        color: '#edf2ff',
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
      links: props.data.network.edges.map((edge) => ({
        ...edge,
        value: edge.similarity.toFixed(2),
        lineStyle: {
          width: Math.max(1.4, edge.similarity * 3),
          color: '#4f608d',
          opacity: 0.55,
        },
      })),
    },
  ],
}) as EChartsOption)
</script>

<template>
  <PanelCard
    title="Similarity Network"
    description="Force-directed view of languages that cluster together once you compare their feature profiles."
  >
    <EChartPanel :option="chartOption" />
  </PanelCard>
</template>
