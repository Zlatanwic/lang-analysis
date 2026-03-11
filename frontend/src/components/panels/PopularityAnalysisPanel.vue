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

const metric = ref<'tiobe_rank' | 'github_stars_rank' | 'stackoverflow_loved_pct'>('tiobe_rank')

const metricConfig = {
  tiobe_rank: { name: 'TIOBE Rank', invert: true, axisLabel: 'Rank (lower is better)' },
  github_stars_rank: { name: 'GitHub Stars Rank', invert: true, axisLabel: 'Rank (lower is better)' },
  stackoverflow_loved_pct: { name: 'Stack Overflow Loved %', invert: false, axisLabel: 'Loved % (higher is better)' },
}

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
    axisLabel: { color: '#98a4c6' },
    splitLine: { lineStyle: { color: '#27314b' } },
  },
  yAxis: {
    type: 'value',
    name: metricConfig[metric.value].axisLabel,
    nameLocation: 'middle',
    nameGap: 52,
    inverse: metricConfig[metric.value].invert,
    axisLabel: { color: '#98a4c6' },
    splitLine: { lineStyle: { color: '#27314b' } },
  },
  series: [
    {
      type: 'scatter',
      data: props.data.popularity.map((point) => ({
        value: [point.complexity, point[metric.value] ?? 0],
        name: point.name,
        notes: point.notes,
        symbolSize: Math.max(10, (point.stackoverflow_loved_pct ?? 50) / 3),
        itemStyle: { color: paradigmColors[point.paradigm] ?? '#7e96ff' },
      })),
      label: {
        show: true,
        formatter: (params: any) => params.data.name,
        position: 'right',
        color: '#98a4c6',
        fontSize: 10,
      },
    },
  ],
}) as EChartsOption)
</script>

<template>
  <PanelCard
    title="Popularity Analysis"
    description="Cross-check type complexity against external popularity and affinity signals."
  >
    <template #actions>
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
    </template>

    <EChartPanel :option="chartOption" />
  </PanelCard>
</template>
