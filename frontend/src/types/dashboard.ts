export interface TimelineEvent {
  year: number
  language: string
  feature: string
  feature_label: string
}

export interface ArmsRaceSeries {
  years: number[]
  yearly_counts: number[]
  cumulative_counts: number[]
  moving_average: number[]
  acceleration: number[]
  total_events: number
  peak_year: number | null
  peak_count: number
}

export interface HeatmapLanguage {
  name: string
  year: number
  paradigm: string
  domain: string
  scores: number[]
  complexity: number
  rationale: Record<string, string>
}

export interface NetworkNode {
  name: string
  paradigm: string
  domain: string
  complexity: number
}

export interface NetworkEdge {
  source: string
  target: string
  similarity: number
}

export interface PopularityPoint {
  name: string
  paradigm: string
  domain: string
  complexity: number
  tiobe_rank?: number
  github_stars_rank?: number
  stackoverflow_loved_pct?: number
  notes?: string
}

export interface DiffusionEvent {
  language: string
  year: number
  score: number
  paradigm: string
  domain: string
  domain_group: string
}

export interface DiffusionFeature {
  label: string
  events: DiffusionEvent[]
}

export interface ClusterPoint {
  name: string
  x: number
  y: number
  cluster: number
  cluster_label: string
  domain: string
  domain_group: string
  paradigm: string
  complexity: number
}

export interface LineageNode {
  name: string
  year: number
  paradigm: string
  domain: string
  domain_group: string
  complexity: number
  virtual?: boolean
}

export interface LineageEdge {
  source: string
  target: string
  reason: string
}

export interface CooccurrenceCell {
  x: string
  y: string
  x_index: number
  y_index: number
  correlation: number
  cooccurrence: number
  support_x: number
  support_y: number
}

export interface CooccurrenceTopPair {
  feature_a: string
  feature_b: string
  label_a: string
  label_b: string
  correlation: number
  cooccurrence: number
}

export interface DashboardData {
  features: string[]
  feature_labels: Record<string, string>
  feature_short_labels: Record<string, string>
  scoring: Record<string, string>
  max_score: number
  heatmap: HeatmapLanguage[]
  network: {
    nodes: NetworkNode[]
    edges: NetworkEdge[]
  }
  timeline: TimelineEvent[]
  arms_race: ArmsRaceSeries
  popularity: PopularityPoint[]
  diffusion: {
    default_feature: string
    features: Record<string, DiffusionFeature>
  }
  lineage: {
    nodes: LineageNode[]
    edges: LineageEdge[]
  }
  clusters: {
    cluster_labels: Record<string, string>
    points: ClusterPoint[]
  }
  cooccurrence: {
    features: string[]
    prevalence: Record<string, number>
    cells: CooccurrenceCell[]
    top_pairs: CooccurrenceTopPair[]
  }
}
