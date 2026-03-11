<script setup lang="ts">
import { computed, ref } from 'vue'
import PanelCard from '../PanelCard.vue'
import type { DashboardData } from '../../types/dashboard'

const props = defineProps<{
  data: DashboardData
}>()

const selectedFeatures = ref<string[]>([])
const threshold = ref(3)
const domainFilter = ref('__all__')

const domainGroups = computed(() =>
  [...new Set(props.data.heatmap.map((language) => language.domain.split(' / ')[0]))].sort(),
)

const filteredLanguages = computed(() => {
  return props.data.heatmap.filter((language) => {
    const group = language.domain.split(' / ')[0]
    return domainFilter.value === '__all__' || group === domainFilter.value
  })
})

const ranked = computed(() => {
  return filteredLanguages.value
    .map((language) => {
      const matched = selectedFeatures.value.filter((feature) => {
        const index = props.data.features.indexOf(feature)
        return language.scores[index] >= threshold.value
      })
      const missing = selectedFeatures.value.filter((feature) => !matched.includes(feature))
      const score =
        matched.length * 12 +
        missing.reduce((acc, feature) => {
          const index = props.data.features.indexOf(feature)
          return acc + language.scores[index]
        }, 0) +
        language.complexity / 10

      return {
        language,
        matched,
        missing,
        score,
      }
    })
    .sort((a, b) => {
      if (b.matched.length !== a.matched.length) return b.matched.length - a.matched.length
      return b.score - a.score
    })
})

const best = computed(() => ranked.value[0] ?? null)

function toggleFeature(feature: string) {
  if (selectedFeatures.value.includes(feature)) {
    selectedFeatures.value = selectedFeatures.value.filter((item) => item !== feature)
    return
  }
  selectedFeatures.value = [...selectedFeatures.value, feature]
}

function reset() {
  selectedFeatures.value = []
  threshold.value = 3
  domainFilter.value = '__all__'
}
</script>

<template>
  <PanelCard
    eyebrow="Configure"
    title="Interactive Feature Recommender"
    description="Turn the dataset into a configuration tool: select the capabilities you care about and surface the closest language matches."
  >
    <template #actions>
      <select v-model="domainFilter" class="control">
        <option value="__all__">All domain groups</option>
        <option
          v-for="group in domainGroups"
          :key="group"
          :value="group"
        >
          {{ group }}
        </option>
      </select>
      <label class="tag">
        Min score
        <input v-model="threshold" type="range" min="1" max="5" />
        {{ threshold }}
      </label>
      <button class="ghost-button" @click="reset">
        Clear
      </button>
    </template>

    <div class="stack">
      <div class="mini-grid">
        <div class="mini-card">
          <strong>{{ best ? `Best match: ${best.language.name}` : 'Choose features to start' }}</strong>
          <span>
            {{
              best
                ? `${best.matched.length} of ${selectedFeatures.length || 1} selected requirements meet the threshold.`
                : 'Without selected features this panel behaves like a ranked browser.'
            }}
          </span>
        </div>
        <div class="mini-card">
          <strong>Selected features</strong>
          <span>{{ selectedFeatures.length ? selectedFeatures.map((feature) => data.feature_short_labels[feature]).join(', ') : 'None yet' }}</span>
        </div>
        <div class="mini-card">
          <strong>Visible slice</strong>
          <span>{{ domainFilter === '__all__' ? 'All domain groups' : domainFilter }}</span>
        </div>
      </div>

      <div class="chip-list">
        <button
          v-for="feature in data.features"
          :key="feature"
          class="feature-toggle"
          :class="{ active: selectedFeatures.includes(feature) }"
          @click="toggleFeature(feature)"
        >
          <strong>{{ data.feature_short_labels[feature] }}</strong>
          <small>{{ data.feature_labels[feature] }}</small>
        </button>
      </div>

      <div
        v-if="!selectedFeatures.length"
        class="empty-state"
      >
        Pick one or more features above to turn this into a hard-filter recommender instead of a passive ranking.
      </div>

      <div class="recommendation-grid">
        <article
          v-for="entry in ranked.slice(0, 8)"
          :key="entry.language.name"
          class="recommendation-card"
        >
          <div class="recommendation-head">
            <div>
              <h3>{{ entry.language.name }}</h3>
              <div class="recommendation-meta">
                {{ entry.language.year }} / {{ entry.language.paradigm }} / {{ entry.language.domain }}
              </div>
            </div>
            <strong>{{ entry.matched.length }}/{{ selectedFeatures.length || 1 }}</strong>
          </div>
          <div class="recommendation-meta">
            Recommendation score: {{ entry.score.toFixed(1) }} / Total complexity: {{ entry.language.complexity }}
          </div>

          <div class="stack" style="margin-top: 12px;">
            <div>
              <strong>Matches</strong>
              <div class="recommendation-tags" style="margin-top: 8px;">
                <span
                  v-for="feature in entry.matched"
                  :key="feature"
                  class="recommendation-tag match"
                >
                  {{ data.feature_short_labels[feature] }}
                </span>
                <span
                  v-if="!entry.matched.length"
                  class="recommendation-tag missing"
                >
                  No features meet the threshold yet
                </span>
              </div>
            </div>

            <div>
              <strong>Missing or weak</strong>
              <div class="recommendation-tags" style="margin-top: 8px;">
                <span
                  v-for="feature in entry.missing"
                  :key="feature"
                  class="recommendation-tag missing"
                >
                  {{ data.feature_short_labels[feature] }}
                </span>
                <span
                  v-if="!entry.missing.length"
                  class="recommendation-tag match"
                >
                  All selected requirements are covered
                </span>
              </div>
            </div>
          </div>
        </article>
      </div>
    </div>
  </PanelCard>
</template>
