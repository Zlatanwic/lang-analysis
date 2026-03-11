<script setup lang="ts">
import { onBeforeUnmount, onMounted, shallowRef, useTemplateRef, watch } from 'vue'
import { useResizeObserver } from '@vueuse/core'
import * as echarts from 'echarts'
import type { EChartsOption, EChartsType } from 'echarts'

const props = defineProps<{
  option: EChartsOption
  compact?: boolean
}>()

const root = useTemplateRef<HTMLDivElement>('root')
const chart = shallowRef<EChartsType | null>(null)

function renderChart(option: EChartsOption) {
  if (!chart.value) return
  chart.value.setOption(option, true)
}

onMounted(() => {
  if (!root.value) return
  chart.value = echarts.init(root.value)
  renderChart(props.option)
})

watch(
  () => props.option,
  (option) => {
    renderChart(option)
  },
  { deep: true },
)

useResizeObserver(root, () => {
  chart.value?.resize()
})

onBeforeUnmount(() => {
  chart.value?.dispose()
  chart.value = null
})
</script>

<template>
  <div ref="root" class="chart-shell" :class="{ compact }"></div>
</template>
