<script setup lang="ts">
import { computed } from 'vue'
import { useLocalStorage } from '@vueuse/core'
import { useDashboardData } from './composables/useDashboardData'
import FeatureMatrixPanel from './components/panels/FeatureMatrixPanel.vue'
import FeatureCooccurrencePanel from './components/panels/FeatureCooccurrencePanel.vue'
import RadarComparisonPanel from './components/panels/RadarComparisonPanel.vue'
import FeatureTimelinePanel from './components/panels/FeatureTimelinePanel.vue'
import ArmsRacePanel from './components/panels/ArmsRacePanel.vue'
import SimilarityNetworkPanel from './components/panels/SimilarityNetworkPanel.vue'
import PopularityAnalysisPanel from './components/panels/PopularityAnalysisPanel.vue'
import FeatureDiffusionPanel from './components/panels/FeatureDiffusionPanel.vue'
import DomainClustersPanel from './components/panels/DomainClustersPanel.vue'
import LineageGraphPanel from './components/panels/LineageGraphPanel.vue'
import FeatureRecommenderPanel from './components/panels/FeatureRecommenderPanel.vue'

const { data, error, isFetching } = useDashboardData()

const tabs = [
  { key: 'matrix', label: 'Feature Matrix', kicker: 'Compare', summary: 'Dense scorecard for deep side-by-side language comparison.' },
  { key: 'cooccurrence', label: 'Feature Co-occurrence', kicker: 'Correlate', summary: 'See which capabilities consistently reinforce each other across the language set.' },
  { key: 'radar', label: 'Radar', kicker: 'Shape', summary: 'Contrast overall type-system profiles across a small hand-picked set.' },
  { key: 'timeline', label: 'Timeline', kicker: 'Sequence', summary: 'See when specific capabilities appeared and how feature eras overlapped.' },
  { key: 'arms-race', label: 'Arms Race Index', kicker: 'Accelerate', summary: 'Aggregate yearly feature arrivals to reveal how fast type-system complexity compounds.' },
  { key: 'network', label: 'Similarity Network', kicker: 'Map', summary: 'Reveal language neighborhoods based on shared feature vectors.' },
  { key: 'popularity', label: 'Popularity', kicker: 'Signal', summary: 'Balance type complexity against ecosystem interest and visibility.' },
  { key: 'diffusion', label: 'Feature Diffusion', kicker: 'Trace', summary: 'Follow one capability as it spreads across domains and families.' },
  { key: 'clusters', label: 'Domain Clusters', kicker: 'Cluster', summary: 'Project feature profiles into groups that expose hidden affinities.' },
  { key: 'lineage', label: 'Lineage Graph', kicker: 'Lineage', summary: 'Track influence paths between research roots and modern languages.' },
  { key: 'recommender', label: 'Recommender', kicker: 'Configure', summary: 'Turn the dataset into a language chooser driven by actual constraints.' },
] as const

const activeTab = useLocalStorage<(typeof tabs)[number]['key']>('dashboard-active-tab', 'matrix')
const activeTabMeta = computed(() => tabs.find((tab) => tab.key === activeTab.value) ?? tabs[0])

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
      <div class="hero-grid">
        <div class="hero-copy">
          <h1>Programming Language Type System Knowledge Graph</h1>
          <p>
            Explore how advanced type-system capabilities cluster, diffuse, and shape language design through a Vue-driven analytical dashboard.
          </p>

          <div class="hero-support">
            <span class="info-pill">Vue 3 interface</span>
            <span class="info-pill">Python data pipeline</span>
            <span class="info-pill">GitHub Pages deployed</span>
          </div>

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
        </div>

        <aside class="hero-side">
          <div class="hero-focus-card">
            <span class="hero-focus-kicker">Current lens</span>
            <strong>{{ activeTabMeta.label }}</strong>
            <p>{{ activeTabMeta.summary }}</p>
          </div>
          <div class="hero-focus-card subtle">
            <span class="hero-focus-kicker">Reading mode</span>
            <strong>{{ activeTabMeta.kicker }}</strong>
            <p>Each panel is tuned for a different analysis style, from dense comparison to exploratory graph reading.</p>
          </div>
        </aside>
      </div>
    </section>

    <section class="view-rail">
      <div class="tab-row">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          class="tab-button"
          :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key"
        >
          <small>{{ tab.kicker }}</small>
          <span>{{ tab.label }}</span>
        </button>
      </div>

      <div class="view-context">
        <span class="view-context-kicker">{{ activeTabMeta.kicker }}</span>
        <strong>{{ activeTabMeta.label }}</strong>
        <p>{{ activeTabMeta.summary }}</p>
      </div>
    </section>

    <div v-if="isFetching && !data" class="loading">
      Loading dashboard data...
    </div>
    <div v-else-if="error" class="error">
      Failed to load <code>dashboard-data.json</code>. Run <code>python main.py --json-output frontend/public/dashboard-data.json</code> and refresh.
    </div>
    <template v-else-if="data">
      <FeatureMatrixPanel v-if="activeTab === 'matrix'" :data="data" />
      <FeatureCooccurrencePanel v-else-if="activeTab === 'cooccurrence'" :data="data" />
      <RadarComparisonPanel v-else-if="activeTab === 'radar'" :data="data" />
      <FeatureTimelinePanel v-else-if="activeTab === 'timeline'" :data="data" />
      <ArmsRacePanel v-else-if="activeTab === 'arms-race'" :data="data" />
      <SimilarityNetworkPanel v-else-if="activeTab === 'network'" :data="data" />
      <PopularityAnalysisPanel v-else-if="activeTab === 'popularity'" :data="data" />
      <FeatureDiffusionPanel v-else-if="activeTab === 'diffusion'" :data="data" />
      <DomainClustersPanel v-else-if="activeTab === 'clusters'" :data="data" />
      <LineageGraphPanel v-else-if="activeTab === 'lineage'" :data="data" />
      <FeatureRecommenderPanel v-else-if="activeTab === 'recommender'" :data="data" />
    </template>
  </main>
</template>
