import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const runtimeEnv = (globalThis as { process?: { env?: Record<string, string | undefined> } })
  .process?.env ?? {}
const repository = runtimeEnv.GITHUB_REPOSITORY ?? ''
const repositoryName = repository.split('/')[1] ?? ''
const defaultPagesBase = repositoryName ? `/${repositoryName}/` : '/'
const base = runtimeEnv.VITE_BASE_PATH
  ?? (runtimeEnv.GITHUB_ACTIONS === 'true' ? defaultPagesBase : '/')

export default defineConfig({
  base,
  plugins: [vue()],
  server: {
    port: 5173,
  },
})
