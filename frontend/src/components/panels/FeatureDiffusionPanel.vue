<script setup lang="ts">
import { computed, ref } from 'vue'
import { useIntervalFn } from '@vueuse/core'
import type { EChartsOption } from 'echarts'
import PanelCard from '../PanelCard.vue'
import EChartPanel from '../EChartPanel.vue'
import type { DashboardData } from '../../types/dashboard'

const props = defineProps<{
  data: DashboardData
}>()

const selectedFeature = ref(props.data.diffusion.default_feature)
const progress = ref(props.data.diffusion.features[selectedFeature.value].events.length)

const featureData = computed(() => props.data.diffusion.features[selectedFeature.value])
const visibleEvents = computed(() => featureData.value.events.slice(0, progress.value))

const { pause, resume, isActive } = useIntervalFn(() => {
  progress.value += 1
  if (progress.value >= featureData.value.events.length) {
    pause()
  }
}, 850, { immediate: false })

function onFeatureChange() {
  pause()
  progress.value = featureData.value.events.length
}

function togglePlay() {
  if (isActive.value) {
    pause()
    return
  }
  progress.value = 1
  resume()
}

const chartOption = computed<EChartsOption>(() => {
  const events = featureData.value.events
  const lastEvent = visibleEvents.value[visibleEvents.value.length - 1]

  return {
    title: {
      text: featureData.value.label,
      left: 12,
      top: 10,
      textStyle: { color: '#1D3124', fontSize: 14 },
      subtext: lastEvent
        ? `可见 ${visibleEvents.value.length}/${events.length} - 最新揭示 ${lastEvent.language} (${lastEvent.year})`
        : '尚无可见事件',
      subtextStyle: { color: '#3A5A47' },
    },
    tooltip: {
      formatter: (params: any) => {
        const event = params.data.meta
        return `<b>${event.language}</b><br>年份：${event.year}<br>评分：${event.score}/5<br>领域：${event.domain}`
      },
    },
    grid: { left: 120, right: 36, top: 72, bottom: 56 },
    xAxis: {
      type: 'value',
      min: Math.min(...events.map((event) => event.year)) - 1,
      max: Math.max(...events.map((event) => event.year)) + 1,
      axisLabel: { color: '#3A5A47' },
      splitLine: { lineStyle: { color: '#C4C2B6' } },
    },
    yAxis: {
      type: 'category',
      data: events.map((event) => event.language),
      axisLabel: { color: '#1D3124', fontSize: 11 },
      splitLine: { lineStyle: { color: '#D4D2C6' } },
    },
    series: [
      {
        type: 'line',
        data: visibleEvents.value.map((event) => ({
          value: [event.year, event.language],
          meta: event,
        })),
        symbolSize: 10,
        lineStyle: { color: '#7e96ff', width: 3 },
        itemStyle: { color: '#7e96ff' },
      },
      {
        type: 'effectScatter',
        data: lastEvent
          ? [{ value: [lastEvent.year, lastEvent.language], meta: lastEvent }]
          : [],
        symbolSize: 16,
        rippleEffect: { scale: 3, brushType: 'stroke' },
        itemStyle: { color: '#ff8aa1' },
      },
    ],
  } as EChartsOption
})
</script>

<template>
  <PanelCard
    eyebrow="追溯"
    title="特性扩散"
    description="选择一个特性并浏览其采用路径，从最早的谱系根源到后期的主流采用。"
  >
    <template #actions>
      <select v-model="selectedFeature" class="control" @change="onFeatureChange">
        <option
          v-for="[feature, value] in Object.entries(data.diffusion.features)"
          :key="feature"
          :value="feature"
        >
          {{ value.label }}
        </option>
      </select>
      <button class="ghost-button" @click="togglePlay">
        {{ isActive ? '暂停' : '播放' }}
      </button>
    </template>

    <div class="stack">
      <div class="mini-grid">
        <div class="mini-card">
          <strong>起源</strong>
          <span>{{ featureData.events[0]?.language }} ({{ featureData.events[0]?.year }})</span>
        </div>
        <div class="mini-card">
          <strong>覆盖</strong>
          <span>可见 {{ visibleEvents.length }} / {{ featureData.events.length }}</span>
        </div>
        <div class="mini-card">
          <strong>领域分布</strong>
          <span>{{ [...new Set(visibleEvents.map((event) => event.domain_group))].join(', ') || '尚无领域数据' }}</span>
        </div>
      </div>

      <div class="toolbar">
        <div class="toolbar-copy">
          进度是交互式的，您可以播放采用路径或直接拖动到特定揭示步骤。
        </div>
        <div class="toolbar-group">
          <input
            v-model="progress"
            type="range"
            min="1"
            :max="featureData.events.length"
          />
          <span class="tag">{{ progress }} / {{ featureData.events.length }}</span>
        </div>
      </div>

      <EChartPanel :option="chartOption" />
    </div>
  </PanelCard>
</template>
