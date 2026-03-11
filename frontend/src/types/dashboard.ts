export interface TimelineEvent {
  year: number
  language: string
  feature: string
  feature_label: string
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
}
