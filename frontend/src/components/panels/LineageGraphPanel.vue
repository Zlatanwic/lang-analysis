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
  const categories = [...new Set(props.data.lineage.nodes.map((node) => (node.virtual ? '谱系根源' : node.domain_group)))]

  return {
    tooltip: {
      formatter: (params: any) => {
        if (params.dataType === 'edge') {
          return `<b>${params.data.source}</b> -> <b>${params.data.target}</b><br>${params.data.reason}`
        }
        return `<b>${params.data.name}</b><br>${params.data.virtual ? '虚拟谱系根源' : `${params.data.paradigm} / ${params.data.domain}`}<br>年份：${params.data.year}`
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
    eyebrow="谱系"
    title="语言演化谱系"
    description="有向影响图，展示思想如何在语言家族、运行时和编程时代中传播。"
  >
    <template #actions>
      <select v-model="focus" class="control">
        <option value="__all__">所有语言</option>
        <option
          v-for="node in data.lineage.nodes.filter((item) => !item.virtual).sort((a, b) => a.name.localeCompare(b.name))"
          :key="node.name"
          :value="node.name"
        >
          {{ node.name }}
        </option>
      </select>
      <button class="ghost-button" @click="focus = '__all__'">
        重置
      </button>
    </template>

    <div class="stack">
      <div class="mini-grid">
        <div class="mini-card">
          <strong>{{ focus === '__all__' ? '根源' : '聚焦语言' }}</strong>
          <span>{{ focus === '__all__' ? `${data.lineage.nodes.filter((node) => node.virtual).length} 个虚拟谱系锚点` : focus }}</span>
        </div>
        <div class="mini-card">
          <strong>受影响于</strong>
          <span>{{ focus === '__all__' ? `${data.lineage.edges.length} 条有向边` : (incoming.map((edge) => edge.source).join(', ') || '当前图中无入边') }}</span>
        </div>
        <div class="mini-card">
          <strong>影响</strong>
          <span>{{ focus === '__all__' ? '选择一种语言以检查本地祖先和后代。' : (outgoing.map((edge) => edge.target).join(', ') || '当前图中无出边') }}</span>
        </div>
      </div>

      <EChartPanel :option="chartOption" />
    </div>
  </PanelCard>
</template>
