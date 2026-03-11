<script setup lang="ts">
import { computed, ref } from 'vue'
import type { EChartsOption } from 'echarts'
import PanelCard from '../PanelCard.vue'
import EChartPanel from '../EChartPanel.vue'
import type { DashboardData } from '../../types/dashboard'
import { paradigmColors } from '../../constants'

const props = defineProps<{
  data: DashboardData
}>()

const focus = ref('__all__')

const highlighted = computed(() => {
  if (focus.value === '__all__') {
    return new Set(props.data.lineage.nodes.map((node) => node.name))
  }

  const active = new Set([focus.value])
  props.data.lineage.edges.forEach((edge) => {
    if (edge.source === focus.value || edge.target === focus.value) {
      active.add(edge.source)
      active.add(edge.target)
    }
  })
  return active
})

const incoming = computed(() => props.data.lineage.edges.filter((edge) => edge.target === focus.value))
const outgoing = computed(() => props.data.lineage.edges.filter((edge) => edge.source === focus.value))

const chartOption = computed<EChartsOption>(() => {
  const categories = [...new Set(props.data.lineage.nodes.map((node) => (node.virtual ? 'Root lineage' : node.domain_group)))]

  return {
    tooltip: {
      formatter: (params: any) => {
        if (params.dataType === 'edge') {
          return `<b>${params.data.source}</b> -> <b>${params.data.target}</b><br>${params.data.reason}`
        }
        return `<b>${params.data.name}</b><br>${params.data.virtual ? 'Virtual lineage root' : `${params.data.paradigm} / ${params.data.domain}`}<br>Year: ${params.data.year}`
      },
    },
    legend: {
      bottom: 0,
      textStyle: { color: '#98a4c6' },
      data: categories,
    },
    series: [
      {
        type: 'graph',
        layout: 'force',
        roam: true,
        draggable: true,
        force: { repulsion: 220, edgeLength: 140, gravity: 0.08 },
        edgeSymbol: ['none', 'arrow'],
        edgeSymbolSize: [0, 10],
        lineStyle: { curveness: 0.14, width: 1.6, color: '#5e6788', opacity: 0.75 },
        label: { show: true, color: '#edf2ff', fontSize: 11 },
        categories: categories.map((name) => ({ name })),
        data: props.data.lineage.nodes.map((node) => ({
          ...node,
          category: categories.indexOf(node.virtual ? 'Root lineage' : node.domain_group),
          symbolSize: node.virtual ? 34 : Math.max(20, Math.min(46, node.complexity)),
          itemStyle: {
            color: node.virtual ? '#ffcf7a' : (paradigmColors[node.paradigm] ?? '#7e96ff'),
            opacity: highlighted.value.has(node.name) ? 0.92 : 0.18,
          },
          label: { opacity: highlighted.value.has(node.name) ? 1 : 0.24 },
        })),
        links: props.data.lineage.edges.map((edge) => ({
          ...edge,
          lineStyle: {
            color: focus.value === '__all__' || edge.source === focus.value || edge.target === focus.value ? '#7e96ff' : '#4c5370',
            opacity: focus.value === '__all__' || edge.source === focus.value || edge.target === focus.value ? 0.92 : 0.12,
            width: focus.value === '__all__' || edge.source === focus.value || edge.target === focus.value ? 2.4 : 1.2,
            curveness: 0.14,
          },
        })),
      },
    ],
  } as EChartsOption
})
</script>

<template>
  <PanelCard
    eyebrow="Lineage"
    title="Language Evolution Lineage"
    description="Directed influence map showing how ideas moved across families, runtimes, and programming eras."
  >
    <template #actions>
      <select v-model="focus" class="control">
        <option value="__all__">All languages</option>
        <option
          v-for="node in data.lineage.nodes.filter((item) => !item.virtual).sort((a, b) => a.name.localeCompare(b.name))"
          :key="node.name"
          :value="node.name"
        >
          {{ node.name }}
        </option>
      </select>
      <button class="ghost-button" @click="focus = '__all__'">
        Reset
      </button>
    </template>

    <div class="stack">
      <div class="mini-grid">
        <div class="mini-card">
          <strong>{{ focus === '__all__' ? 'Roots' : 'Focused language' }}</strong>
          <span>{{ focus === '__all__' ? `${data.lineage.nodes.filter((node) => node.virtual).length} virtual lineage anchors` : focus }}</span>
        </div>
        <div class="mini-card">
          <strong>Influenced by</strong>
          <span>{{ focus === '__all__' ? `${data.lineage.edges.length} total directed edges` : (incoming.map((edge) => edge.source).join(', ') || 'No incoming edges in current map') }}</span>
        </div>
        <div class="mini-card">
          <strong>Influenced</strong>
          <span>{{ focus === '__all__' ? 'Select a language to inspect local ancestry and descendants.' : (outgoing.map((edge) => edge.target).join(', ') || 'No outgoing edges in current map') }}</span>
        </div>
      </div>

      <EChartPanel :option="chartOption" />
    </div>
  </PanelCard>
</template>
