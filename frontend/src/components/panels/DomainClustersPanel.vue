<script setup lang="ts">
import { computed, ref } from 'vue'
import type { EChartsOption } from 'echarts'
import PanelCard from '../PanelCard.vue'
import EChartPanel from '../EChartPanel.vue'
import type { DashboardData } from '../../types/dashboard'
import { clusterPalette, domainGroupColors, domainGroupSymbols } from '../../constants'

const props = defineProps<{
  data: DashboardData
}>()

const showLabels = ref(true)

const domainGroups = computed(() => [...new Set(props.data.clusters.points.map((point) => point.domain_group))])
const clusterLabels = props.data.clusters.cluster_labels as Record<string, string>

const chartOption = computed<EChartsOption>(() => {
  const clusters = [...new Set(props.data.clusters.points.map((point) => point.cluster))].sort((a, b) => a - b)

  return {
    tooltip: {
      formatter: (params: any) =>
        `<b>${params.data.name}</b><br>${params.data.cluster_label}<br>${params.data.domain}<br>复杂度：${params.data.value?.[2]}`,
    },
    legend: {
      bottom: 0,
      textStyle: { color: '#98a4c6' },
    },
    grid: { left: 62, right: 30, top: 24, bottom: 70 },
    xAxis: {
      type: 'value',
      name: '主成分 1',
      axisLabel: { color: '#98a4c6' },
      splitLine: { lineStyle: { color: '#27314b' } },
    },
    yAxis: {
      type: 'value',
      name: '主成分 2',
      axisLabel: { color: '#98a4c6' },
      splitLine: { lineStyle: { color: '#27314b' } },
    },
    series: clusters.map((cluster) => ({
      name: clusterLabels[String(cluster)] ?? `聚类 ${cluster + 1}`,
      type: 'scatter',
      label: {
        show: showLabels.value,
        formatter: (params: any) => params.data.name,
        position: 'top',
        color: '#c7d0ea',
        fontSize: 10,
      },
      data: props.data.clusters.points
        .filter((point) => point.cluster === cluster)
        .map((point) => ({
          value: [point.x, point.y, point.complexity],
          name: point.name,
          domain: point.domain,
          cluster_label: point.cluster_label,
          symbol: domainGroupSymbols[point.domain_group] ?? 'circle',
          symbolSize: Math.max(12, point.complexity / 2),
          itemStyle: { color: clusterPalette[cluster % clusterPalette.length] },
        })),
    })),
  } as EChartsOption
})
</script>

<template>
  <PanelCard
    eyebrow="聚类"
    title="领域聚类"
    description="K-means 根据完整特征向量对语言进行分组，然后通过 PCA 将空间压缩成可读的散点图。"
  >
    <template #actions>
      <button class="ghost-button" @click="showLabels = !showLabels">
        {{ showLabels ? '隐藏标签' : '显示标签' }}
      </button>
    </template>

    <div class="stack">
      <div class="mini-grid">
        <div
          v-for="cluster in [0, 1, 2]"
          :key="cluster"
          class="mini-card"
        >
          <strong>{{ clusterLabels[String(cluster)] }}</strong>
          <span>{{ data.clusters.points.filter((point) => point.cluster === cluster).length }} 种语言</span>
        </div>
      </div>

      <div class="legend-row">
        <span
          v-for="group in domainGroups"
          :key="group"
          class="legend-chip"
        >
          <span
            style="width: 10px; height: 10px; border-radius: 999px; display: inline-block"
            :style="{ background: domainGroupColors[group] ?? '#98a4c6' }"
          />
          {{ group }}
        </span>
      </div>

      <EChartPanel :option="chartOption" />
    </div>
  </PanelCard>
</template>
