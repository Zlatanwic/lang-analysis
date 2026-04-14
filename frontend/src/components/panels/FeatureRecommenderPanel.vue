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
    eyebrow="配置"
    title="交互式特性推荐器"
    description="将数据集转换为配置工具：选择您关心的特性，并呈现最匹配的语言。"
  >
    <template #actions>
      <select v-model="domainFilter" class="control">
        <option value="__all__">所有领域组</option>
        <option
          v-for="group in domainGroups"
          :key="group"
          :value="group"
        >
          {{ group }}
        </option>
      </select>
      <label class="tag">
        最低评分
        <input v-model="threshold" type="range" min="1" max="5" />
        {{ threshold }}
      </label>
      <button class="ghost-button" @click="reset">
        清空
      </button>
    </template>

    <div class="stack">
      <div class="mini-grid">
        <div class="mini-card">
          <strong>{{ best ? `最佳匹配：${best.language.name}` : '选择特性开始' }}</strong>
          <span>
            {{
              best
                ? `${best.matched.length} / ${selectedFeatures.length || 1} 个所选需求满足阈值。`
                : '未选择特性时，此面板的行为类似于排名浏览器。'
            }}
          </span>
        </div>
        <div class="mini-card">
          <strong>已选特性</strong>
          <span>{{ selectedFeatures.length ? selectedFeatures.map((feature) => data.feature_short_labels[feature]).join(', ') : '尚无' }}</span>
        </div>
        <div class="mini-card">
          <strong>可见切片</strong>
          <span>{{ domainFilter === '__all__' ? '所有领域组' : domainFilter }}</span>
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
        在上方选择一个或多个特性，将其转换为硬过滤推荐器，而非被动排名。
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
            推荐评分：{{ entry.score.toFixed(1) }} / 总复杂度：{{ entry.language.complexity }}
          </div>

          <div class="stack" style="margin-top: 12px;">
            <div>
              <strong>匹配</strong>
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
                  尚无特性满足阈值
                </span>
              </div>
            </div>

            <div>
              <strong>缺失或薄弱</strong>
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
                  所有所选需求均已覆盖
                </span>
              </div>
            </div>
          </div>
        </article>
      </div>
    </div>
  </PanelCard>
</template>
