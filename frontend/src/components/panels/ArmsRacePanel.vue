<script setup lang="ts">
import { computed } from 'vue'
import type { EChartsOption } from 'echarts'
import PanelCard from '../PanelCard.vue'
import EChartPanel from '../EChartPanel.vue'
import type { DashboardData } from '../../types/dashboard'

const props = defineProps<{
  data: DashboardData
}>()

const recentAverage = computed(() => {
  const counts = props.data.arms_race.yearly_counts
  const window = counts.slice(-5)
  if (!window.length) return 0
  return (window.reduce((sum, value) => sum + value, 0) / window.length).toFixed(2)
})

const momentumRatio = computed(() => {
  const counts = props.data.arms_race.yearly_counts
  if (!counts.length) return '0.0x'

  const splitIndex = Math.max(1, Math.floor(counts.length / 2))
  const early = counts.slice(0, splitIndex)
  const recent = counts.slice(-Math.min(5, counts.length))
  const earlyAverage = early.reduce((sum, value) => sum + value, 0) / early.length
  const recentAverageValue = recent.reduce((sum, value) => sum + value, 0) / recent.length

  if (earlyAverage <= 0) {
    return `${recentAverageValue.toFixed(1)}x`
  }
  return `${(recentAverageValue / earlyAverage).toFixed(1)}x`
})

const latestAcceleration = computed(() => {
  const values = props.data.arms_race.acceleration
  return values.length ? values[values.length - 1] : 0
})

const chartOption = computed<EChartsOption>(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'cross' },
    formatter: (params: any) => {
      const points = Array.isArray(params) ? params : [params]
      const year = points[0]?.axisValueLabel ?? ''
      const yearly = points.find((point: any) => point.seriesName === 'Annual additions')?.data ?? 0
      const moving = points.find((point: any) => point.seriesName === '5-year average')?.data ?? 0
      const cumulative = points.find((point: any) => point.seriesName === 'Cumulative total')?.data ?? 0
      return [
        `<b>${year}</b>`,
        `Annual additions: ${yearly}`,
        `5-year average: ${moving}`,
        `Cumulative total: ${cumulative}`,
      ].join('<br>')
    },
  },
  legend: {
    bottom: 0,
    textStyle: { color: '#98a4c6' },
  },
  grid: { left: 56, right: 62, top: 26, bottom: 72 },
  xAxis: {
    type: 'category',
    data: props.data.arms_race.years.map(String),
    axisLabel: { color: '#98a4c6' },
    axisLine: { lineStyle: { color: '#27314b' } },
  },
  yAxis: [
    {
      type: 'value',
      name: 'New feature arrivals',
      axisLabel: { color: '#98a4c6' },
      splitLine: { lineStyle: { color: '#27314b' } },
    },
    {
      type: 'value',
      name: 'Cumulative total',
      axisLabel: { color: '#98a4c6' },
      splitLine: { show: false },
    },
  ],
  series: [
    {
      name: 'Annual additions',
      type: 'bar',
      data: props.data.arms_race.yearly_counts,
      itemStyle: { color: '#ffcf7a', borderRadius: [8, 8, 0, 0] },
      emphasis: { itemStyle: { color: '#ffd88e' } },
    },
    {
      name: '5-year average',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 7,
      data: props.data.arms_race.moving_average,
      lineStyle: { width: 3, color: '#6fe0b7' },
      itemStyle: { color: '#6fe0b7' },
    },
    {
      name: 'Cumulative total',
      type: 'line',
      yAxisIndex: 1,
      smooth: true,
      symbol: 'none',
      data: props.data.arms_race.cumulative_counts,
      lineStyle: { width: 2, color: '#7e96ff' },
      areaStyle: { color: 'rgba(126, 150, 255, 0.12)' },
    },
  ],
}))
</script>

<template>
  <PanelCard
    eyebrow="Accelerate"
    title="Type-System Arms Race Index"
    description="Counts every recorded feature arrival by year, then layers yearly bursts, trailing momentum, and cumulative buildup into one acceleration view."
  >
    <div class="stack">
      <div class="mini-grid">
        <div class="mini-card">
          <strong>{{ data.arms_race.total_events }}</strong>
          <span>Total feature arrivals recorded across all language timelines.</span>
        </div>
        <div class="mini-card">
          <strong>{{ data.arms_race.peak_year ?? 'n/a' }}</strong>
          <span>Peak burst year with {{ data.arms_race.peak_count }} newly logged feature arrivals.</span>
        </div>
        <div class="mini-card">
          <strong>{{ recentAverage }}</strong>
          <span>Average annual arrivals across the most recent 5 years in the series.</span>
        </div>
        <div class="mini-card">
          <strong>{{ momentumRatio }}</strong>
          <span>
            Recent momentum versus the early era. Latest year-over-year delta:
            {{ latestAcceleration >= 0 ? '+' : '' }}{{ latestAcceleration }}.
          </span>
        </div>
      </div>

      <EChartPanel :option="chartOption" />
    </div>
  </PanelCard>
</template>
