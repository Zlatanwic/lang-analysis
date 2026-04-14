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
  { key: 'matrix', label: '特性矩阵', kicker: '对比', summary: '用于深入对比编程语言的密集计分卡。' },
  { key: 'cooccurrence', label: '特性共现', kicker: '关联', summary: '查看哪些特性在语言集合中始终相互强化。' },
  { key: 'radar', label: '雷达图', kicker: '轮廓', summary: '对比精选小集合的整体类型系统特征。' },
  { key: 'timeline', label: '时间线', kicker: '序列', summary: '查看特定特性何时出现以及特性时代如何重叠。' },
  { key: 'arms-race', label: '军备竞赛指数', kicker: '加速', summary: '汇总年度特性引入情况，揭示类型系统复杂度的累积速度。' },
  { key: 'network', label: '相似性网络', kicker: '映射', summary: '基于共享特性向量揭示语言亲疏关系。' },
  { key: 'popularity', label: '流行度', kicker: '信号', summary: '平衡类型复杂度与生态系统关注度和可见度。' },
  { key: 'diffusion', label: '特性扩散', kicker: '追溯', summary: '追踪单一特性如何跨越领域和语言家族传播。' },
  { key: 'clusters', label: '领域聚类', kicker: '聚类', summary: '将特性配置文件投射到可揭示隐藏亲和性的分组中。' },
  { key: 'lineage', label: '谱系图', kicker: '谱系', summary: '追踪从研究根源到现代语言的影响路径。' },
  { key: 'recommender', label: '推荐器', kicker: '配置', summary: '将数据集转换为由实际约束驱动的语言选择器。' },
] as const

const activeTab = useLocalStorage<(typeof tabs)[number]['key']>('dashboard-active-tab', 'matrix')
const activeTabMeta = computed(() => tabs.find((tab) => tab.key === activeTab.value) ?? tabs[0])

const topStats = computed(() => {
  if (!data.value) return []
  return [
    { label: '语言', value: data.value.heatmap.length },
    { label: '特性维度', value: data.value.features.length },
    { label: '相似性边', value: data.value.network.edges.length },
    { label: '谱系链接', value: data.value.lineage.edges.length },
  ]
})
</script>

<template>
  <main class="app-shell">
    <section class="hero">
      <span class="hero-eyebrow">Vue 仪表盘重构</span>
      <div class="hero-grid">
        <div class="hero-copy">
          <h1>编程语言类型系统知识图谱</h1>
          <p>
            通过 Vue 驱动的分析仪表盘，探索高级类型系统特性如何聚集、扩散并塑造语言设计。
          </p>

          <div class="hero-support">
            <span class="info-pill">Vue 3 界面</span>
            <span class="info-pill">Python 数据管道</span>
            <span class="info-pill">GitHub Pages 部署</span>
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
            <span class="hero-focus-kicker">当前视角</span>
            <strong>{{ activeTabMeta.label }}</strong>
            <p>{{ activeTabMeta.summary }}</p>
          </div>
          <div class="hero-focus-card subtle">
            <span class="hero-focus-kicker">阅读模式</span>
            <strong>{{ activeTabMeta.kicker }}</strong>
            <p>每个面板都针对不同的分析风格进行了调优，从密集对比到探索性图表阅读。</p>
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
      正在加载仪表盘数据...
    </div>
    <div v-else-if="error" class="error">
      加载 <code>dashboard-data.json</code> 失败。请运行 <code>python main.py --json-output frontend/public/dashboard-data.json</code> 并刷新。
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
