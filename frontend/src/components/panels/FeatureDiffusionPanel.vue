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
      textStyle: { color: '#edf2ff', fontSize: 14 },
      subtext: lastEvent
        ? `Visible ${visibleEvents.value.length}/${events.length} - latest reveal ${lastEvent.language} (${lastEvent.year})`
        : 'No visible events yet',
      subtextStyle: { color: '#98a4c6' },
    },
    tooltip: {
      formatter: (params: any) => {
        const event = params.data.meta
        return `<b>${event.language}</b><br>Year: ${event.year}<br>Score: ${event.score}/5<br>Domain: ${event.domain}`
      },
    },
    grid: { left: 120, right: 36, top: 72, bottom: 56 },
    xAxis: {
      type: 'value',
      min: Math.min(...events.map((event) => event.year)) - 1,
      max: Math.max(...events.map((event) => event.year)) + 1,
      axisLabel: { color: '#98a4c6' },
      splitLine: { lineStyle: { color: '#27314b' } },
    },
    yAxis: {
      type: 'category',
      data: events.map((event) => event.language),
      axisLabel: { color: '#edf2ff', fontSize: 11 },
      splitLine: { lineStyle: { color: '#182033' } },
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
    eyebrow="Trace"
    title="Feature Diffusion"
    description="Pick a capability and scrub through its adoption path, from earliest lineage roots to later mainstream uptake."
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
        {{ isActive ? 'Pause' : 'Play' }}
      </button>
    </template>

    <div class="stack">
      <div class="mini-grid">
        <div class="mini-card">
          <strong>Origin</strong>
          <span>{{ featureData.events[0]?.language }} ({{ featureData.events[0]?.year }})</span>
        </div>
        <div class="mini-card">
          <strong>Coverage</strong>
          <span>{{ visibleEvents.length }} of {{ featureData.events.length }} visible</span>
        </div>
        <div class="mini-card">
          <strong>Domain spread</strong>
          <span>{{ [...new Set(visibleEvents.map((event) => event.domain_group))].join(', ') || 'No domains yet' }}</span>
        </div>
      </div>

      <div class="toolbar">
        <div class="toolbar-copy">
          Progress is interactive, so you can either play the adoption path or drag directly to a specific reveal step.
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
