<script setup lang="ts">
import { computed } from 'vue'
import type { EChartsOption } from 'echarts'
import PanelCard from '../PanelCard.vue'
import EChartPanel from '../EChartPanel.vue'
import type { DashboardData } from '../../types/dashboard'
import { featurePalette } from '../../constants'

const props = defineProps<{
  data: DashboardData
}>()

const chartOption = computed<EChartsOption>(() => {
  const events = props.data.timeline
  const languages = [...new Set(events.map((event) => event.language))]
  const features = [...new Set(events.map((event) => event.feature))]

  const series = features.map((feature, index) => ({
    name: props.data.feature_short_labels[feature],
    type: 'scatter',
    symbolSize: 13,
    itemStyle: { color: featurePalette[index % featurePalette.length] },
    data: events
      .filter((event) => event.feature === feature)
      .map((event) => ({
        value: [event.year, languages.indexOf(event.language)],
        language: event.language,
        feature_label: event.feature_label,
      })),
  }))

  return {
    tooltip: {
      formatter: (params: any) =>
        `<b>${params.data.language}</b><br>${params.data.feature_label}<br>Year: ${params.data.value[0]}`,
    },
    legend: {
      type: 'scroll',
      bottom: 0,
      textStyle: { color: '#3A5A47', fontSize: 10 },
    },
    grid: { left: 120, right: 30, top: 24, bottom: 80 },
    xAxis: {
      type: 'value',
      min: 1985,
      max: 2026,
      axisLabel: { color: '#3A5A47' },
      splitLine: { lineStyle: { color: '#C4C2B6' } },
    },
    yAxis: {
      type: 'category',
      data: languages,
      axisLabel: { color: '#1D3124', fontSize: 11 },
      splitLine: { lineStyle: { color: '#D4D2C6' } },
    },
    series,
  } as EChartsOption
})
</script>

<template>
  <PanelCard
    eyebrow="序列"
    title="特性时间线"
    description="追踪各语言中个别特性首次出现的时间，按特性家族分组。"
  >
    <EChartPanel :option="chartOption" />
  </PanelCard>
</template>
