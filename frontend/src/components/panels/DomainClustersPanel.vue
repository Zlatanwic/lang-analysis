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
const domainFilter = ref<string[]>()

const domainGroups = computed(() => [...new Set(props.data.clusters.points.map((point) => point.domain_group))])
const clusterLabels = props.data.clusters.cluster_labels as Record<string, string>

const filteredPoints = computed(() => {
  if (!domainFilter.value || domainFilter.value.length === 0) return props.data.clusters.points
  return props.data.clusters.points.filter((point) => !domainFilter.value!.includes(point.domain_group))
})

const chartOption = computed<EChartsOption>(() => {
  const clusters = [...new Set(filteredPoints.value.map((point) => point.cluster))].sort((a, b) => a - b)

  return {
    tooltip: {
      formatter: (params: any) =>
        `<b>${params.data.name}</b><br>${params.data.cluster_label}<br>${params.data.domain}<br>复杂度：${params.data.value?.[2]}`,
    },
    legend: {
      bottom: 0,
      textStyle: { color: '#3A5A47' },
    },
    grid: { left: 62, right: 30, top: 24, bottom: 70 },
    xAxis: {
      type: 'value',
      name: '主成分 1',
      axisLabel: { color: '#3A5A47' },
      splitLine: { lineStyle: { color: '#C4C2B6' } },
    },
    yAxis: {
      type: 'value',
      name: '主成分 2',
      axisLabel: { color: '#3A5A47' },
      splitLine: { lineStyle: { color: '#C4C2B6' } },
    },
    series: clusters.map((cluster) => ({
      name: clusterLabels[String(cluster)] ?? `聚类 ${cluster + 1}`,
      type: 'scatter',
      label: {
        show: showLabels.value,
        formatter: (params: any) => params.data.name,
        position: 'top',
        color: '#3D5142',
        fontSize: 10,
      },
      data: filteredPoints.value
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

function toggleDomain(domain: string) {
  if (!domainFilter.value) {
    // Nothing hidden yet - hide this domain
    domainFilter.value = [domain]
  } else if (domainFilter.value.includes(domain)) {
    // This domain is hidden - show it
    domainFilter.value = domainFilter.value.filter((d) => d !== domain)
  } else {
    // This domain is visible - hide it
    domainFilter.value = [...domainFilter.value, domain]
  }
}

function resetDomains() {
  domainFilter.value = undefined
}
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
      <button class="ghost-button" @click="resetDomains">
        重置领域
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
          <span>{{ filteredPoints.filter((point) => point.cluster === cluster).length }} 种语言</span>
        </div>
      </div>

      <div class="legend-row">
        <button
          v-for="group in domainGroups"
          :key="group"
          class="legend-chip clickable"
          :class="{ inactive: domainFilter?.includes(group) }"
          @click="toggleDomain(group)"
        >
          <span
            style="width: 10px; height: 10px; border-radius: 999px; display: inline-block"
            :style="{ background: domainGroupColors[group] ?? '#3A5A47', opacity: domainFilter?.includes(group) ? 0.3 : 1 }"
          />
          {{ group }}
        </button>
      </div>

      <EChartPanel :option="chartOption" />
    </div>
  </PanelCard>
</template>
