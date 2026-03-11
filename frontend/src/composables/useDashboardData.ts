import { computed } from 'vue'
import { useFetch } from '@vueuse/core'
import type { DashboardData } from '../types/dashboard'

export function useDashboardData() {
  const { data, error, isFetching, isFinished } = useFetch('/dashboard-data.json')
    .get()
    .json<DashboardData>()

  return {
    data: computed(() => data.value ?? null),
    error,
    isFetching,
    isFinished,
  }
}
