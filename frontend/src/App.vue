<script setup lang="ts">
import { computed } from 'vue'
import { useLocalStorage } from '@vueuse/core'
import { useDashboardData } from './composables/useDashboardData'
import FeatureMatrixPanel from './components/panels/FeatureMatrixPanel.vue'
import RadarComparisonPanel from './components/panels/RadarComparisonPanel.vue'
import FeatureTimelinePanel from './components/panels/FeatureTimelinePanel.vue'
import SimilarityNetworkPanel from './components/panels/SimilarityNetworkPanel.vue'
import PopularityAnalysisPanel from './components/panels/PopularityAnalysisPanel.vue'
import FeatureDiffusionPanel from './components/panels/FeatureDiffusionPanel.vue'
import DomainClustersPanel from './components/panels/DomainClustersPanel.vue'
import LineageGraphPanel from './components/panels/LineageGraphPanel.vue'
import FeatureRecommenderPanel from './components/panels/FeatureRecommenderPanel.vue'

const { data, error, isFetching } = useDashboardData()

const tabs = [
  { key: 'matrix', label: 'Feature Matrix' },
  { key: 'radar', label: 'Radar' },
  { key: 'timeline', label: 'Timeline' },
  { key: 'network', label: 'Similarity Network' },
  { key: 'popularity', label: 'Popularity' },
  { key: 'diffusion', label: 'Feature Diffusion' },
  { key: 'clusters', label: 'Domain Clusters' },
  { key: 'lineage', label: 'Lineage Graph' },
  { key: 'recommender', label: 'Recommender' },
] as const

const activeTab = useLocalStorage<(typeof tabs)[number]['key']>('dashboard-active-tab', 'matrix')

const topStats = computed(() => {
  if (!data.value) return []
  return [
    { label: 'Languages', value: data.value.heatmap.length },
    { label: 'Feature dimensions', value: data.value.features.length },
    { label: 'Similarity edges', value: data.value.network.edges.length },
    { label: 'Lineage links', value: data.value.lineage.edges.length },
  ]
})
</script>

<template>
  <main class="app-shell">
    <section class="hero">
      <span class="hero-eyebrow">Vue dashboard refactor</span>
      <h1>Programming Language Type System Knowledge Graph</h1>
      <p>
        The frontend is now organized as a Vue 3 application instead of a monolithic HTML string.
        Python prepares the dataset, Vue owns the interaction model, and every analytical surface now has a real component boundary.
      </p>

      <div class="top-stats">
        <div
          v-for="item in topStats"
          :key="item.label"
          class="stat-card"
        >
          <strong>{{ item.value }}</strong>
          <span>{{ item.label }}</span>
        </div>
      </div>
    </section>

    <div class="tab-row">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="tab-button"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <div v-if="isFetching && !data" class="loading">
      Loading dashboard data...
    </div>
    <div v-else-if="error" class="error">
      Failed to load <code>dashboard-data.json</code>. Run <code>python main.py --json-output frontend/public/dashboard-data.json</code> and refresh.
    </div>
    <template v-else-if="data">
      <FeatureMatrixPanel v-if="activeTab === 'matrix'" :data="data" />
      <RadarComparisonPanel v-else-if="activeTab === 'radar'" :data="data" />
      <FeatureTimelinePanel v-else-if="activeTab === 'timeline'" :data="data" />
      <SimilarityNetworkPanel v-else-if="activeTab === 'network'" :data="data" />
      <PopularityAnalysisPanel v-else-if="activeTab === 'popularity'" :data="data" />
      <FeatureDiffusionPanel v-else-if="activeTab === 'diffusion'" :data="data" />
      <DomainClustersPanel v-else-if="activeTab === 'clusters'" :data="data" />
      <LineageGraphPanel v-else-if="activeTab === 'lineage'" :data="data" />
      <FeatureRecommenderPanel v-else-if="activeTab === 'recommender'" :data="data" />
    </template>
  </main>
</template>
