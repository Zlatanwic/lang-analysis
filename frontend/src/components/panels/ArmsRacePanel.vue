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
      const yearly = points.find((point: any) => point.seriesName === '年度新增')?.data ?? 0
      const moving = points.find((point: any) => point.seriesName === '5年移动平均')?.data ?? 0
      const cumulative = points.find((point: any) => point.seriesName === '累计总数')?.data ?? 0
      return [
        `<b>${year}</b>`,
        `年度新增：${yearly}`,
        `5年移动平均：${moving}`,
        `累计总数：${cumulative}`,
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
    axisLabel: { color: '#3A5A47' },
    axisLine: { lineStyle: { color: '#C4C2B6' } },
  },
  yAxis: [
    {
      type: 'value',
      name: '新特性引入',
      axisLabel: { color: '#98a4c6' },
      splitLine: { lineStyle: { color: '#C4C2B6' } },
    },
    {
      type: 'value',
      name: '累计总数',
      axisLabel: { color: '#98a4c6' },
      splitLine: { show: false },
    },
  ],
  series: [
    {
      name: '年度新增',
      type: 'bar',
      data: props.data.arms_race.yearly_counts,
      itemStyle: { color: '#ffcf7a', borderRadius: [8, 8, 0, 0] },
      emphasis: { itemStyle: { color: '#ffd88e' } },
    },
    {
      name: '5年移动平均',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 7,
      data: props.data.arms_race.moving_average,
      lineStyle: { width: 3, color: '#6fe0b7' },
      itemStyle: { color: '#6fe0b7' },
    },
    {
      name: '累计总数',
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
    eyebrow="加速"
    title="类型系统军备竞赛指数"
    description="统计每年记录的所有特性引入，然后将年度爆发、持续势能和累积增长叠加成一个加速视图。"
  >
    <div class="stack">
      <div class="mini-grid">
        <div class="mini-card">
          <strong>{{ data.arms_race.total_events }}</strong>
          <span>所有语言时间线中记录的特性引入总数。</span>
        </div>
        <div class="mini-card">
          <strong>{{ data.arms_race.peak_year ?? 'n/a' }}</strong>
          <span>峰值年份，新增记录的特性引入数为 {{ data.arms_race.peak_count }}。</span>
        </div>
        <div class="mini-card">
          <strong>{{ recentAverage }}</strong>
          <span>序列最近5年的平均年度引入量。</span>
        </div>
        <div class="mini-card">
          <strong>{{ momentumRatio }}</strong>
          <span>
            近期势能与早期相比。最新的年度变化：
            {{ latestAcceleration >= 0 ? '+' : '' }}{{ latestAcceleration }}。
          </span>
        </div>
      </div>

      <EChartPanel :option="chartOption" />
    </div>
  </PanelCard>
</template>
