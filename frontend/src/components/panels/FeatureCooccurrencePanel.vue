<script setup lang="ts">
import { computed } from 'vue'
import type { EChartsOption } from 'echarts'
import PanelCard from '../PanelCard.vue'
import EChartPanel from '../EChartPanel.vue'
import type { DashboardData } from '../../types/dashboard'

const props = defineProps<{
  data: DashboardData
}>()

const shortLabels = computed(() =>
  props.data.cooccurrence.features.map((feature) => props.data.feature_short_labels[feature] ?? feature),
)

const mostCommonFeature = computed(() => {
  const entries = Object.entries(props.data.cooccurrence.prevalence)
  if (!entries.length) return null
  const [feature, count] = entries.sort((a, b) => b[1] - a[1])[0]
  return {
    feature,
    count,
    label: props.data.feature_labels[feature] ?? feature,
    short: props.data.feature_short_labels[feature] ?? feature,
  }
})

const chartOption = computed<EChartsOption>(() => ({
  tooltip: {
    formatter: (params: any) => {
      const data = params.data
      const xFeature = props.data.cooccurrence.features[data.value[0]]
      const yFeature = props.data.cooccurrence.features[data.value[1]]
      return [
        `<b>${props.data.feature_labels[xFeature]}</b> x <b>${props.data.feature_labels[yFeature]}</b>`,
        `相关性：${Number(data.value[2]).toFixed(2)}`,
        `共同语言：${data.cooccurrence}`,
        `${props.data.feature_short_labels[xFeature]} 支持度：${data.support_x}`,
        `${props.data.feature_short_labels[yFeature]} 支持度：${data.support_y}`,
      ].join('<br>')
    },
  },
  grid: { left: 110, right: 40, top: 72, bottom: 96 },
  xAxis: {
    type: 'category',
    data: shortLabels.value,
    axisLabel: { color: '#98a4c6', rotate: 30, interval: 0 },
    splitArea: { show: true, areaStyle: { color: ['rgba(10, 13, 22, 0.46)', 'rgba(13, 17, 28, 0.64)'] } },
  },
  yAxis: {
    type: 'category',
    data: shortLabels.value,
    axisLabel: { color: '#98a4c6', interval: 0 },
    splitArea: { show: true, areaStyle: { color: ['rgba(10, 13, 22, 0.46)', 'rgba(13, 17, 28, 0.64)'] } },
  },
  visualMap: {
    min: -1,
    max: 1,
    calculable: false,
    orient: 'horizontal',
    left: 'center',
    top: 18,
    textStyle: { color: '#98a4c6' },
    inRange: {
      color: ['#ff8aa1', '#1c2436', '#6fe0b7'],
    },
  },
  series: [
    {
      name: '特性相关性',
      type: 'heatmap',
      data: props.data.cooccurrence.cells.map((cell) => ({
        value: [cell.x_index, cell.y_index, cell.correlation],
        cooccurrence: cell.cooccurrence,
        support_x: cell.support_x,
        support_y: cell.support_y,
      })),
      emphasis: {
        itemStyle: {
          borderColor: '#edf2ff',
          borderWidth: 1,
        },
      },
      progressive: 0,
      animation: false,
    },
  ],
}))
</script>

<template>
  <PanelCard
    eyebrow="关联"
    title="特性共现矩阵"
    description="相关性根据语言间 0-5 的特性评分计算，悬停提示还显示有多少语言同时包含两种特性。"
  >
    <div class="stack">
      <div class="mini-grid">
        <div
          v-for="pair in data.cooccurrence.top_pairs.slice(0, 4)"
          :key="`${pair.feature_a}-${pair.feature_b}`"
          class="mini-card"
        >
          <strong>
            {{ data.feature_short_labels[pair.feature_a] }} + {{ data.feature_short_labels[pair.feature_b] }}
          </strong>
          <span>
            {{ pair.label_a }} 和 {{ pair.label_b }} 协同变化，相关性为 {{ pair.correlation.toFixed(2) }}，
            跨越 {{ pair.cooccurrence }} 种共同语言。
          </span>
        </div>
      </div>

      <div v-if="mostCommonFeature" class="legend-row">
        <span class="legend-chip">
          最广泛特性：
          <strong>{{ mostCommonFeature.short }}</strong>
          存在于 {{ mostCommonFeature.count }} 种语言中
        </span>
        <span class="legend-chip">
          使用对角线读取原始支持度，然后扫描非对角线块以发现强配对。
        </span>
      </div>

      <EChartPanel :option="chartOption" />
    </div>
  </PanelCard>
</template>
