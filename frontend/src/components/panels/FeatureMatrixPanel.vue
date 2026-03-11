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
  return `rgba(126, 150, 255, ${alpha.toFixed(3)})`
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
    title="Feature Matrix"
    description="The matrix stays compact by default. Long feature names and scoring rationale only surface inside the hover card."
  >
    <div class="stack">
      <div class="toolbar">
        <div class="toolbar-copy">
          {{ data.heatmap.length }} languages, {{ data.features.length }} scored type-system dimensions, and a sticky score rail so dense comparisons stay readable.
        </div>
        <div class="toolbar-group">
          <div class="mini-card">
            <strong>{{ topLanguage?.name }}</strong>
            <span>Highest total complexity: {{ topLanguage?.complexity }}</span>
          </div>
          <div class="mini-card">
            <strong>{{ data.max_score }}</strong>
            <span>Maximum theoretical score</span>
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
                  <strong>Language</strong>
                  <small>Year / paradigm / domain</small>
                </div>
              </th>
              <th
                v-for="feature in data.features"
                :key="feature"
                class="sticky-top"
              >
                <div
                  class="matrix-card matrix-header-card"
                  @mouseenter="showTooltip($event, data.feature_labels[feature], 'Compact header shown by default so long feature names never flood the table.')"
                  @mousemove="moveTooltip"
                  @mouseleave="hideTooltip"
                >
                  <strong>{{ data.feature_short_labels[feature] }}</strong>
                  <small>#{{ data.features.indexOf(feature) + 1 }}</small>
                </div>
              </th>
              <th class="sticky-top sticky-right">
                <div class="matrix-card matrix-score">
                  <strong>Total</strong>
                  <small>Complexity</small>
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
                  @mouseenter="showTooltip($event, `${language.name} - ${data.feature_labels[feature]}`, language.rationale[feature] || 'No detailed rationale was provided for this score.')"
                  @mousemove="moveTooltip"
                  @mouseleave="hideTooltip"
                >
                  {{ language.scores[index] }}
                </div>
              </td>
              <td class="sticky-right">
                <div class="matrix-card matrix-score">
                  <strong>{{ language.complexity }}</strong>
                  <small>{{ (language.complexity / data.max_score).toFixed(2) }} of max</small>
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
