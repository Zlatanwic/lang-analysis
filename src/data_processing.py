"""Data processing module for type system knowledge graph."""

import json
import math
from pathlib import Path


def load_data(path: str | None = None) -> dict:
    """Load the language type system dataset."""
    if path is None:
        path = str(Path(__file__).parent.parent / "data" / "languages.json")
    with open(path) as f:
        return json.load(f)


def get_feature_names(data: dict) -> list[str]:
    """Return ordered list of feature keys."""
    return list(data["metadata"]["features"].keys())


def get_feature_labels(data: dict) -> dict[str, str]:
    """Return feature key -> human-readable label mapping."""
    return data["metadata"]["features"]


def get_scoring_scale(data: dict) -> dict[str, str]:
    """Return the scoring scale descriptions."""
    return data["metadata"]["scoring"]


def get_feature_vectors(data: dict) -> dict[str, list[int]]:
    """Return {language_name: [feature_scores]} dict."""
    features = get_feature_names(data)
    return {
        lang["name"]: [lang["features"].get(f, 0) for f in features]
        for lang in data["languages"]
    }


def cosine_similarity(a: list[int], b: list[int]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def compute_similarity_matrix(data: dict) -> dict:
    """Compute pairwise cosine similarity between all languages."""
    vectors = get_feature_vectors(data)
    names = list(vectors.keys())
    matrix = {}
    for i, name_a in enumerate(names):
        for j, name_b in enumerate(names):
            if i < j:
                sim = cosine_similarity(vectors[name_a], vectors[name_b])
                matrix[f"{name_a}|{name_b}"] = round(sim, 4)
    return {"names": names, "similarities": matrix}


def compute_similarity_edges(data: dict, threshold: float = 0.6) -> list[dict]:
    """Compute similarity edges for the network graph."""
    vectors = get_feature_vectors(data)
    names = list(vectors.keys())
    edges = []
    for i, name_a in enumerate(names):
        for j, name_b in enumerate(names):
            if i < j:
                sim = cosine_similarity(vectors[name_a], vectors[name_b])
                if sim >= threshold:
                    edges.append({
                        "source": name_a,
                        "target": name_b,
                        "similarity": round(sim, 4),
                    })
    return edges


def compute_type_complexity_score(lang: dict) -> int:
    """Sum of all feature scores as a rough complexity metric."""
    return sum(lang["features"].values())


def max_possible_score(data: dict) -> int:
    """Maximum possible complexity score (num_features * max_score)."""
    num_features = len(get_feature_names(data))
    max_score = max(int(k) for k in data["metadata"]["scoring"].keys())
    return num_features * max_score


def build_timeline_events(data: dict) -> list[dict]:
    """Build a flat list of (year, language, feature) events for the timeline."""
    labels = get_feature_labels(data)
    events = []
    for lang in data["languages"]:
        for feat, year in lang.get("feature_timeline", {}).items():
            events.append({
                "year": year,
                "language": lang["name"],
                "feature": feat,
                "feature_label": labels.get(feat, feat),
            })
    events.sort(key=lambda e: e["year"])
    return events


def build_popularity_data(data: dict) -> list[dict]:
    """Extract popularity data for the complexity-vs-popularity analysis."""
    result = []
    for lang in data["languages"]:
        pop = lang.get("popularity", {})
        if not pop:
            continue
        complexity = compute_type_complexity_score(lang)
        result.append({
            "name": lang["name"],
            "paradigm": lang["paradigm"],
            "domain": lang["domain"],
            "complexity": complexity,
            "tiobe_rank": pop.get("tiobe_rank"),
            "github_stars_rank": pop.get("github_stars_rank"),
            "stackoverflow_loved_pct": pop.get("stackoverflow_loved_pct"),
            "notes": pop.get("notes", ""),
        })
    return result


def prepare_dashboard_data(data: dict) -> dict:
    """Prepare all data needed by the frontend dashboard."""
    features = get_feature_names(data)
    labels = get_feature_labels(data)
    scoring = get_scoring_scale(data)
    max_score = max(int(k) for k in scoring.keys())

    # Heatmap data
    heatmap_languages = []
    for lang in data["languages"]:
        heatmap_languages.append({
            "name": lang["name"],
            "year": lang["year"],
            "paradigm": lang["paradigm"],
            "domain": lang["domain"],
            "scores": [lang["features"].get(f, 0) for f in features],
            "complexity": compute_type_complexity_score(lang),
            "rationale": lang.get("scoring_rationale", {}),
        })
    heatmap_languages.sort(key=lambda x: -x["complexity"])

    # Similarity network
    edges = compute_similarity_edges(data, threshold=0.65)
    nodes = []
    for lang in data["languages"]:
        complexity = compute_type_complexity_score(lang)
        nodes.append({
            "name": lang["name"],
            "paradigm": lang["paradigm"],
            "domain": lang["domain"],
            "complexity": complexity,
        })

    # Timeline
    timeline = build_timeline_events(data)

    # Popularity
    popularity = build_popularity_data(data)

    return {
        "features": features,
        "feature_labels": labels,
        "scoring": scoring,
        "max_score": max_score,
        "heatmap": heatmap_languages,
        "network": {"nodes": nodes, "edges": edges},
        "timeline": timeline,
        "popularity": popularity,
    }
