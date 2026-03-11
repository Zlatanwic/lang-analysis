import { computed } from 'vue'
import { useFetch } from '@vueuse/core'
import type { DashboardData } from '../types/dashboard'

export function useDashboardData() {
  const baseUrl = import.meta.env.BASE_URL.endsWith('/')
    ? import.meta.env.BASE_URL
    : `${import.meta.env.BASE_URL}/`
  const dataUrl = `${baseUrl}dashboard-data.json`
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
