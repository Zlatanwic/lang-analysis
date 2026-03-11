# Lang Analysis Dashboard

[![Deploy GitHub Pages](https://github.com/Zlatanwic/lang-analysis/actions/workflows/deploy-github-pages.yml/badge.svg)](https://github.com/Zlatanwic/lang-analysis/actions/workflows/deploy-github-pages.yml)
[Live Site](https://zlatanwic.github.io/lang-analysis/)

A Vue 3 + Vite dashboard for exploring programming language type-system features, similarity, adoption timelines, lineage, and recommendation scenarios.

Python is responsible for turning the source dataset into frontend-ready JSON. Vue is responsible for the UI, charts, interactions, and layout.

## Overview

The dashboard is built around a single generated data bundle:

- Source data lives in [`data/languages.json`](/e:/lang_analysis/data/languages.json)
- Python transforms that data in [`src/data_processing.py`](/e:/lang_analysis/src/data_processing.py)
- The generated bundle is written to [`frontend/public/dashboard-data.json`](/e:/lang_analysis/frontend/public/dashboard-data.json)
- The Vue app in [`frontend/`](/e:/lang_analysis/frontend/) reads that JSON and renders the dashboard

This repository no longer supports the old standalone HTML template path. Vue is now the only frontend implementation.

## What The Dashboard Includes

- Feature matrix with compact headers and hover detail
- Radar comparison for cross-language feature profiles
- Feature timeline for adoption events over time
- Similarity network for clustering related languages
- Popularity analysis against external ranking signals
- Feature diffusion view for capability spread over time
- Domain clustering based on feature vectors
- Lineage graph for influence relationships
- Interactive recommender for feature-driven language matching

## Requirements

- Python 3.11+
- Node.js 22+
- `pnpm` 10+

## Quick Start

### 1. Install frontend dependencies

```powershell
cd frontend
pnpm install
```

If `pnpm install` warns that `esbuild` build scripts were ignored, run:

```powershell
pnpm approve-builds
pnpm rebuild esbuild
```

### 2. Generate the frontend data bundle

From the repository root:

```powershell
python main.py
```

This writes:

```text
frontend/public/dashboard-data.json
```

### 3. Start the Vue app

```powershell
cd frontend
pnpm dev
```

For a one-command local dev flow:

```powershell
cd frontend
pnpm run dev:sync
```

That regenerates the JSON data first, then starts Vite.

## Common Commands

### Generate dashboard data

```powershell
python main.py
```

### Generate data to a custom path

```powershell
python main.py --json-output custom/path/dashboard-data.json
```

### Type-check the frontend

```powershell
cd frontend
pnpm run check
```

### Build the frontend

```powershell
cd frontend
pnpm run build
```

### Preview the production build

```powershell
cd frontend
pnpm run preview
```

## Deploy To GitHub Pages

This repository is configured to deploy through GitHub Actions with the workflow in [`.github/workflows/deploy-github-pages.yml`](/e:/lang_analysis/.github/workflows/deploy-github-pages.yml).

### What the workflow does

1. Checks out the repository
2. Sets up Python and Node.js
3. Generates `frontend/public/dashboard-data.json`
4. Installs frontend dependencies with `pnpm`
5. Runs `pnpm run check`
6. Builds the Vue app with the correct GitHub Pages `base` path
7. Uploads `frontend/dist`
8. Deploys the build to GitHub Pages

### One-time GitHub repository setup

In your GitHub repository:

1. Open `Settings`
2. Open `Pages`
3. Set `Source` to `GitHub Actions`

After that, every push to `main` will trigger a deployment.

### Expected Pages URL

For this repository remote, the site URL should be:

```text
https://zlatanwic.github.io/lang-analysis/
```

That URL is inferred from the current remote repository name `Zlatanwic/lang-analysis`.

## Data Flow

The project uses a simple two-step flow:

1. `data/languages.json` is loaded by [`src/data_processing.py`](/e:/lang_analysis/src/data_processing.py)
2. [`main.py`](/e:/lang_analysis/main.py) serializes the processed result into `frontend/public/dashboard-data.json`
3. The Vue app loads that file through [`frontend/src/composables/useDashboardData.ts`](/e:/lang_analysis/frontend/src/composables/useDashboardData.ts)
4. Individual panel components render their own chart or interaction layer from the shared dataset

This separation keeps data modeling in Python and UI logic in Vue.

## Project Structure

### Root

- [`main.py`](/e:/lang_analysis/main.py): generates the frontend JSON bundle
- [`data/languages.json`](/e:/lang_analysis/data/languages.json): source dataset
- [`src/data_processing.py`](/e:/lang_analysis/src/data_processing.py): Python transformation logic

### Frontend

- [`frontend/src/App.vue`](/e:/lang_analysis/frontend/src/App.vue): app shell and tab orchestration
- [`frontend/src/components/PanelCard.vue`](/e:/lang_analysis/frontend/src/components/PanelCard.vue): shared panel wrapper
- [`frontend/src/components/EChartPanel.vue`](/e:/lang_analysis/frontend/src/components/EChartPanel.vue): reusable ECharts mount component
- [`frontend/src/components/panels/`](/e:/lang_analysis/frontend/src/components/panels): dashboard views
- [`frontend/src/composables/useDashboardData.ts`](/e:/lang_analysis/frontend/src/composables/useDashboardData.ts): JSON loading
- [`frontend/src/types/dashboard.ts`](/e:/lang_analysis/frontend/src/types/dashboard.ts): shared data types
- [`frontend/src/constants.ts`](/e:/lang_analysis/frontend/src/constants.ts): colors and UI constants
- [`frontend/package.json`](/e:/lang_analysis/frontend/package.json): frontend scripts and dependencies

## Development Notes

- The frontend uses Vue 3 Composition API with TypeScript.
- Charts are rendered with ECharts.
- Some interactions use VueUse helpers.
- The dashboard expects `frontend/public/dashboard-data.json` to exist before the app is opened.

## Troubleshooting

### `pnpm run build` fails with `spawn EPERM`

This is usually an `esbuild` approval or Windows execution issue, not a Vue code issue.

Try:

```powershell
cd frontend
pnpm approve-builds
pnpm rebuild esbuild
pnpm run build
```

### GitHub Pages deploy succeeds but assets 404

The Vite config now computes the correct repository subpath during GitHub Actions builds.

If you ever deploy this app under a different path, set a custom base explicitly:

```powershell
cd frontend
$env:VITE_BASE_PATH='/your-repo-name/'
pnpm run build
```

### The app loads but shows missing data

Regenerate the JSON bundle:

```powershell
python main.py
```

### Type-checking the frontend

This repository has already been validated with:

```powershell
cd frontend
pnpm run check
```

## Current Status

- Vue frontend migration completed
- Legacy HTML renderer removed
- Python now only generates frontend-consumable JSON
- `pnpm run check` passes
