<script setup lang="ts">
import { reactive } from 'vue'
import PanelCard from '../PanelCard.vue'
import type { DashboardData } from '../../types/dashboard'

const props = defineProps<{
  data: DashboardData
}>()

const tooltip = reactive({
  visible: false,
  x: 0,
  y: 0,
  title: '',
  body: '',
})

function colorFor(score: number, max: number) {
  const alpha = 0.16 + (score / Math.max(max, 1)) * 0.8
  return `rgba(159, 232, 112, ${alpha.toFixed(3)})`
}

function showTooltip(event: MouseEvent, title: string, body: string) {
  tooltip.visible = true
  tooltip.x = event.clientX + 14
  tooltip.y = event.clientY + 14
  tooltip.title = title
  tooltip.body = body
}

function moveTooltip(event: MouseEvent) {
  tooltip.x = event.clientX + 14
  tooltip.y = event.clientY + 14
}

function hideTooltip() {
  tooltip.visible = false
}

const topLanguage = props.data.heatmap[0]
</script>

<template>
  <PanelCard
    eyebrow="对比"
    title="特性矩阵"
    description="矩阵默认保持紧凑。较长的特性名称和评分理由仅在悬停卡片中显示。"
  >
    <div class="stack">
      <div class="toolbar">
        <div class="toolbar-copy">
          {{ data.heatmap.length }} 种语言，{{ data.features.length }} 个评分类型系统维度，以及固定分数轨道，使密集对比保持可读性。
        </div>
        <div class="toolbar-group">
          <div class="mini-card">
            <strong>{{ topLanguage?.name }}</strong>
            <span>最高总复杂度：{{ topLanguage?.complexity }}</span>
          </div>
          <div class="mini-card">
            <strong>{{ data.max_score }}</strong>
            <span>最大理论得分</span>
          </div>
        </div>
      </div>

      <div class="pill-grid">
        <div
          v-for="(copy, score) in data.scoring"
          :key="score"
          class="mini-card"
        >
          <strong>{{ score }} / {{ data.max_score }}</strong>
          <span>{{ copy }}</span>
        </div>
      </div>

      <div class="table-scroll">
        <table class="table-matrix">
          <thead>
            <tr>
              <th class="sticky-top sticky-left">
                <div class="matrix-card matrix-label">
                  <strong>语言</strong>
                  <small>年份 / 范式 / 领域</small>
                </div>
              </th>
              <th
                v-for="feature in data.features"
                :key="feature"
                class="sticky-top"
              >
                <div
                  class="matrix-card matrix-header-card"
                  @mouseenter="showTooltip($event, data.feature_labels[feature], '默认显示紧凑表头，避免长特性名称淹没表格。')"
                  @mousemove="moveTooltip"
                  @mouseleave="hideTooltip"
                >
                  <strong>{{ data.feature_short_labels[feature] }}</strong>
                  <small>#{{ data.features.indexOf(feature) + 1 }}</small>
                </div>
              </th>
              <th class="sticky-top sticky-right">
                <div class="matrix-card matrix-score">
                  <strong>总计</strong>
                  <small>复杂度</small>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="language in data.heatmap"
              :key="language.name"
            >
              <td class="sticky-left">
                <div class="matrix-card matrix-label">
                  <strong>{{ language.name }}</strong>
                  <small>{{ language.year }} / {{ language.paradigm }} / {{ language.domain }}</small>
                </div>
              </td>
              <td
                v-for="(feature, index) in data.features"
                :key="`${language.name}-${feature}`"
              >
                <div
                  class="matrix-cell"
                  :style="{ background: colorFor(language.scores[index], data.max_score) }"
                  @mouseenter="showTooltip($event, `${language.name} - ${data.feature_labels[feature]}`, language.rationale[feature] || '此评分未提供详细理由。')"
                  @mousemove="moveTooltip"
                  @mouseleave="hideTooltip"
                >
                  {{ language.scores[index] }}
                </div>
              </td>
              <td class="sticky-right">
                <div class="matrix-card matrix-score">
                  <strong>{{ language.complexity }}</strong>
                  <small>{{ (language.complexity / data.max_score).toFixed(2) }} / 最大值</small>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <Teleport to="body">
      <div
        v-if="tooltip.visible"
        class="tooltip-card"
        :style="{ left: `${tooltip.x}px`, top: `${tooltip.y}px` }"
      >
        <strong>{{ tooltip.title }}</strong>
        <p>{{ tooltip.body }}</p>
      </div>
    </Teleport>
  </PanelCard>
</template>
