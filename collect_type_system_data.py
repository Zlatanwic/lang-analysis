"""
编程语言类型系统特性数据采集脚本
====================================
数据来源：
1. 内置知识库：基于语言规范和学术文献（TAPL等）的类型系统特性标注
2. GitHub API：语言流行度数据（stars, repos count）
3. 语言发布时间线：关键类型特性引入的版本和年份

输出：
- languages_type_features.csv    类型系统特性矩阵
- languages_popularity.csv       GitHub 流行度数据
- feature_timeline.csv           特性引入时间线
- languages_combined.json        合并后的完整数据集
"""

import json
import csv
import os
from datetime import datetime

# ============================================================
# 第一部分：类型系统特性矩阵（基于语言规范手动标注）
# ============================================================
# 标注标准：
#   2 = 完整支持（语言核心特性，有完善的语法和语义支持）
#   1 = 部分支持（通过扩展/库/有限语法支持，或支持但有明显限制）
#   0 = 不支持
#
# 参考来源：
#   - 各语言官方 Reference / Spec
#   - Pierce, "Types and Programming Languages" (2002)
#   - Cardelli & Wegner, "On Understanding Types" (1985)
#   - 各语言 RFC / proposal 文档

FEATURES = [
    "parametric_polymorphism",      # 参数多态 / 泛型
    "ad_hoc_polymorphism",          # ad-hoc 多态 (trait/typeclass/interface with dispatch)
    "subtype_polymorphism",         # 子类型多态 (class inheritance)
    "algebraic_data_types",         # 代数数据类型 (sum types + product types)
    "pattern_matching",             # 模式匹配
    "type_inference",               # 类型推断
    "higher_kinded_types",          # 高阶类型 (HKT)
    "dependent_types",              # 依赖类型
    "linear_affine_types",          # 线性/仿射类型 (ownership/borrowing)
    "effect_system",                # 效果系统 (checked exceptions 算部分)
    "gadt",                         # 广义代数数据类型
    "type_classes",                 # Type classes / Traits (with coherence)
    "refinement_types",             # 精化类型
    "gradual_typing",               # 渐进类型
    "structural_typing",            # 结构化类型 (vs nominal)
    "flow_sensitive_typing",        # 流敏感类型 (narrowing/smart casts)
    "existential_types",            # 存在类型
    "rank_n_types",                 # Rank-N 多态
    "row_polymorphism",             # 行多态
    "macro_metaprogramming",        # 类型级宏/元编程
]

FEATURE_CATEGORIES = {
    "基础多态": ["parametric_polymorphism", "ad_hoc_polymorphism", "subtype_polymorphism"],
    "数据建模": ["algebraic_data_types", "pattern_matching"],
    "类型推断与安全": ["type_inference", "flow_sensitive_typing", "gradual_typing"],
    "高级类型特性": ["higher_kinded_types", "dependent_types", "gadt", 
                       "existential_types", "rank_n_types", "row_polymorphism"],
    "资源与效果": ["linear_affine_types", "effect_system", "refinement_types"],
    "类型组织": ["type_classes", "structural_typing", "macro_metaprogramming"],
}

# 语言元信息
LANGUAGES_META = {
    "C":          {"year": 1972, "paradigm": "imperative",   "domain": "systems",    "typing": "static/weak"},
    "C++":        {"year": 1985, "paradigm": "multi",        "domain": "systems",    "typing": "static/strong"},
    "Java":       {"year": 1995, "paradigm": "OOP",          "domain": "enterprise", "typing": "static/strong"},
    "Haskell":    {"year": 1990, "paradigm": "functional",   "domain": "academic",   "typing": "static/strong"},
    "OCaml":      {"year": 1996, "paradigm": "functional",   "domain": "academic",   "typing": "static/strong"},
    "Rust":       {"year": 2015, "paradigm": "multi",        "domain": "systems",    "typing": "static/strong"},
    "Go":         {"year": 2009, "paradigm": "imperative",   "domain": "systems",    "typing": "static/strong"},
    "TypeScript": {"year": 2012, "paradigm": "multi",        "domain": "web",        "typing": "static/gradual"},
    "Python":     {"year": 1991, "paradigm": "multi",        "domain": "general",    "typing": "dynamic/gradual"},
    "Scala":      {"year": 2004, "paradigm": "multi",        "domain": "enterprise", "typing": "static/strong"},
    "Kotlin":     {"year": 2011, "paradigm": "multi",        "domain": "mobile",     "typing": "static/strong"},
    "Swift":      {"year": 2014, "paradigm": "multi",        "domain": "mobile",     "typing": "static/strong"},
    "Zig":        {"year": 2016, "paradigm": "imperative",   "domain": "systems",    "typing": "static/strong"},
    "Idris":      {"year": 2007, "paradigm": "functional",   "domain": "academic",   "typing": "static/strong"},
    "Agda":       {"year": 2007, "paradigm": "functional",   "domain": "academic",   "typing": "static/strong"},
    "Elixir":     {"year": 2011, "paradigm": "functional",   "domain": "web",        "typing": "dynamic"},
    "F#":         {"year": 2005, "paradigm": "functional",   "domain": "enterprise", "typing": "static/strong"},
    "Nim":        {"year": 2008, "paradigm": "multi",        "domain": "systems",    "typing": "static/strong"},
    "Dart":       {"year": 2011, "paradigm": "OOP",          "domain": "mobile",     "typing": "static/strong"},
    "Julia":      {"year": 2012, "paradigm": "multi",        "domain": "scientific", "typing": "dynamic/strong"},
}

# 类型系统特性标注矩阵
# 每一行对应 FEATURES 列表的顺序
TYPE_FEATURES = {
    #                          para adh  sub  adt  pm   infer hkt  dep  lin  eff  gadt tc   ref  grad struct flow exist rankn row  macro
    "C":          {"scores":  [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,    0,    0,   1]},
    "C++":        {"scores":  [2,   1,   2,   1,   1,   2,   0,   0,   1,   0,   0,   1,   0,   0,   1,    0,   0,    0,    0,   2]},
    "Java":       {"scores":  [2,   2,   2,   1,   1,   1,   0,   0,   0,   1,   0,   0,   0,   0,   0,    0,   1,    0,    0,   0]},
    "Haskell":    {"scores":  [2,   2,   0,   2,   2,   2,   2,   0,   1,   1,   2,   2,   0,   0,   0,    0,   2,    2,    1,   1]},
    "OCaml":      {"scores":  [2,   1,   0,   2,   2,   2,   1,   0,   0,   0,   1,   1,   0,   0,   1,    0,   1,    1,    2,   1]},
    "Rust":       {"scores":  [2,   2,   0,   2,   2,   2,   0,   0,   2,   0,   0,   2,   0,   0,   0,    0,   1,    0,    0,   2]},
    "Go":         {"scores":  [2,   2,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   2,    0,   0,    0,    0,   0]},
    "TypeScript": {"scores":  [2,   1,   2,   2,   1,   2,   1,   0,   0,   0,   0,   0,   0,   2,   2,    2,   0,    0,    0,   2]},
    "Python":     {"scores":  [1,   1,   1,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   2,   1,    0,   0,    0,    0,   1]},
    "Scala":      {"scores":  [2,   2,   2,   2,   2,   2,   2,   1,   0,   1,   1,   2,   0,   0,   1,    0,   2,    1,    0,   1]},
    "Kotlin":     {"scores":  [2,   2,   2,   2,   2,   2,   0,   0,   0,   0,   0,   0,   0,   0,   0,    2,   0,    0,    0,   0]},
    "Swift":      {"scores":  [2,   2,   2,   2,   2,   2,   0,   0,   1,   0,   0,   2,   0,   0,   0,    0,   1,    0,    0,   1]},
    "Zig":        {"scores":  [2,   0,   0,   1,   1,   1,   0,   0,   0,   1,   0,   0,   0,   0,   0,    0,   0,    0,    0,   2]},
    "Idris":      {"scores":  [2,   2,   0,   2,   2,   2,   2,   2,   1,   2,   2,   2,   2,   0,   0,    0,   2,    2,    0,   1]},
    "Agda":       {"scores":  [2,   1,   0,   2,   2,   2,   2,   2,   0,   0,   2,   1,   2,   0,   0,    0,   2,    2,    0,   0]},
    "Elixir":     {"scores":  [0,   1,   0,   0,   2,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,    0,   0,    0,    0,   1]},
    "F#":         {"scores":  [2,   1,   1,   2,   2,   2,   1,   0,   0,   0,   0,   1,   0,   0,   1,    1,   1,    0,    0,   1]},
    "Nim":        {"scores":  [2,   1,   1,   1,   1,   2,   0,   0,   0,   1,   0,   1,   0,   0,   0,    0,   0,    0,    0,   2]},
    "Dart":       {"scores":  [2,   1,   2,   1,   2,   2,   0,   0,   0,   0,   0,   0,   0,   0,   0,    1,   0,    0,    0,   0]},
    "Julia":      {"scores":  [2,   2,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,    0,   0,    0,    0,   2]},
}

# ============================================================
# 第二部分：关键类型特性引入时间线
# ============================================================
# 格式: (语言, 特性, 版本, 年份, 来源备注)

FEATURE_TIMELINE = [
    # C++
    ("C++", "parametric_polymorphism", "C++98 Templates", 1998, "ISO/IEC 14882:1998"),
    ("C++", "type_inference", "C++11 auto", 2011, "N2546"),
    ("C++", "pattern_matching", "C++17 structured bindings", 2017, "P0144R2"),
    ("C++", "ad_hoc_polymorphism", "C++20 Concepts", 2020, "P0734R0"),
    ("C++", "linear_affine_types", "C++11 move semantics", 2011, "N2027"),
    
    # Java
    ("Java", "parametric_polymorphism", "JDK 5 Generics", 2004, "JSR 14"),
    ("Java", "type_inference", "JDK 10 var", 2018, "JEP 286"),
    ("Java", "pattern_matching", "JDK 16 instanceof patterns", 2021, "JEP 394"),
    ("Java", "algebraic_data_types", "JDK 17 sealed classes", 2021, "JEP 409"),
    ("Java", "effect_system", "JDK 1.0 checked exceptions", 1996, "JLS"),
    
    # Rust
    ("Rust", "linear_affine_types", "1.0 ownership/borrowing", 2015, "Rust Reference"),
    ("Rust", "type_classes", "1.0 traits", 2015, "RFC 0000"),
    ("Rust", "pattern_matching", "1.0 match", 2015, "Rust Reference"),
    ("Rust", "macro_metaprogramming", "1.0 macro_rules!", 2015, "Rust Reference"),
    ("Rust", "macro_metaprogramming", "1.15 proc macros (derive)", 2017, "RFC 1681"),
    
    # TypeScript
    ("TypeScript", "parametric_polymorphism", "0.9 Generics", 2013, "TS Spec"),
    ("TypeScript", "flow_sensitive_typing", "1.4 Type Guards", 2014, "TS 1.4 Release"),
    ("TypeScript", "gradual_typing", "1.0 any type", 2012, "TS Spec"),
    ("TypeScript", "macro_metaprogramming", "2.1 Mapped Types", 2016, "TS 2.1 Release"),
    ("TypeScript", "macro_metaprogramming", "2.8 Conditional Types", 2018, "TS 2.8 Release"),
    ("TypeScript", "algebraic_data_types", "2.0 Discriminated Unions", 2016, "TS 2.0 Release"),
    ("TypeScript", "structural_typing", "1.0", 2012, "TS Spec"),
    
    # Go
    ("Go", "parametric_polymorphism", "1.18 Generics", 2022, "Go Spec"),
    ("Go", "structural_typing", "1.0 interfaces", 2009, "Go Spec"),
    
    # Haskell
    ("Haskell", "type_classes", "Haskell 98", 1998, "Haskell Report"),
    ("Haskell", "gadt", "GHC 6.4 GADTs", 2005, "GHC docs"),
    ("Haskell", "rank_n_types", "GHC 6.6 RankNTypes", 2006, "GHC docs"),
    ("Haskell", "higher_kinded_types", "Haskell 98", 1998, "Haskell Report"),
    ("Haskell", "effect_system", "GHC IO Monad", 1998, "Peyton Jones 2001"),
    ("Haskell", "linear_affine_types", "GHC 9.0 LinearTypes", 2021, "GHC Proposal #111"),
    ("Haskell", "dependent_types", "GHC 9.x DependentHaskell (partial)", 2023, "GHC proposals"),
    
    # Scala
    ("Scala", "higher_kinded_types", "Scala 2", 2004, "Scala Spec"),
    ("Scala", "dependent_types", "Scala 3 match types", 2021, "Scala 3 Spec"),
    ("Scala", "type_classes", "Scala 2 implicits", 2004, "Scala Spec"),
    ("Scala", "type_classes", "Scala 3 given/using", 2021, "Scala 3 Spec"),
    ("Scala", "effect_system", "Scala 3 CanThrow", 2021, "SIP-47"),
    
    # Swift
    ("Swift", "type_classes", "1.0 Protocols", 2014, "Swift Docs"),
    ("Swift", "algebraic_data_types", "1.0 enum with associated values", 2014, "Swift Docs"),
    ("Swift", "pattern_matching", "1.0", 2014, "Swift Docs"),
    ("Swift", "linear_affine_types", "5.9 ~Copyable", 2023, "SE-0390"),
    
    # Kotlin
    ("Kotlin", "flow_sensitive_typing", "1.0 smart casts", 2016, "Kotlin Docs"),
    ("Kotlin", "pattern_matching", "2.0 when guards", 2024, "KT-13626"),
    
    # Python
    ("Python", "gradual_typing", "3.5 typing module", 2015, "PEP 484"),
    ("Python", "pattern_matching", "3.10 match statement", 2021, "PEP 634"),
    
    # Idris
    ("Idris", "dependent_types", "1.0", 2013, "Idris docs"),
    ("Idris", "effect_system", "2.0 Effects", 2020, "Idris 2 docs"),
    
    # F#
    ("F#", "algebraic_data_types", "1.0 Discriminated Unions", 2005, "F# Spec"),
    ("F#", "type_inference", "1.0 Hindley-Milner", 2005, "F# Spec"),
    ("F#", "pattern_matching", "1.0", 2005, "F# Spec"),
    
    # Dart
    ("Dart", "pattern_matching", "3.0 Patterns", 2023, "Dart Enhancement"),
    ("Dart", "algebraic_data_types", "3.0 sealed classes", 2023, "Dart Enhancement"),
    ("Dart", "flow_sensitive_typing", "2.12 null safety promotion", 2021, "Dart Docs"),
    
    # Julia
    ("Julia", "macro_metaprogramming", "1.0 @generated", 2018, "Julia Docs"),
    ("Julia", "ad_hoc_polymorphism", "1.0 multiple dispatch", 2018, "Julia Docs"),
]

# ============================================================
# 第三部分：GitHub 流行度数据（静态快照 + API 采集指引）
# ============================================================
# 以下为 2025 年中的近似数据快照，用于离线使用
# 如需实时数据，可取消注释 fetch_github_data() 并提供 token

GITHUB_POPULARITY_SNAPSHOT = {
    "C":          {"github_repos_approx": 1200000, "top_repo_stars": 190000, "top_repo": "linux"},
    "C++":        {"github_repos_approx": 800000,  "top_repo_stars": 120000, "top_repo": "tensorflow"},
    "Java":       {"github_repos_approx": 1500000, "top_repo_stars": 75000,  "top_repo": "spring-boot"},
    "Haskell":    {"github_repos_approx": 55000,   "top_repo_stars": 30000,  "top_repo": "shellcheck"},
    "OCaml":      {"github_repos_approx": 15000,   "top_repo_stars": 5000,   "top_repo": "ocaml/ocaml"},
    "Rust":       {"github_repos_approx": 350000,  "top_repo_stars": 100000, "top_repo": "deno"},
    "Go":         {"github_repos_approx": 700000,  "top_repo_stars": 125000, "top_repo": "go"},
    "TypeScript": {"github_repos_approx": 1000000, "top_repo_stars": 100000, "top_repo": "vscode"},
    "Python":     {"github_repos_approx": 2500000, "top_repo_stars": 65000,  "top_repo": "cpython"},
    "Scala":      {"github_repos_approx": 120000,  "top_repo_stars": 40000,  "top_repo": "spark"},
    "Kotlin":     {"github_repos_approx": 250000,  "top_repo_stars": 50000,  "top_repo": "kotlin"},
    "Swift":      {"github_repos_approx": 250000,  "top_repo_stars": 67000,  "top_repo": "swift"},
    "Zig":        {"github_repos_approx": 15000,   "top_repo_stars": 35000,  "top_repo": "zig"},
    "Idris":      {"github_repos_approx": 2000,    "top_repo_stars": 3800,   "top_repo": "Idris2"},
    "Agda":       {"github_repos_approx": 1500,    "top_repo_stars": 2500,   "top_repo": "agda"},
    "Elixir":     {"github_repos_approx": 80000,   "top_repo_stars": 25000,  "top_repo": "elixir"},
    "F#":         {"github_repos_approx": 20000,   "top_repo_stars": 4000,   "top_repo": "fsharp"},
    "Nim":        {"github_repos_approx": 12000,   "top_repo_stars": 16000,  "top_repo": "Nim"},
    "Dart":       {"github_repos_approx": 200000,  "top_repo_stars": 165000, "top_repo": "flutter"},
    "Julia":      {"github_repos_approx": 50000,   "top_repo_stars": 46000,  "top_repo": "julia"},
}

# GitHub API 实时采集函数（需要 token）
def fetch_github_data(token=None):
    """
    用 GitHub REST API 获取各语言的实时仓库数量和星标数据。
    需要 Personal Access Token 以避免 rate limit。
    
    用法:
        export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
        然后运行此脚本
    """
    import urllib.request
    import urllib.error
    
    if not token:
        token = os.environ.get("GITHUB_TOKEN")
    
    if not token:
        print("[INFO] 未设置 GITHUB_TOKEN，使用静态快照数据")
        return None
    
    results = {}
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
        "User-Agent": "TypeSystemCollector/1.0"
    }
    
    for lang in LANGUAGES_META:
        query = lang.lower()
        # 搜索该语言的仓库数量
        url = f"https://api.github.com/search/repositories?q=language:{query}&sort=stars&per_page=1"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                total_count = data.get("total_count", 0)
                top_repo = data["items"][0] if data.get("items") else None
                results[lang] = {
                    "github_repos_approx": total_count,
                    "top_repo_stars": top_repo["stargazers_count"] if top_repo else 0,
                    "top_repo": top_repo["full_name"] if top_repo else "N/A",
                }
                print(f"  [OK] {lang}: {total_count} repos")
        except Exception as e:
            print(f"  [ERR] {lang}: {e}")
            results[lang] = GITHUB_POPULARITY_SNAPSHOT.get(lang, {})
    
    return results

# ============================================================
# 第四部分：数据导出
# ============================================================

def export_type_features_csv(output_dir):
    """导出类型系统特性矩阵为 CSV"""
    filepath = os.path.join(output_dir, "languages_type_features.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        header = ["language", "year", "paradigm", "domain", "typing"] + FEATURES + ["total_score"]
        writer.writerow(header)
        
        for lang, meta in LANGUAGES_META.items():
            scores = TYPE_FEATURES[lang]["scores"]
            total = sum(scores)
            row = [lang, meta["year"], meta["paradigm"], meta["domain"], meta["typing"]] + scores + [total]
            writer.writerow(row)
    
    print(f"[EXPORT] {filepath}")
    return filepath

def export_timeline_csv(output_dir):
    """导出特性引入时间线为 CSV"""
    filepath = os.path.join(output_dir, "feature_timeline.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["language", "feature", "version_or_name", "year", "source"])
        for entry in sorted(FEATURE_TIMELINE, key=lambda x: (x[3], x[0])):
            writer.writerow(entry)
    
    print(f"[EXPORT] {filepath}")
    return filepath

def export_popularity_csv(output_dir, github_data=None):
    """导出流行度数据为 CSV"""
    data = github_data or GITHUB_POPULARITY_SNAPSHOT
    filepath = os.path.join(output_dir, "languages_popularity.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["language", "github_repos_approx", "top_repo_stars", "top_repo"])
        for lang in LANGUAGES_META:
            d = data.get(lang, {})
            writer.writerow([lang, d.get("github_repos_approx", 0),
                           d.get("top_repo_stars", 0), d.get("top_repo", "N/A")])
    
    print(f"[EXPORT] {filepath}")
    return filepath

def export_combined_json(output_dir, github_data=None):
    """导出合并后的完整 JSON 数据集"""
    popularity = github_data or GITHUB_POPULARITY_SNAPSHOT
    
    combined = {}
    for lang in LANGUAGES_META:
        scores = TYPE_FEATURES[lang]["scores"]
        feature_dict = {FEATURES[i]: scores[i] for i in range(len(FEATURES))}
        
        # 计算各分类得分
        category_scores = {}
        for cat, feats in FEATURE_CATEGORIES.items():
            cat_score = sum(feature_dict.get(f, 0) for f in feats)
            cat_max = len(feats) * 2
            category_scores[cat] = {
                "score": cat_score,
                "max": cat_max,
                "ratio": round(cat_score / cat_max, 2)
            }
        
        combined[lang] = {
            "meta": LANGUAGES_META[lang],
            "type_features": feature_dict,
            "feature_scores_by_category": category_scores,
            "total_score": sum(scores),
            "max_possible_score": len(FEATURES) * 2,
            "type_richness_ratio": round(sum(scores) / (len(FEATURES) * 2), 2),
            "popularity": popularity.get(lang, {}),
        }
    
    # 添加时间线数据
    timeline_by_lang = {}
    for lang, feat, version, year, source in FEATURE_TIMELINE:
        if lang not in timeline_by_lang:
            timeline_by_lang[lang] = []
        timeline_by_lang[lang].append({
            "feature": feat,
            "version": version,
            "year": year,
            "source": source,
        })
    
    dataset = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "num_languages": len(LANGUAGES_META),
            "num_features": len(FEATURES),
            "scoring": {
                "0": "不支持",
                "1": "部分支持",
                "2": "完整支持",
            },
            "feature_categories": {k: v for k, v in FEATURE_CATEGORIES.items()},
            "features_list": FEATURES,
        },
        "languages": combined,
        "timeline": timeline_by_lang,
    }
    
    filepath = os.path.join(output_dir, "languages_combined.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    print(f"[EXPORT] {filepath}")
    return filepath

def print_summary():
    """打印数据集摘要"""
    print("\n" + "=" * 60)
    print("  编程语言类型系统特性数据集 - 摘要")
    print("=" * 60)
    
    print(f"\n语言数量: {len(LANGUAGES_META)}")
    print(f"特性维度: {len(FEATURES)}")
    print(f"时间线事件: {len(FEATURE_TIMELINE)}")
    
    # 类型丰富度排名
    print("\n--- 类型系统丰富度排名 (总分/{}) ---".format(len(FEATURES) * 2))
    rankings = []
    for lang in LANGUAGES_META:
        total = sum(TYPE_FEATURES[lang]["scores"])
        rankings.append((lang, total))
    rankings.sort(key=lambda x: -x[1])
    
    for i, (lang, score) in enumerate(rankings, 1):
        bar = "█" * score + "░" * (len(FEATURES) * 2 - score)
        ratio = score / (len(FEATURES) * 2)
        print(f"  {i:2d}. {lang:<12s} {score:2d}/{len(FEATURES)*2}  ({ratio:.0%})  {bar}")
    
    # 各分类平均得分
    print("\n--- 各分类平均得分率 ---")
    for cat, feats in FEATURE_CATEGORIES.items():
        avg_ratio = 0
        for lang in LANGUAGES_META:
            scores = TYPE_FEATURES[lang]["scores"]
            feat_dict = {FEATURES[i]: scores[i] for i in range(len(FEATURES))}
            cat_score = sum(feat_dict.get(f, 0) for f in feats)
            avg_ratio += cat_score / (len(feats) * 2)
        avg_ratio /= len(LANGUAGES_META)
        print(f"  {cat:<16s}: {avg_ratio:.0%}")
    
    # 特性普及率
    print("\n--- 各特性普及率 (≥1 分的语言占比) ---")
    for i, feat in enumerate(FEATURES):
        count = sum(1 for lang in LANGUAGES_META if TYPE_FEATURES[lang]["scores"][i] >= 1)
        ratio = count / len(LANGUAGES_META)
        print(f"  {feat:<30s}: {count:2d}/{len(LANGUAGES_META)} ({ratio:.0%})")


def main():
    output_dir = os.environ.get("OUTPUT_DIR", ".")
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("  编程语言类型系统数据采集脚本")
    print("=" * 60)
    
    # 尝试从 GitHub 获取实时数据
    print("\n[1/4] 尝试获取 GitHub 数据...")
    github_data = fetch_github_data()
    
    # 导出数据
    print("\n[2/4] 导出类型特性矩阵...")
    export_type_features_csv(output_dir)
    
    print("\n[3/4] 导出特性时间线...")
    export_timeline_csv(output_dir)
    
    print("\n[4/4] 导出合并数据集...")
    export_popularity_csv(output_dir, github_data)
    export_combined_json(output_dir, github_data)
    
    # 打印摘要
    print_summary()
    
    print("\n" + "=" * 60)
    print("  数据采集完成！输出文件：")
    print(f"    {output_dir}/languages_type_features.csv")
    print(f"    {output_dir}/feature_timeline.csv")
    print(f"    {output_dir}/languages_popularity.csv")
    print(f"    {output_dir}/languages_combined.json")
    print("=" * 60)


if __name__ == "__main__":
    main()
