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
  tiobe_rank: { name: 'TIOBE 排名', invert: true, axisLabel: '排名（越低越好）' },
  github_stars_rank: { name: 'GitHub Stars 排名', invert: true, axisLabel: '排名（越低越好）' },
  stackoverflow_loved_pct: { name: 'Stack Overflow 喜爱度 %', invert: false, axisLabel: '喜爱度 %（越高越好）' },
}

const chartOption = computed<EChartsOption>(() => ({
  tooltip: {
    formatter: (params: any) =>
      `<b>${params.data.name}</b><br>复杂度：${params.data.value[0]}<br>${metricConfig[metric.value].name}：${params.data.value[1]}<br><em>${params.data.notes ?? ''}</em>`,
  },
  grid: { left: 86, right: 40, top: 40, bottom: 70 },
  xAxis: {
    type: 'value',
    name: '类型复杂度',
    nameLocation: 'middle',
    nameGap: 34,
    axisLabel: { color: '#454745' },
    splitLine: { lineStyle: { color: '#e8e8e6' } },
  },
  yAxis: {
    type: 'value',
    name: metricConfig[metric.value].axisLabel,
    nameLocation: 'middle',
    nameGap: 52,
    inverse: metricConfig[metric.value].invert,
    axisLabel: { color: '#454745' },
    splitLine: { lineStyle: { color: '#e8e8e6' } },
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
        color: '#454745',
        fontSize: 10,
      },
    },
  ],
}) as EChartsOption)
</script>

<template>
  <PanelCard
    eyebrow="信号"
    title="流行度分析"
    description="将类型复杂度与外部流行度和亲和度信号进行交叉检验。"
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
