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

const selected = ref<string[]>(['Rust', 'Haskell', 'Go'])

function toggleLanguage(name: string) {
  if (selected.value.includes(name)) {
    selected.value = selected.value.filter((item) => item !== name)
    return
  }

  if (selected.value.length >= 4) return
  selected.value = [...selected.value, name]
}

const chartOption = computed<EChartsOption>(() => {
  const series = selected.value
    .map((name) => props.data.heatmap.find((language) => language.name === name))
    .filter((language): language is NonNullable<typeof language> => Boolean(language))
    .map((language) => ({
      value: language.scores,
      name: language.name,
      lineStyle: { width: 2, color: paradigmColors[language.paradigm] ?? '#7e96ff' },
      itemStyle: { color: paradigmColors[language.paradigm] ?? '#7e96ff' },
      areaStyle: { opacity: 0.14 },
    }))

  return {
    tooltip: { trigger: 'item' },
    legend: {
      bottom: 0,
      textStyle: { color: '#454745' },
      data: selected.value,
    },
    radar: {
      indicator: props.data.features.map((feature) => ({
        name: props.data.feature_short_labels[feature],
        max: props.data.max_score,
      })),
      axisName: { color: '#454745', fontSize: 11 },
      splitArea: { areaStyle: { color: ['#f5f5f4', '#e8e8e6'] } },
      splitLine: { lineStyle: { color: '#e8e8e6' } },
      axisLine: { lineStyle: { color: '#e8e8e6' } },
    },
    series: [{ type: 'radar', data: series }],
  }
})
</script>

<template>
  <PanelCard
    eyebrow="轮廓"
    title="雷达图对比"
    description="在完整类型系统表面上对比最多四种语言，同时保持紧凑矩阵的上下文。"
  >
    <div class="stack">
      <div class="chip-list">
        <button
          v-for="language in data.heatmap"
          :key="language.name"
          class="language-chip"
          :class="{ active: selected.includes(language.name) }"
          @click="toggleLanguage(language.name)"
        >
          {{ language.name }}
        </button>
      </div>
      <EChartPanel :option="chartOption" />
    </div>
  </PanelCard>
</template>
