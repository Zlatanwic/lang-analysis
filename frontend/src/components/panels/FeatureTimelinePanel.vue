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
      textStyle: { color: '#98a4c6', fontSize: 10 },
    },
    grid: { left: 120, right: 30, top: 24, bottom: 80 },
    xAxis: {
      type: 'value',
      min: 1985,
      max: 2026,
      axisLabel: { color: '#98a4c6' },
      splitLine: { lineStyle: { color: '#27314b' } },
    },
    yAxis: {
      type: 'category',
      data: languages,
      axisLabel: { color: '#edf2ff', fontSize: 11 },
      splitLine: { lineStyle: { color: '#182033' } },
    },
    series,
  } as EChartsOption
})
</script>

<template>
  <PanelCard
    title="Feature Timeline"
    description="Track when individual capabilities first appeared in each language, grouped by feature family."
  >
    <EChartPanel :option="chartOption" />
  </PanelCard>
</template>
