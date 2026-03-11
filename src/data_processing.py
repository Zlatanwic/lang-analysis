"""Data processing module for type system knowledge graph."""

import json
import math
from pathlib import Path


def load_data(path: str | None = None) -> dict:
    """Load the language type system dataset."""
    if path is None:
        path = str(Path(__file__).parent.parent / "data" / "languages.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_feature_names(data: dict) -> list[str]:
    """Return ordered list of feature keys."""
    return list(data["metadata"]["features"].keys())


def get_feature_labels(data: dict) -> dict[str, str]:
    """Return feature key -> human-readable label mapping."""
    return data["metadata"]["features"]


def get_feature_short_labels() -> dict[str, str]:
    """Return compact labels for dense dashboard table headers."""
    return {
        "parametric_polymorphism": "Generics",
        "ad_hoc_polymorphism": "Traits",
        "algebraic_data_types": "ADTs",
        "pattern_matching": "Matching",
        "ownership_lifetime": "Ownership",
        "dependent_types": "Dep Types",
        "gadts": "GADTs",
        "higher_kinded_types": "HKT",
        "effect_system": "Effects",
        "refinement_types": "Refinement",
        "gradual_typing": "Gradual",
        "type_inference": "Inference",
        "structural_typing": "Structural",
        "flow_sensitive_typing": "Flow",
    }


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


def pearson_correlation(a: list[float], b: list[float]) -> float:
    """Compute Pearson correlation between two equal-length vectors."""
    if not a or not b or len(a) != len(b):
        return 0.0

    mean_a = sum(a) / len(a)
    mean_b = sum(b) / len(b)
    centered_a = [value - mean_a for value in a]
    centered_b = [value - mean_b for value in b]
    numerator = sum(x * y for x, y in zip(centered_a, centered_b))
    denom_a = math.sqrt(sum(value * value for value in centered_a))
    denom_b = math.sqrt(sum(value * value for value in centered_b))
    if denom_a == 0 or denom_b == 0:
        return 0.0
    return numerator / (denom_a * denom_b)


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


def build_arms_race_index(data: dict) -> dict:
    """Aggregate yearly feature arrivals into an acceleration-focused trend series."""
    events = build_timeline_events(data)
    if not events:
        return {
            "years": [],
            "yearly_counts": [],
            "cumulative_counts": [],
            "moving_average": [],
            "acceleration": [],
            "total_events": 0,
            "peak_year": None,
            "peak_count": 0,
        }

    years = list(range(events[0]["year"], events[-1]["year"] + 1))
    yearly_totals = {year: 0 for year in years}
    for event in events:
        yearly_totals[event["year"]] += 1

    yearly_counts = [yearly_totals[year] for year in years]
    cumulative_counts = []
    running_total = 0
    for count in yearly_counts:
        running_total += count
        cumulative_counts.append(running_total)

    moving_average = []
    for idx in range(len(yearly_counts)):
        start_idx = max(0, idx - 4)
        window = yearly_counts[start_idx : idx + 1]
        moving_average.append(round(sum(window) / len(window), 2))

    acceleration = []
    previous = 0
    for count in yearly_counts:
        acceleration.append(count - previous)
        previous = count

    peak_count = max(yearly_counts)
    peak_year = years[yearly_counts.index(peak_count)]

    return {
        "years": years,
        "yearly_counts": yearly_counts,
        "cumulative_counts": cumulative_counts,
        "moving_average": moving_average,
        "acceleration": acceleration,
        "total_events": len(events),
        "peak_year": peak_year,
        "peak_count": peak_count,
    }


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


def get_domain_group(domain: str) -> str:
    """Collapse detailed domains into a top-level category."""
    return domain.split(" / ")[0].strip()


def build_feature_diffusion(data: dict) -> dict:
    """Build chronological adoption paths for each feature."""
    labels = get_feature_labels(data)
    features = get_feature_names(data)
    diffusion = {}
    for feature in features:
        events = []
        for lang in data["languages"]:
            year = lang.get("feature_timeline", {}).get(feature)
            score = lang["features"].get(feature, 0)
            if year is None and score <= 0:
                continue
            events.append({
                "language": lang["name"],
                "year": year or lang["year"],
                "score": score,
                "paradigm": lang["paradigm"],
                "domain": lang["domain"],
                "domain_group": get_domain_group(lang["domain"]),
            })
        events.sort(key=lambda item: (item["year"], item["language"]))
        diffusion[feature] = {
            "label": labels.get(feature, feature),
            "events": events,
        }
    return {
        "default_feature": "pattern_matching" if "pattern_matching" in diffusion else features[0],
        "features": diffusion,
    }


def build_language_lineage(data: dict) -> dict:
    """Build a directed language influence graph with a few virtual roots."""
    languages = {lang["name"]: lang for lang in data["languages"]}
    virtual_nodes = {
        "ML": {
            "name": "ML",
            "year": 1973,
            "paradigm": "Functional",
            "domain": "Academic / Research",
            "domain_group": "Academic",
            "complexity": 0,
            "virtual": True,
        },
        "Lisp": {
            "name": "Lisp",
            "year": 1958,
            "paradigm": "Functional",
            "domain": "Academic / General",
            "domain_group": "Academic",
            "complexity": 0,
            "virtual": True,
        },
        "Erlang": {
            "name": "Erlang",
            "year": 1986,
            "paradigm": "Functional",
            "domain": "Web / Distributed",
            "domain_group": "Web",
            "complexity": 0,
            "virtual": True,
        },
        "JavaScript": {
            "name": "JavaScript",
            "year": 1995,
            "paradigm": "Multi-paradigm",
            "domain": "Web development",
            "domain_group": "Web",
            "complexity": 0,
            "virtual": True,
        },
    }

    influence_edges = [
        ("ML", "OCaml", "Module system and pattern matching"),
        ("ML", "Haskell", "Typed FP lineage and Hindley-Milner"),
        ("OCaml", "F#", "ML family on .NET"),
        ("OCaml", "Rust", "Enums and pattern matching ergonomics"),
        ("Haskell", "PureScript", "Type classes and HKT for the web"),
        ("Haskell", "Elm", "Typed FP frontend simplification"),
        ("Haskell", "Idris", "Dependent type research lineage"),
        ("Haskell", "Roc", "Elm-like UX with stronger FP roots"),
        ("Haskell", "Rust", "Traits, ADTs, and expressive type design"),
        ("Java", "C#", ".NET response to Java-style OO"),
        ("Java", "Scala", "JVM platform and enterprise interop"),
        ("Java", "Kotlin", "Pragmatic JVM evolution"),
        ("C#", "F#", "Functional language on the CLR"),
        ("C", "C++", "Systems performance and syntax lineage"),
        ("C", "Go", "Compiled systems simplicity"),
        ("C", "Rust", "Systems programming baseline"),
        ("C", "Zig", "Manual control and low-level portability"),
        ("C", "Nim", "C interoperability and systems focus"),
        ("C++", "Rust", "Safety and zero-cost abstractions reaction"),
        ("JavaScript", "TypeScript", "Gradual typing for the JS ecosystem"),
        ("Erlang", "Elixir", "BEAM runtime and distributed model"),
        ("Lisp", "Clojure", "Modern Lisp on the JVM"),
        ("Ruby", "Elixir", "Developer-friendly web ergonomics"),
    ]

    nodes = []
    for name, lang in languages.items():
        nodes.append({
            "name": name,
            "year": lang["year"],
            "paradigm": lang["paradigm"],
            "domain": lang["domain"],
            "domain_group": get_domain_group(lang["domain"]),
            "complexity": compute_type_complexity_score(lang),
            "virtual": False,
        })
    nodes.extend(virtual_nodes.values())

    return {
        "nodes": nodes,
        "edges": [
            {"source": source, "target": target, "reason": reason}
            for source, target, reason in influence_edges
            if source in virtual_nodes or source in languages
            if target in virtual_nodes or target in languages
        ],
    }


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _normalize(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector[:]
    return [value / norm for value in vector]


def _mat_vec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [_dot(row, vector) for row in matrix]


def _power_iteration(matrix: list[list[float]], iterations: int = 64) -> tuple[float, list[float]]:
    size = len(matrix)
    vector = _normalize([1.0 + (idx * 0.07) for idx in range(size)])
    for _ in range(iterations):
        vector = _normalize(_mat_vec(matrix, vector))
    eigenvalue = _dot(vector, _mat_vec(matrix, vector))
    return eigenvalue, vector


def _deflate(matrix: list[list[float]], eigenvalue: float, eigenvector: list[float]) -> list[list[float]]:
    size = len(matrix)
    return [
        [
            matrix[row][col] - eigenvalue * eigenvector[row] * eigenvector[col]
            for col in range(size)
        ]
        for row in range(size)
    ]


def _project_pca_2d(vectors: list[list[float]]) -> tuple[list[tuple[float, float]], list[list[float]]]:
    if not vectors:
        return [], []

    dimension = len(vectors[0])
    count = len(vectors)
    means = [
        sum(vector[idx] for vector in vectors) / count
        for idx in range(dimension)
    ]
    centered = [
        [vector[idx] - means[idx] for idx in range(dimension)]
        for vector in vectors
    ]

    covariance = []
    denom = max(count - 1, 1)
    for row in range(dimension):
        covariance_row = []
        for col in range(dimension):
            covariance_row.append(
                sum(vector[row] * vector[col] for vector in centered) / denom
            )
        covariance.append(covariance_row)

    eigenvalue_1, eigenvector_1 = _power_iteration(covariance)
    covariance_2 = _deflate(covariance, eigenvalue_1, eigenvector_1)
    _, eigenvector_2 = _power_iteration(covariance_2)

    projections = [
        (_dot(vector, eigenvector_1), _dot(vector, eigenvector_2))
        for vector in centered
    ]
    return projections, centered


def _kmeans(points: list[list[float]], k: int = 3, iterations: int = 24) -> tuple[list[int], list[list[float]]]:
    if not points:
        return [], []

    k = min(k, len(points))
    centroids = [point[:] for point in points[:k]]
    assignments = [0] * len(points)

    for _ in range(iterations):
        updated = False
        for idx, point in enumerate(points):
            distances = [
                sum((value - centroid[dim]) ** 2 for dim, value in enumerate(point))
                for centroid in centroids
            ]
            cluster = min(range(k), key=lambda cluster_idx: distances[cluster_idx])
            if assignments[idx] != cluster:
                assignments[idx] = cluster
                updated = True

        grouped: list[list[list[float]]] = [[] for _ in range(k)]
        for assignment, point in zip(assignments, points):
            grouped[assignment].append(point)

        new_centroids = []
        for cluster_idx, group in enumerate(grouped):
            if not group:
                new_centroids.append(centroids[cluster_idx])
                continue
            new_centroids.append([
                sum(point[dim] for point in group) / len(group)
                for dim in range(len(group[0]))
            ])
        centroids = new_centroids

        if not updated:
            break

    return assignments, centroids


def build_domain_clusters(data: dict) -> dict:
    """Project languages into 2D and cluster them by type-feature profile."""
    languages = data["languages"]
    features = get_feature_names(data)
    raw_vectors = [
        [lang["features"].get(feature, 0) for feature in features]
        for lang in languages
    ]
    projections, centered_vectors = _project_pca_2d(raw_vectors)
    assignments, _ = _kmeans(centered_vectors, k=3)

    cluster_domain_votes: dict[int, dict[str, int]] = {}
    for assignment, lang in zip(assignments, languages):
        cluster_domain_votes.setdefault(assignment, {})
        group = get_domain_group(lang["domain"])
        cluster_domain_votes[assignment][group] = cluster_domain_votes[assignment].get(group, 0) + 1

    cluster_labels = {}
    for assignment, votes in cluster_domain_votes.items():
        dominant_group = max(votes.items(), key=lambda item: item[1])[0]
        cluster_labels[assignment] = f"Cluster {assignment + 1} / {dominant_group}-leaning"

    points = []
    for idx, lang in enumerate(languages):
        x, y = projections[idx]
        cluster = assignments[idx]
        points.append({
            "name": lang["name"],
            "x": round(x, 3),
            "y": round(y, 3),
            "cluster": cluster,
            "cluster_label": cluster_labels[cluster],
            "domain": lang["domain"],
            "domain_group": get_domain_group(lang["domain"]),
            "paradigm": lang["paradigm"],
            "complexity": compute_type_complexity_score(lang),
        })

    return {
        "cluster_labels": cluster_labels,
        "points": points,
    }


def build_feature_cooccurrence(data: dict) -> dict:
    """Measure how strongly features travel together across the language set."""
    features = get_feature_names(data)
    labels = get_feature_labels(data)
    feature_scores = {
        feature: [lang["features"].get(feature, 0) for lang in data["languages"]]
        for feature in features
    }
    prevalence = {
        feature: sum(1 for score in scores if score > 0)
        for feature, scores in feature_scores.items()
    }

    cells = []
    top_pairs = []
    for y_index, feature_y in enumerate(features):
        scores_y = feature_scores[feature_y]
        for x_index, feature_x in enumerate(features):
            scores_x = feature_scores[feature_x]
            correlation = 1.0 if feature_x == feature_y else pearson_correlation(scores_x, scores_y)
            cooccurrence = sum(
                1 for score_x, score_y in zip(scores_x, scores_y)
                if score_x > 0 and score_y > 0
            )
            cells.append({
                "x": feature_x,
                "y": feature_y,
                "x_index": x_index,
                "y_index": y_index,
                "correlation": round(correlation, 3),
                "cooccurrence": cooccurrence,
                "support_x": prevalence[feature_x],
                "support_y": prevalence[feature_y],
            })
            if x_index < y_index:
                top_pairs.append({
                    "feature_a": feature_x,
                    "feature_b": feature_y,
                    "label_a": labels.get(feature_x, feature_x),
                    "label_b": labels.get(feature_y, feature_y),
                    "correlation": round(correlation, 3),
                    "cooccurrence": cooccurrence,
                })

    top_pairs.sort(
        key=lambda pair: (pair["correlation"], pair["cooccurrence"]),
        reverse=True,
    )

    return {
        "features": features,
        "prevalence": prevalence,
        "cells": cells,
        "top_pairs": top_pairs[:6],
    }


def prepare_dashboard_data(data: dict) -> dict:
    """Prepare all data needed by the frontend dashboard."""
    features = get_feature_names(data)
    labels = get_feature_labels(data)
    short_labels = get_feature_short_labels()
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
    arms_race = build_arms_race_index(data)

    # Popularity
    popularity = build_popularity_data(data)

    # Diffusion, lineage, clustering, and co-occurrence
    diffusion = build_feature_diffusion(data)
    lineage = build_language_lineage(data)
    clusters = build_domain_clusters(data)
    cooccurrence = build_feature_cooccurrence(data)

    return {
        "features": features,
        "feature_labels": labels,
        "feature_short_labels": {
            feature: short_labels.get(feature, labels.get(feature, feature))
            for feature in features
        },
        "scoring": scoring,
        "max_score": max_score,
        "heatmap": heatmap_languages,
        "network": {"nodes": nodes, "edges": edges},
        "timeline": timeline,
        "arms_race": arms_race,
        "popularity": popularity,
        "diffusion": diffusion,
        "lineage": lineage,
        "clusters": clusters,
        "cooccurrence": cooccurrence,
    }
