import { computed } from 'vue'
import { useFetch } from '@vueuse/core'
import type { DashboardData } from '../types/dashboard'

export function useDashboardData() {
  const dataUrl = new URL('dashboard-data.json', import.meta.env.BASE_URL).toString()
  const { data, error, isFetching, isFinished } = useFetch(dataUrl)
    .get()
    .json<DashboardData>()

  return {
    data: computed(() => data.value ?? null),
    error,
    isFetching,
    isFinished,
  }
}
