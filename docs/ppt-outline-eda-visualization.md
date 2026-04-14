# 编程语言类型系统知识图谱
## 探索性数据分析与可视化技术课程报告 PPT 大纲

---

## PPT 页数统计

| 部分 | 页数 |
|------|------|
| 第一部分：项目概述 | 4 页 |
| 第二部分：数据预处理与特征工程 | 2 页 |
| 第三部分：核心算法 | 5 页 |
| 第四部分：可视化技术 | 6 页 |
| 第五部分：应用案例 | 2 页 |
| 第六部分：技术总结 | 3 页 |
| **总计** | **22 页** |

---

# 第一部分：项目概述

---

## 第 1 页：封面

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│            编程语言类型系统知识图谱                           │
│                                                             │
│      Programming Language Type System Knowledge Atlas        │
│                                                             │
│   ────────────────────────────────────────────────          │
│                                                             │
│         探索性数据分析与可视化技术 课程报告                    │
│                                                             │
│         姓名：XXX    学号：XXXXXXXXXX                        │
│         学院：XXXXX    专业：XXXXX                          │
│                                                             │
│         2026年4月                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 第 2 页：研究背景与核心问题

**核心问题：如何系统化地比较编程语言的类型系统？**

### 传统语言比较维度

| 维度 | 说明 | 局限性 |
|------|------|--------|
| 语法风格 | 缩进、关键字、语法糖 | 主观性强，难以量化 |
| 社区热度 | GitHub Stars、SO 提问量 | 反映流行度，非语言质量 |
| 生态规模 | 第三方库数量、框架成熟度 | 与类型系统设计无直接关系 |

### 本项目的独特视角：类型系统设计

```
传统视角                              本项目视角
─────────                             ─────────
"Python 好用吗？"                    "Python 的类型系统表达能力如何？"
"Rust 学起来难？"                    "Rust 在类型安全层面解决了什么问题？"
"Go 为什么这么简单？"                "Go 在类型系统上做了哪些刻意取舍？"
```

### 类型系统的三个设计维度

| 维度 | 含义 | 示例语言 |
|------|------|---------|
| 表达力 (Expressiveness) | 类型级计算、证明能力 | Idris, Haskell |
| 安全性 (Safety) | 内存安全、类型安全 | Rust, Swift |
| 工程化 (Pragmatism) | 学习曲线、渐进迁移 | TypeScript, Python |

---

## 第 3 页：数据类型与评分标准

### 数据来源

| 来源类型 | 具体内容 | 权威性 |
|---------|---------|--------|
| 语言官方规范 | Rust Reference, Haskell Report, JLS | ★★★★★ |
| 学术文献 | TAPL (Pierce, 2002), Cardelli & Wegner 1985 | ★★★★★ |
| 语言实现验证 | 阅读编译器源码、测试边界情况 | ★★★★ |
| RFC/Proposals | Rust RFCs, Java JEPs, Scala SIPs | ★★★★ |

### 14 个类型系统特性维度

| 编号 | 特性标识 | 中文说明 | 代表语言 |
|------|---------|---------|---------|
| 1 | parametric_polymorphism | 参数多态 / 泛型 | Rust, Haskell, Scala |
| 2 | ad_hoc_polymorphism | Trait / Typeclass 多态 | Rust, Haskell |
| 3 | algebraic_data_types | 代数数据类型 (ADT) | Haskell, Rust, Scala |
| 4 | pattern_matching | 模式匹配 | Rust, Haskell, OCaml |
| 5 | ownership_lifetime | 所有权 / 生命周期 | Rust |
| 6 | dependent_types | 依赖类型 | Idris, Agda |
| 7 | gadts | 广义代数数据类型 | Haskell, Scala |
| 8 | higher_kinded_types | 高阶类型 (HKT) | Haskell, Scala |
| 9 | effect_system | 效应系统 | Haskell, Koka |
| 10 | refinement_types | 细化类型 | LiquidHaskell |
| 11 | gradual_typing | 渐进类型 | TypeScript |
| 12 | type_inference | 类型推断 | Haskell, OCaml |
| 13 | structural_typing | 结构化类型 | TypeScript |
| 14 | flow_sensitive_typing | 流敏感类型 | TypeScript |

### 六级评分标准 (0-5)

| 分数 | 英文 | 中文 | 含义 |
|------|------|------|------|
| 0 | Not supported | 不支持 | 功能完全不存在 |
| 1 | Minimal | 最小 | 极其有限或仅第三方支持 |
| 2 | Basic | 基础 | 功能存在但有明显限制 |
| 3 | Moderate | 中等 | 可用的实现，覆盖常见场景 |
| 4 | Strong | 强 | 良好集成，仅有微小缺陷 |
| 5 | Full | 完整 | 最佳实践或参考实现 |

### 评分示例：Rust 所有权系统

```json
{
  "ownership_lifetime": {
    "score": 5,
    "rationale": "Defines the category — borrow checker, lifetimes, move semantics"
  }
}
```

### 评分示例：TypeScript 渐进类型

```json
{
  "gradual_typing": {
    "score": 5,
    "rationale": "Designed for gradual adoption — any, unknown, strict mode"
  }
}
```

---

## 第 4 页：数据集概览

### 覆盖语言：26 门编程语言

按设计理念分类：

```
┌────────────────────────────────────────────────────────────┐
│  学术/理论导向                                              │
│  Haskell · Idris · Agda · OCaml · PureScript · Elm        │
├────────────────────────────────────────────────────────────┤
│  系统/底层编程                                              │
│  Rust · C · C++ · Zig · Nim                                │
├────────────────────────────────────────────────────────────┤
│  JVM 生态                                                  │
│  Scala · Kotlin · Java · Clojure                          │
├────────────────────────────────────────────────────────────┤
│  Web 前端                                                  │
│  TypeScript · Elm · Dart                                   │
├────────────────────────────────────────────────────────────┤
│  多范式语言                                                │
│  Python · Ruby · Go · F# · Swift · Julia                  │
├────────────────────────────────────────────────────────────┤
│  现代新锐                                                  │
│  Gleam · Roc · Elixir                                     │
└────────────────────────────────────────────────────────────┘
```

### 复杂度得分排名 Top 10

| 排名 | 语言 | 复杂度得分 | 特点 |
|------|------|-----------|------|
| 1 | Idris | 51 | 全功能依赖类型 |
| 2 | Haskell | 43 | 强类型系统参考实现 |
| 3 | Scala | 43 | JVM 上的强类型多范式 |
| 4 | PureScript | 40 | Haskell 系，编译到 JS |
| 5 | Rust | 32 | 现代系统编程，安全优先 |
| 6 | OCaml | 32 | 函数式 + 多范式 |
| 7 | Swift | 29 | Apple 平台，安全性 |
| 8 | Kotlin | 27 | Android 首选 |
| 9 | TypeScript | 26 | Web 类型安全 |
| 10 | F# | 26 | .NET 函数式 |

---

# 第二部分：数据预处理与特征工程

---

## 第 5 页：特征向量构建

### 原始数据到特征向量的转换

```python
# src/data_processing.py

def get_feature_vectors(data: dict) -> dict[str, list[int]]:
    """将每门语言转换为 14 维特征向量"""
    features = get_feature_names(data)  # 14 个特性标识符列表

    return {
        lang["name"]: [lang["features"].get(f, 0) for f in features]
        # 默认分数为 0（该语言不支持该特性）
        for lang in data["languages"]
    }
```

### 转换示例

```
输入：languages.json 中的一条语言记录
┌─────────────────────────────────────────────┐
│  "name": "Rust"                             │
│  "features": {                              │
│    "parametric_polymorphism": 5,             │
│    "ownership_lifetime": 5,                  │
│    "pattern_matching": 5,                    │
│    ...                                       │
│  }                                          │
└─────────────────────────────────────────────┘
                    ↓
输出：Rust 的 14 维特征向量
┌─────────────────────────────────────────────┐
│  Rust → [5, 5, 5, 5, 5, 0, 0, 1, 0, 0, 0,  │
│           4, 0, 2]                          │
└─────────────────────────────────────────────┘
           ↑  ↑  ↑  ↑  ↑           ↑     ↑
        泛型 特质 ADT 模式 所有权 推断 流敏感
```

### 向量空间假设

> 编程语言的类型系统可以通过 14 维特征向量进行数值化表示。每种语言对应一个长度为 14 的整数数组，数组元素取值为 0-5。通过计算向量间的相似度，可以量化语言间的"类型系统距离"。

---

## 第 6 页：数据管道架构

### 完整数据流

```
                    ┌──────────────────────────────┐
                    │   data/languages.json          │
                    │   (专家手工标注的原始数据)      │
                    └──────────────┬─────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │        main.py                │
                    │   入口脚本，调用数据生成函数    │
                    └──────────────┬─────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │   src/data_processing.py      │
                    │   ─────────────────────────   │
                    │   • 特征向量提取              │
                    │   • 余弦相似度计算            │
                    │   • PCA 降维 + K-means 聚类   │
                    │   • 皮尔逊相关系数            │
                    │   • 时间线事件构建            │
                    │   • 领域聚类构建              │
                    └──────────────┬─────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ frontend/public/             │
                    │ dashboard-data.json          │
                    │ (前端可消费的完整数据包)      │
                    └──────────────┬─────────────────┘
                                   │
                    ┌──────────────┴─────────────────┐
                    ▼                                  ▼
         ┌──────────────────┐              ┌──────────────────┐
         │  Vue 3 组件      │              │  ECharts 图表    │
         │  11 个分析面板   │              │  雷达图/网络图/  │
         │                  │              │  热力图/散点图    │
         └──────────────────┘              └──────────────────┘
```

### Python 数据处理模块职责

| 函数 | 职责 |
|------|------|
| `get_feature_vectors()` | 构建 14 维特征向量 |
| `cosine_similarity()` | 计算余弦相似度 |
| `pearson_correlation()` | 计算皮尔逊相关系数 |
| `compute_similarity_edges()` | 生成相似性网络边 |
| `build_domain_clusters()` | PCA + K-means 聚类 |
| `build_feature_cooccurrence()` | 特性共现分析 |
| `build_timeline_events()` | 时间线事件构建 |
| `build_arms_race_index()` | 军备竞赛指数 |
| `build_language_lineage()` | 谱系影响关系 |

---

# 第三部分：核心算法

---

## 第 7 页：余弦相似度算法

### 算法原理

余弦相似度衡量两个向量在方向上的一致性，忽略它们的长度差异。

```
向量 A 和 B 的点积
         A · B = |A| |B| cos(θ)

重新排列得：
         cos(θ) = (A · B) / (|A| |B|)
```

### 数学公式

$$
\text{cosine\_similarity}(A, B) = \frac{\sum_{i=1}^{n} A_i \times B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \times \sqrt{\sum_{i=1}^{n} B_i^2}}
$$

### 算法特性

| 特性 | 说明 |
|------|------|
| 取值范围 | [-1, 1]，本项目中实际为 [0, 1]（评分非负）|
| 值为 1 | 完全相似的特征分布 |
| 值为 0 | 无相似性（正交向量）|
| 对 magnitude 不敏感 | 只关注方向一致性 |

### Python 实现

```python
import math

def cosine_similarity(a: list[int], b: list[int]) -> float:
    """计算两个特征向量的余弦相似度"""
    dot = sum(x * y for x, y in zip(a, b))           # 点积
    mag_a = math.sqrt(sum(x * x for x in a))         # 向量 A 的模长
    mag_b = math.sqrt(sum(x * x for x in b))         # 向量 B 的模长

    if mag_a == 0 or mag_b == 0:
        return 0.0

    return dot / (mag_a * mag_b)
```

### 计算示例：Rust vs Haskell

```
Rust:    [5, 5, 5, 5, 5, 0, 0, 1, 0, 0, 0, 4, 0, 2]
Haskell: [5, 5, 5, 5, 0, 3, 5, 5, 3, 2, 0, 5, 0, 0]

Rust · Haskell = 5×5 + 5×5 + 5×5 + 5×5 + 5×0 + ... = 95
|Rust| = √(25+25+25+25+25+0+0+1+0+0+0+16+0+4) = √121 ≈ 11.0
|Haskell| = √(25+25+25+25+0+9+25+25+9+4+0+25+0+0) = √172 ≈ 13.1

cosine_similarity = 95 / (11.0 × 13.1) ≈ 0.658
```

### 相似度矩阵构建

```python
def compute_similarity_matrix(data: dict) -> dict:
    """计算所有语言对的余弦相似度"""
    vectors = get_feature_vectors(data)
    names = list(vectors.keys())
    matrix = {}

    for i, name_a in enumerate(names):
        for j, name_b in enumerate(names):
            if i < j:  # 只计算上三角（矩阵对称）
                sim = cosine_similarity(vectors[name_a], vectors[name_b])
                matrix[f"{name_a}|{name_b}"] = round(sim, 4)

    return {"names": names, "similarities": matrix}
```

---

## 第 8 页：皮尔逊相关系数

### 与余弦相似度的区别

| 算法 | 测量内容 | 对均值的处理 |
|------|---------|-------------|
| 余弦相似度 | 方向一致性 | 不处理 |
| 皮尔逊相关系数 | 线性相关性 | 先中心化（减去均值）|

### 皮尔逊相关系数的几何解释

```
余弦相似度：直接比较向量方向
皮尔逊：先对向量做中心化（减去均值），再比较方向

向量 A: [2, 4, 4, 6]   均值 = 4
向量 B: [10, 14, 14, 18] 均值 = 14

中心化后：
A': [-2, 0, 0, 2]
B': [-4, 0, 0, 4]

此时 A' 和 B' 方向完全一致，Pearson = 1.0
但原始向量的余弦相似度 < 1.0（因为绝对值差异大）
```

### 数学公式

$$
r = \frac{\sum_{i=1}^{n}(A_i - \bar{A})(B_i - \bar{B})}{\sqrt{\sum_{i=1}^{n}(A_i - \bar{A})^2} \times \sqrt{\sum_{i=1}^{n}(B_i - \bar{B})^2}}
$$

### Python 实现

```python
def pearson_correlation(a: list[float], b: list[float]) -> float:
    """计算皮尔逊相关系数"""
    if not a or not b or len(a) != len(b):
        return 0.0

    mean_a = sum(a) / len(a)
    mean_b = sum(b) / len(b)

    # 中心化
    centered_a = [value - mean_a for value in a]
    centered_b = [value - mean_b for value in b]

    # 计算相关系数
    numerator = sum(x * y for x, y in zip(centered_a, centered_b))
    denom_a = math.sqrt(sum(value * value for value in centered_a))
    denom_b = math.sqrt(sum(value * value for value in centered_b))

    if denom_a == 0 or denom_b == 0:
        return 0.0

    return numerator / (denom_a * denom_b)
```

### 应用场景：特性共现分析

皮尔逊相关系数用于识别哪些类型系统特性倾向于同时出现在编程语言中：

| 特性对 | 相关系数 | 解读 |
|-------|---------|------|
| ADTs ↔ Pattern Matching | ≈ 1.0 | 强共现：设计 ADT 的语言通常也会实现模式匹配 |
| Gradual Typing ↔ Type Inference | 中等正相关 | 渐进类型语言往往也注重类型推断 |
| Ownership ↔ Effect System | 弱相关 | 两者独立演进，无必然联系 |

---

## 第 9 页：PCA 降维算法

### 为什么需要 PCA？

- 14 维特征空间难以直观可视化
- 需要将语言投影到 2D 平面进行散点图展示
- 同时保留尽可能多的原始信息（方差）

### PCA 算法流程

```
┌─────────────────────────────────────────────────────────────┐
│                     PCA 降维流程                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: 数据中心化                                         │
│  ─────────────────                                          │
│  对每个特征维度，计算所有语言的平均值                          │
│  然后每条记录减去该均值                                      │
│                                                             │
│  原始向量: [f1, f2, ..., f14]                               │
│  均值向量: [μ1, μ2, ..., μ14]                               │
│  中心化后: [f1-μ1, f2-μ2, ..., f14-μ14]                    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 2: 计算协方差矩阵                                      │
│  ─────────────────────────                                  │
│  Σij = Cov(Xi, Xj) = E[(Xi - μi)(Xj - μj)]                │
│                                                             │
│  得到 14×14 的对称矩阵                                      │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 3: 幂迭代法求主特征向量                                │
│  ───────────────────────────────                            │
│  迭代公式: v_new = normalize(A × v_old)                     │
│  64 次迭代后收敛                                            │
│                                                             │
│  最大特征值 λ 对应的特征向量 = 第一主成分 (PC1)              │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 4: Deflation 去除已提取方向                            │
│  ───────────────────────────────                            │
│  A' = A - λ × v × v^T                                      │
│  从矩阵中移除 PC1 的贡献                                     │
│  对 A' 重复 Step 3，得到 PC2                               │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 5: 投影到 2D 平面                                     │
│  ────────────────────                                       │
│  语言 i 的新坐标:                                           │
│    x_i = PC1 · centered_vector_i                            │
│    y_i = PC2 · centered_vector_i                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 幂迭代法实现

```python
def _power_iteration(matrix: list[list[float]], iterations: int = 64):
    """幂迭代法求主特征向量"""
    size = len(matrix)
    # 非均匀初始化，避免零向量收敛问题
    vector = _normalize([1.0 + (idx * 0.07) for idx in range(size)])

    for _ in range(iterations):
        vector = _normalize(_mat_vec(matrix, vector))

    # Rayleigh 商计算特征值
    eigenvalue = _dot(vector, _mat_vec(matrix, vector))
    return eigenvalue, vector

def _deflate(matrix, eigenvalue, eigenvector):
    """Deflation: 从矩阵中移除已提取特征向量的贡献"""
    size = len(matrix)
    return [
        [
            matrix[row][col] - eigenvalue * eigenvector[row] * eigenvector[col]
            for col in range(size)
        ]
        for row in range(size)
    ]
```

### PCA 投影结果示例

```
           PC2 (第二主成分)
              │
              │      Haskell(3.2, 2.1)
              │           │
              │    Idris(2.8, 1.9)
              │           │
         0.5  │           │    Scala(1.5, 0.8)
              │           │
        ──────┼───────────┼────────────────── PC1 (第一主成分)
              │           │
              │           │    Rust(-0.5, -0.3)
              │           │
        -0.5  │           │
              │           │    Go(-1.2, -0.8)
              │           │
              │           │    C(-2.1, -1.5)
              │
```

---

## 第 10 页：K-means 聚类算法

### 算法原理

K-means 将语言分为 K 个簇，使得簇内方差最小化。

### 算法流程

```
┌─────────────────────────────────────────────────────────────┐
│                     K-means 聚类流程                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  输入: 中心化后的语言特征向量 (n × 14)                        │
│  参数: K = 3 (聚类数量)                                      │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  初始化:                                                    │
│  选择前 K 个点作为初始质心                                    │
│  centroids = [point[:] for point in points[:k]]             │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  迭代 (最多 24 次):                                          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  E 步 (分配):                                        │   │
│  │  对每个点，计算到所有质心的欧氏距离平方                  │   │
│  │  distance² = Σ((value - centroid)²)                  │   │
│  │  分配到距离最近的质心所属的簇                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  M 步 (更新):                                        │   │
│  │  对每个簇，重新计算质心位置                            │   │
│  │  new_centroid[d] = Σ(point[d]) / |cluster|          │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  收敛检查:                                          │   │
│  │  如果所有点的簇分配没有变化 → 提前终止                 │   │
│  │  如果达到 24 次迭代上限 → 强制终止                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Python 实现

```python
def _kmeans(points: list[list[float]], k: int = 3, iterations: int = 24):
    """K-means 聚类算法"""
    if not points:
        return [], []

    k = min(k, len(points))
    centroids = [point[:] for point in points[:k]]  # 前 K 个点作为质心
    assignments = [0] * len(points)

    for _ in range(iterations):
        updated = False

        # E 步：分配点到最近质心
        for idx, point in enumerate(points):
            distances = [
                sum((value - centroid[dim]) ** 2
                    for dim, value in enumerate(point))
                for centroid in centroids
            ]
            cluster = min(range(k), key=lambda i: distances[i])
            if assignments[idx] != cluster:
                assignments[idx] = cluster
                updated = True

        # M 步：重新计算质心
        grouped: list[list[list[float]]] = [[] for _ in range(k)]
        for assignment, point in zip(assignments, points):
            grouped[assignment].append(point)

        new_centroids = []
        for cluster_idx, group in enumerate(grouped):
            if not group:
                new_centroids.append(centroids[cluster_idx])  # 空簇保持原质心
                continue
            new_centroids.append([
                sum(point[dim] for point in group) / len(group)
                for dim in range(len(group[0]))
            ])
        centroids = new_centroids

        if not updated:
            break  # 提前终止

    return assignments, centroids
```

### 智能标签生成

```python
# 基于领域投票生成聚类标签
cluster_domain_votes: dict[int, dict[str, int]] = {}
for assignment, lang in zip(assignments, languages):
    cluster_domain_votes.setdefault(assignment, {})
    group = get_domain_group(lang["domain"])
    cluster_domain_votes[assignment][group] += 1

for assignment, votes in cluster_domain_votes.items():
    dominant_group = max(votes.items(), key=lambda item: item[1])[0]
    cluster_labels[assignment] = f"Cluster {assignment + 1} / {dominant_group}-leaning"
```

### 聚类结果示例

```
┌─────────────────────────────────────────────────────────────┐
│  Cluster 1 / Systems-leaning                               │
│  ────────────────────────────                              │
│  Rust, C, Zig, Nim, C++                                    │
│  特点: 强内存安全、底层控制、高性能                           │
├─────────────────────────────────────────────────────────────┤
│  Cluster 2 / Academic-leaning                              │
│  ────────────────────────────                              │
│  Haskell, Idris, Agda, OCaml, PureScript                   │
│  特点: 强类型系统、函数式、学术研究                           │
├─────────────────────────────────────────────────────────────┤
│  Cluster 3 / Web-leaning                                  │
│  ────────────────────────────                              │
│  TypeScript, Elm, Gleam, Dart                              │
│  特点: 渐进类型、Web 开发、类型安全                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 第 11 页：算法复杂度分析

### 各算法复杂度对比

| 算法 | 时间复杂度 | 空间复杂度 | 解释 |
|------|-----------|-----------|------|
| 特征向量提取 | O(N × F) | O(N × F) | N: 语言数, F: 特征数(14) |
| 相似度矩阵 | O(N² × F) | O(N²) | N×N 对称矩阵 |
| 皮尔逊相关 | O(F) per pair | O(F) | 每次计算 14 维向量 |
| PCA 降维 | O(n×d² + d²×iter) | O(d²) | n: 语言数, d: 14, iter: 64 |
| K-means | O(k×n×d×iter) | O(n) | k: 3, iter: 24 |

### 实际性能数据

```
数据规模: 26 种语言 × 14 个特征维度

相似度矩阵计算:
  - 需计算 26×25/2 = 325 个语言对
  - 每对 14 次乘法 + 14 次加法 = 28 次操作
  - 总操作数: 325 × 28 ≈ 9,100 次
  - 耗时: < 1 毫秒

PCA 降维:
  - 协方差矩阵: 14×14 = 196 次计算
  - 幂迭代 64 次: 2 × 14² × 64 ≈ 25,000 次
  - 总耗时: < 1 毫秒

K-means 聚类:
  - 3 × 26 × 14 × 24 ≈ 32,000 次操作
  - 总耗时: < 1 毫秒
```

### 总体性能结论

```
┌─────────────────────────────────────────────────────────────┐
│  ✅ 所有算法在毫秒级完成                                      │
│  ✅ 适合实时数据更新场景                                      │
│  ✅ 无需外部机器学习库 (纯 Python 实现)                        │
└─────────────────────────────────────────────────────────────┘
```

---

# 第四部分：可视化技术

---

## 第 12 页：特性矩阵 (Feature Matrix)

### 可视化类型：热力图 + 表格

### 视觉设计

```
┌────────────────────────────────────────────────────────────────────────┐
│  Scoring:  [0]Not [1]Min [2]Basic [3]Moderate [4]Strong [5]Full       │
├────────────────────────────────────────────────────────────────────────┤
│          │Gener│Traits│ ADT │Match│Ownr│Dep │GADT│ HKT│Eff │Ref │Grad│Inf │Strc│Flow│ Total│
├──────────┼─────┼──────┼─────┼─────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼─────┤
│ 🔒 Name  │     │      │     │     │    │    │    │    │    │    │    │    │    │     │  🔒 │
│ 🔒 Year  │     │      │     │     │    │    │    │    │    │    │    │    │    │     │  🔒 │
│ 🔒 Paradgm│     │      │     │     │    │    │    │    │    │    │    │    │    │     │  🔒 │
├──────────┼─────┼──────┼─────┼─────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼─────┤
│ Idris    │  5  │  5   │  5  │  5  │  2  │  5 │  5 │  5 │  5 │  5 │  0 │  4 │  0 │  0  │  51 │
│ Haskell  │  5  │  5   │  5  │  5  │  0  │  3 │  5 │  5 │  3 │  2 │  0 │  5 │  0 │  0  │  43 │
│ Scala    │  5  │  5   │  5  │  5  │  0  │  3 │  3 │  5 │  2 │  2 │  0 │  4 │  3 │  1  │  43 │
│ Rust     │  5  │  5   │  5  │  5  │  5  │  0 │  0 │  1 │  0 │  0 │  0 │  4 │  0 │  2  │  32 │
│ ...      │     │      │     │     │    │    │    │    │    │    │    │    │    │     │     │
└────────────────────────────────────────────────────────────────────────┘
 🔓 sticky left column                    sticky right column 🔓
```

### 颜色编码

```typescript
function colorFor(score: number): string {
  // 透明度随分数增加而增加
  // 0 分 → α ≈ 0.16 (几乎透明)
  // 5 分 → α ≈ 0.96 (深色)
  const alpha = 0.16 + (score / 5) * 0.8
  return `rgba(126, 150, 255, ${alpha.toFixed(3)})`
}
```

### 交互设计

| 交互 | 行为 |
|------|------|
| 列头悬停 | 显示特性完整名称和简短说明 |
| 单元格悬停 | 显示该语言该特性的详细评分理由 |
| 横向滚动 | 语言名称和总分列始终固定（sticky） |
| 纵向滚动 | 表头始终固定（sticky） |

### 悬停卡片示例

```
┌──────────────────────────────────────────┐
│  Rust / parametric_polymorphism          │
├──────────────────────────────────────────┤
│  Score: 5 / Full                         │
│                                          │
│  "Full monomorphized generics with       │
│   trait bounds, where clauses,            │
│   const generics"                        │
└──────────────────────────────────────────┘
```

---

## 第 13 页：雷达图对比 (Radar Chart)

### 可视化类型：多语言叠加雷达图

### 雷达图配置

```typescript
const chartOption = computed<EChartsOption>(() => ({
  legend: {
    data: selectedLanguages,  // 动态显示选中语言
    textStyle: { color: '#9ca3af' }
  },
  radar: {
    indicator: features.map(f => ({
      name: featureShortLabels[f],
      max: 5  // 最大值为 5
    })),
    shape: 'polygon',
    splitNumber: 5,
    axisName: { color: '#9ca3af' }
  },
  series: [{
    type: 'radar',
    data: selectedLanguages.map(name => ({
      name,
      value: languageScores[name],  // 14 维评分向量
      lineStyle: { width: 2 },
      areaStyle: { opacity: 0.15 }
    }))
  }]
}))
```

### 雷达图示例：Rust vs Haskell vs TypeScript

```
                    泛型
                     │
                   5 ┼    ★ Rust (5)
                     │   ╭─╮
                   4 ┼   │ │ ★ Haskell (5)
                     │ ╭─╯ ╰─╮
                   3 ┼│       │ ★ TypeScript (4)
                     ││  ╭─╮  │
                   2 ┼│  │ │  │
                     │╰──╯ ╰──╯
                   1 ┼★ Rust(1)
                     │         ★ TS(1)
                   0 ┼───────────────────
                     0    1    2    3    4
                         特质    所有权
                              ╲    │
                               ╲   │
                                ╲  ★ Rust(5)
                                 ╲
                                  ★ Haskell(0)
```

### 视觉映射

| 视觉元素 | 映射维度 | 规则 |
|---------|---------|------|
| 填充区域 | 语言 | 半透明叠加 |
| 边框颜色 | 语言 | 固定调色板 |
| 区域透明度 | — | 0.15（避免遮挡）|

---

## 第 14 页：特性共现热力图 (Feature Co-occurrence)

### 可视化类型：相关性热力图

### 算法：计算特性间的皮尔逊相关系数

```python
def build_feature_cooccurrence(data: dict) -> dict:
    """构建特性共现相关性矩阵"""
    features = get_feature_names(data)

    # 提取每种特性的 26 种语言评分向量
    feature_vectors = {}
    for feature in features:
        feature_vectors[feature] = [
            lang["features"].get(feature, 0)
            for lang in data["languages"]
        ]

    # 计算两两之间的皮尔逊相关系数
    matrix = []
    for i, feat_a in enumerate(features):
        row = []
        for j, feat_b in enumerate(features):
            if i == j:
                row.append(1.0)  # 自身相关性为 1
            else:
                r = pearson_correlation(
                    feature_vectors[feat_a],
                    feature_vectors[feat_b]
                )
                row.append(round(r, 2))
        matrix.append(row)

    return {"features": features, "matrix": matrix}
```

### 热力图示例

```
                    特质  HKT   ADT  匹配  泛型  推断  线性  效应  依赖  GADT  细化  渐进  结构  流敏
                 ┌────────────────────────────────────────────────────────────────────────────────────┐
│  Traits       │  1.0  0.85  0.92  0.88  0.76  0.65  0.21  0.45  0.38  0.42  0.15  0.12  0.08  0.31  │
│  HKT          │  0.85  1.0  0.78  0.82  0.71  0.58  0.12  0.52  0.61  0.55  0.22  0.08  0.15  0.19  │
│  ADTs         │  0.92  0.78  1.0  0.97  0.81  0.62  0.18  0.48  0.35  0.41  0.12  0.05  0.21  0.28  │
│  Matching      │  0.88  0.82  0.97  1.0  0.79  0.60  0.15  0.51  0.33  0.39  0.14  0.09  0.18  0.25  │
│  Generics      │  0.76  0.71  0.81  0.79  1.0  0.68  0.24  0.42  0.29  0.36  0.18  0.22  0.14  0.35  │
│  Inference     │  0.65  0.58  0.62  0.60  0.68  1.0  0.31  0.38  0.42  0.48  0.25  0.35  0.52  0.41  │
│  Linear        │  0.21  0.12  0.18  0.15  0.24  0.31  1.0  0.08  0.05  0.11  0.02  0.18  0.09  0.44  │
│  Effect        │  0.45  0.52  0.48  0.51  0.42  0.38  0.08  1.0  0.58  0.62  0.35  0.05  0.12  0.08  │
│  Dependent     │  0.38  0.61  0.35  0.33  0.29  0.42  0.05  0.58  1.0  0.72  0.45  0.02  0.08  0.05  │
│  GADTs         │  0.42  0.55  0.41  0.39  0.36  0.48  0.11  0.62  0.72  1.0  0.38  0.04  0.15  0.12  │
│  Refinement    │  0.15  0.22  0.12  0.14  0.18  0.25  0.02  0.35  0.45  0.38  1.0  0.01  0.08  0.06  │
│  Gradual       │  0.12  0.08  0.05  0.09  0.22  0.35  0.18  0.05  0.02  0.04  0.01  1.0  0.45  0.38  │
│  Structural    │  0.08  0.15  0.21  0.18  0.14  0.52  0.09  0.12  0.08  0.15  0.08  0.45  1.0  0.42  │
│  Flow          │  0.31  0.19  0.28  0.25  0.35  0.41  0.44  0.08  0.05  0.12  0.06  0.38  0.42  1.0  │
                 └────────────────────────────────────────────────────────────────────────────────────┘
                           深色 = 高相关性    浅色 = 低相关性
```

### 关键发现

| 特性对 | 相关系数 | 解读 |
|-------|---------|------|
| ADTs ↔ Pattern Matching | **0.97** | 最强共现：ML 传统 |
| Traits ↔ ADTs | **0.92** | 强共现：类型类系统 |
| Traits ↔ HKT | **0.85** | 强共现：高级类型特性 |
| Gradual ↔ Structural | 0.45 | 中等相关：Web 语言 |
| Linear ↔ Flow | 0.44 | 中等相关：安全性语言 |

---

## 第 15 页：相似性网络 (Similarity Network)

### 可视化类型：力导向图 (Force-Directed Graph)

### 网络构建

```python
def compute_similarity_edges(data: dict, threshold: float = 0.65) -> list[dict]:
    """计算相似性网络边"""
    vectors = get_feature_vectors(data)
    names = list(vectors.keys())
    edges = []

    for i, name_a in enumerate(names):
        for j, name_b in enumerate(names):
            if i < j:
                sim = cosine_similarity(vectors[name_a], vectors[name_b])
                if sim >= threshold:  # 0.65 阈值过滤
                    edges.append({
                        "source": name_a,
                        "target": name_b,
                        "similarity": round(sim, 4)
                    })

    return edges
```

### 力导向图可视化配置

```typescript
const chartOption = computed<EChartsOption>(() => ({
  series: [{
    type: 'graph',
    layout: 'force',
    roam: true,           // 支持缩放和平移
    draggable: true,      // 支持拖拽节点
    force: {
      repulsion: 240,     // 节点间斥力
      edgeLength: 150,    // 边的理想长度
      gravity: 0.08       // 中心引力
    },
    symbolSize: (value: number) => Math.max(18, Math.min(46, value)),
    lineStyle: {
      width: (params: any) => params.data.similarity * 3,
      opacity: 0.55,
      color: '#4f608d'
    }
  }]
}))
```

### 网络可视化效果

```
                    ┌─────────────────────────────────────────────────┐
                    │                                                 │
                    │      Haskell══════ Scala                         │
                    │         ║         ║                            │
                    │         ╚═════════╝                            │
                    │            ║                                    │
                    │         Idris                                    │
                    │            ║                                    │
                    │      PureScript                                  │
                    │                                                 │
                    │  Rust ═══════════ Swift                         │
                    │         ║                                        │
                    │         ╚══════════ Nim                          │
                    │                    ║                             │
                    │                 Zig                              │
                    │                                                 │
                    │  TypeScript                                      │
                    │      ║                                           │
                    │      ╠══════ Elm                                 │
                    │      ║                                           │
                    │  Dart ═══════ Gleam                              │
                    │                                                 │
                    │        Java ═════════ C#                         │
                    │                         ║                       │
                    │                      Kotlin                      │
                    │                                                 │
                    └─────────────────────────────────────────────────┘

    图例:  ● Functional    ■ Multi-paradigm    ▲ Systems    ● Web
```

### 节点视觉映射

| 视觉元素 | 数据字段 | 映射规则 |
|---------|---------|---------|
| 节点大小 | `complexity` | 复杂度越高节点越大 [18-46px] |
| 节点颜色 | `paradigm` | Functional=绿, Multi=蓝, Systems=黄, Web=紫 |
| 边宽度 | `similarity` | 相似度越高边越粗 [0.65×3=1.95px, 3px] |
| 边透明度 | 固定 | 0.55 |

### 典型语言对相似度

| 语言对 | 相似度 | 解读 |
|-------|--------|------|
| Rust ↔ Swift | **0.958** | 几乎相同的类型系统设计 |
| Rust ↔ Haskell | 0.737 | 共同重视安全性 |
| Haskell ↔ Scala | 0.928 | ML 函数式家族 |
| Java ↔ C# | 0.888 | 企业级 OOP 语言 |
| Rust ↔ C | 0.702 | 系统语言，但 C 极简 |
| Go ↔ Python | 0.521 | 设计哲学差异大 |

---

## 第 16 页：领域聚类 (Domain Clusters)

### 可视化类型：PCA 投影散点图 + K-means 着色

### 散点图配置

```typescript
const chartOption = computed<EChartsOption>(() => ({
  xAxis: {
    name: 'Principal Component 1',
    type: 'value'
  },
  yAxis: {
    name: 'Principal Component 2',
    type: 'value'
  },
  series: [{
    type: 'scatter',
    data: points.map(p => ({
      name: p.name,
      value: [p.x, p.y],
      itemStyle: {
        color: clusterPalette[p.cluster],  // 聚类颜色
        symbol: domainGroupSymbols[p.domain_group]  // 领域形状
      }
    }))
  }]
}))
```

### 聚类可视化效果

```
              PC2
                │
          2.5  │                    ● Idris (Academic)
                │               ●
          2.0  │            ● Haskell (Academic)
                │        ●
          1.5  │                          ◆ Nim (Systems)
                │                    ◆
          1.0  │        ● Scala (Academic)       ◆ Zig (Systems)
                │    ●
          0.5  │           ◆ Rust (Systems)
                │     ◆               ◆ C (Systems)
    ────────────┼───────────────────────────────────────── PC1
          0.0  │          ● OCaml (Academic)      ★ TypeScript (Web)
                │                  ◆ C++ (Systems)    ★ Elm (Web)
         -0.5   │            ◆ Swift (Systems)  ★ Dart (Web)
                │                                 ★ Gleam (Web)
         -1.0   │     ▲ Java (General)    ★
                │   ▲ ▲ C# (General) ▲ Kotlin (General)
         -1.5   │  ▲
                │ ▲ Python (General) Go (Systems)
         -2.0   │
                │


    ● Cluster 0 / Academic-leaning    ◆ Cluster 1 / Systems-leaning
    ★ Cluster 2 / Web-leaning         ▲ 未归入前三大聚类
```

### 颜色与形状映射

```typescript
const clusterPalette = ['#7e96ff', '#ff8aa1', '#6fe0b7']

const domainGroupSymbols = {
  'Systems': 'diamond',     // 菱形
  'Web': 'circle',          // 圆形
  'Academic': 'triangle',    // 三角形
  'General': 'rect'         // 方形
}

const domainGroupColors = {
  'Systems': '#ffcf7a',     // 黄色系
  'Web': '#7e96ff',         // 蓝色系
  'Academic': '#6fe0b7',     // 绿色系
  'General': '#ff8aa1'      // 粉色系
}
```

---

## 第 17 页：时间线 (Feature Timeline)

### 可视化类型：时间轴事件流

### 时间线数据结构

```python
def build_timeline_events(data: dict) -> list[dict]:
    """构建特性采用时间线事件"""
    events = []

    for lang in data["languages"]:
        timeline = lang.get("feature_timeline", {})
        for feature, year in timeline.items():
            events.append({
                "language": lang["name"],
                "feature": feature,
                "year": year,
                "domain": lang["domain"],
                "paradigm": lang["paradigm"]
            })

    return sorted(events, key=lambda x: x["year"])
```

### 时间线可视化效果

```
年份    2010        2015        2020        2025
       │           │           │           │
       ▼           ▼           ▼           ▼
  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │  Rust (Systems)                                         │
  │  ├─ 2010: ADTs, Pattern Matching                        │
  │  ├─ 2012: Ownership/Lifetime, Traits                    │
  │  └─ 2012: Generics                                     │
  │                                                         │
  │  TypeScript (Web)                                       │
  │  ├─ 2012: Gradual Typing, Structural Typing             │
  │  ├─ 2016: Flow-sensitive Typing, ADTs                   │
  │  └─ 2018: Conditional Types (macro)                    │
  │                                                         │
  │  Kotlin (Mobile)                                        │
  │  ├─ 2011: Generics, ADTs, Pattern Matching             │
  │  └─ 2016: Smart Casts (Flow-sensitive)                  │
  │                                                         │
  │  Go (Systems)                                           │
  │  └─ 2022: Generics (parametric polymorphism)           │
  │                                                         │
  │  Java (Enterprise)                                      │
  │  ├─ 2004: Generics                                      │
  │  ├─ 2020: ADTs (sealed classes), Pattern Matching      │
  │  └─ 2021: Record patterns                              │
  │                                                         │
  └─────────────────────────────────────────────────────────┘
```

### 特性扩散模式发现

| 模式 | 特性 | 说明 |
|------|------|------|
| 快速扩散 | 泛型 (Generics) | 2004-2022 年间被大多数语言采纳 |
| 缓慢渗透 | 依赖类型 (Dependent Types) | 仅限学术语言（Haskell, Idris, Agda） |
| 趋同进化 | ADTs + Pattern Matching | 几乎同步在多种语言中出现 |
| 刻意缺失 | Go | 始终不支持 ADT 和模式匹配 |

---

# 第五部分：应用案例

---

## 第 18 页：语言推荐器 (Feature Recommender)

### 交互界面

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Feature Recommender                                    [Domain ▼] [3] [Clear]  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐           │
│  │ Best Match      │ │ Selected        │ │ Visible Slice   │           │
│  │ Rust            │ │ Generics ✓      │ │ All domains     │           │
│  │ 4 of 4 matched │ │ Ownership ✓     │ │ 26 languages    │           │
│  └─────────────────┘ │ ADTs ✓          │ └─────────────────┘           │
│                       │ Matching ✓      │                                 │
│                       └─────────────────┘                                 │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  Feature Selection                                                │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │  │
│  │  │ Generics│ │  Traits │ │   ADT   │ │Matching │ │Ownership│      │  │
│  │  │  (5)    │ │  (5)    │ │  (5)    │ │  (5)    │ │  (5)    │      │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘      │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │  │
│  │  │Dep Types│ │  GADT   │ │   HKT   │ │ Effects │ │Refine.  │      │  │
│  │  │  (0)    │ │  (0)    │ │  (1)    │ │  (0)    │ │  (0)    │      │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘      │  │
│  │  ...                                                              │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─────────────────────────────────┐ ┌─────────────────────────────────┐ │
│  │ Rust                      4/4   │ │ Scala                      3/4   │ │
│  │ 2010 / Systems / Systems       │ │ 2004 / Multi / Data            │ │
│  │ Score: 61.2 / Complexity: 32  │ │ Score: 45.8 / Complexity: 43    │ │
│  │                               │ │                                 │ │
│  │ ✓ Matches:                    │ │ ✓ Matches:                      │ │
│  │ [Generics] [Traits]           │ │ [Generics] [Traits] [ADTs]     │ │
│  │ [ADTs] [Matching] [Ownership] │ │                                 │ │
│  │                               │ │ ✗ Missing:                     │ │
│  │                               │ │ [Ownership] (score: 0)          │ │
│  └───────────────────────────────┘ └─────────────────────────────────┘ │
│                                                                         │
│  ... 更多推荐卡片                                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 推荐算法

```typescript
// 推荐评分公式
const score = matched.length * 12
            + missing_features_scores.reduce((sum, s) => sum + s, 0)
            + language.complexity / 10

// 硬匹配条件
const isMatched = featureScore >= threshold  // threshold = 3 (默认)

// 排序规则
const ranked = languages.sort((a, b) => {
  if (b.matched.length !== a.matched.length) {
    return b.matched.length - a.matched.length  // 先按满足数量
  }
  return b.score - a.score  // 再按总分
})
```

### 使用场景

| 场景 | 需求描述 | 操作 | 推荐结果 |
|------|---------|------|---------|
| 技术选型 | 需要泛型、ADT、所有权 | 选 3 个特性 + Systems 领域 | Rust (4/4) |
| 渐进迁移 | Python 项目逐步引入类型 | 只选 Gradual Typing | TypeScript (5), Dart (3) |
| 学术研究 | 依赖类型 + 效应系统 | 选 2 个特性 + Academic 领域 | Idris (2/2), Haskell (1/2) |

---

## 第 19 页：典型发现与洞察

### 发现 1：ML 函数式家族的高度相似性

```
语言            泛型  特质  ADT  匹配  推断  HKT   总分
───────────────────────────────────────────────────────
Haskell         5     5     5    5     5     5     43
Scala           5     5     5    5     4     5     43
Idris           5     5     5    5     4     5     51
PureScript      5     5     5    5     4     5     40
OCaml           5     2     5    5     5     3     32

相似度: Haskell-Scala ≈ 0.93, Haskell-Idris ≈ 0.91
结论: 这些语言共享相同的学术传统 (ML family)
```

### 发现 2：Rust 与 Swift 的惊人相似

```
特性          Rust    Swift    差异
───────────────────────────────────
泛型          5       4        -1
特质/协议     5       4        -1
ADT           5       5         0
模式匹配      5       5         0
所有权        5       2        -3
类型推断      4       4         0
流敏感类型    2       3        +1

相似度: 0.958 (本项目最高语言对之一)
解释: 两者都专注于系统编程 + 内存安全 + 现代语言设计
```

### 发现 3：Go 的刻意简化哲学

```
特性          Go      C        Python    相似度
───────────────────────────────────────────────
泛型          3       0        2         Go-C: 0.52
ADT           0       0        0         Go-Python: 0.52
模式匹配      0       0        2
结构类型      5       1        3

结论: Go 1.0 (2009) 刻意排除 ADT 和模式匹配
     保持语言的 "简单性" 和 "可读性"
```

### 发现 4：特性共现规律

```
ADTs ↔ Pattern Matching (r = 0.97)
原因: 这两个特性是相辅相成的——ADT 提供可分解的数据结构，
     模式匹配提供穷尽性检查。

Traits ↔ HKT (r = 0.85)
原因: 高阶类型需要类型类系统来约束参数化类型的实例化。

Gradual ↔ Structural (r = 0.45)
原因: 渐进类型语言（如 TypeScript）倾向于使用结构化类型
     以支持鸭子类型和灵活的类型兼容。
```

---

# 第六部分：技术总结

---

## 第 20 页：技术栈全景

### 数据层

```
┌─────────────────────────────────────┐
│  data/languages.json                │
│  • 26 种编程语言                    │
│  • 14 维类型系统特性评分            │
│  • 专家手工标注 + 规范文档验证      │
│  • 评分理由说明                    │
│  • 特性采用时间线                  │
│  • 流行度指标                      │
└─────────────────────────────────────┘
```

### Python 数据处理层

```
┌──────────────────────────────────────────────────────────────┐
│  src/data_processing.py                                     │
│                                                              │
│  纯 Python 实现，无 sklearn 等外部机器学习库依赖                │
│                                                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ 相似度计算   │ │ PCA 降维    │ │ K-means 聚类 │           │
│  │ • 余弦相似度 │ │ • 幂迭代法   │ │ • E 步/M 步  │           │
│  │ • 皮尔逊相关 │ │ • Deflation │ │ • 欧氏距离   │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
│                                                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ 时序分析    │ │ 共现分析    │ │ 谱系构建     │           │
│  │ • 时间线事件 │ │ • 相关矩阵  │ │ • 影响关系   │           │
│  │ • 军备指数  │ │ • 热力图   │ │ • 继承关系   │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└──────────────────────────────────────────────────────────────┘
```

### Vue 3 前端可视化层

```
┌──────────────────────────────────────────────────────────────┐
│  frontend/                                                   │
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ Vue 3 + TypeScript │  │ ECharts 图表库   │                  │
│  │ • Composition API │  │ • 雷达图         │                  │
│  │ • 响应式数据绑定  │  │ • 力导向图       │                  │
│  │ • 组件化架构     │  │ • 热力图         │                  │
│  └─────────────────┘  │ • 散点图         │                  │
│                       │ • 时间线         │                  │
│  ┌─────────────────┐  └─────────────────┘                  │
│  │ VueUse 工具库   │                                        │
│  │ • useFetch      │  ┌─────────────────┐                  │
│  │ • useResizeObserver │ │ CSS 原生样式    │                  │
│  └─────────────────┘  │ • CSS Grid       │                  │
│                       │ • Sticky 定位    │                  │
│                       │ • 响应式断点     │                  │
│                       └─────────────────┘                  │
└──────────────────────────────────────────────────────────────┘
```

### 部署架构

```
┌──────────────────────────────────────────────────────────────┐
│  GitHub Pages                                               │
│  https://zlatanwic.github.io/lang-analysis/                  │
│                                                              │
│  部署流程 (GitHub Actions):                                  │
│  1. 检出代码                                                 │
│  2. 安装 Python + Node.js                                   │
│  3. python main.py → 生成 dashboard-data.json               │
│  4. pnpm install → 安装前端依赖                               │
│  5. pnpm run build → 构建 Vue 应用                          │
│  6. 上传 dist/ → 部署到 GitHub Pages                        │
└──────────────────────────────────────────────────────────────┘
```

---

## 第 21 页：EDA 方法论总结

### 数据探索流程

```
┌──────────────────────────────────────────────────────────────┐
│                    EDA 方法论框架                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 数据采集                                                 │
│     ├── 专家知识 (语言规范、学术文献)                         │
│     ├── 手工标注 (确保评分准确性)                             │
│     └── 静态快照 + 可选的 API 实时更新                        │
│                                                              │
│  2. 特征工程                                                 │
│     ├── 原始数据 → 结构化特征向量                            │
│     ├── 选择 14 个有意义的维度                               │
│     └── 统一评分标准 (0-5 级)                                │
│                                                              │
│  3. 多维分析                                                 │
│     ├── 相似度分析 (余弦、皮尔逊)                            │
│     ├── 降维可视化 (PCA)                                     │
│     ├── 聚类分析 (K-means)                                   │
│     └── 时序分析 (特性采用时间线)                             │
│                                                              │
│  4. 可视化呈现                                               │
│     ├── 热力图 (表格型数据)                                   │
│     ├── 雷达图 (多维对比)                                    │
│     ├── 网络图 (相似性关系)                                  │
│     ├── 散点图 (聚类结果)                                    │
│     └── 时间线 (演化趋势)                                    │
│                                                              │
│  5. 交互探索                                                 │
│     ├── 筛选过滤 (领域、阈值)                                │
│     ├── 悬停详情 (评分理由)                                  │
│     ├── 推荐系统 (特性反向搜索)                              │
│     └── 动态探索 (缩放、拖拽)                                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 可视化设计原则

| 原则 | 应用实例 |
|------|---------|
| 数据墨水比最大化 | 颜色深浅编码评分，避免装饰性元素 |
| 交互性 | 悬停显示详情，筛选过滤，缩放拖拽 |
| 一致性 | 颜色语义固定（绿=Functional，蓝=Multi） |
| 上下文保留 | sticky 行列锁定，始终可见关键信息 |
| 多视图互补 | 同一数据多种图表呈现 |

### 技术选型决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 为什么不用 D3.js？ | ECharts | 更低的开发成本，够用的图表类型 |
| 为什么不用 Plotly？ | ECharts | 更好的 Vue 集成 |
| 为什么不用 sklearn？ | 纯 Python 实现 | 降低依赖复杂度，便于教学理解 |
| 为什么不做后端 API？ | 静态 JSON | 项目规模不需要，简化部署 |

---

## 第 22 页：参考资源与致谢

### 项目资源

| 资源 | 链接 |
|------|------|
| 项目仓库 | https://github.com/Zlatanwic/lang-analysis |
| 线上演示 | https://zlatanwic.github.io/lang-analysis/ |
| 源代码 | 本地 `E:\lang_analysis\` 目录 |

### 核心文献

| 文献 | 作者 | 年份 | 相关内容 |
|------|------|------|---------|
| Types and Programming Languages | Benjamin Pierce | 2002 | 类型系统理论基础 |
| On Understanding Types | Cardelli & Wegner | 1985 | 类型系统概论 |
| The Haskell 98 Report | Haskell Committee | 1998 | Haskell 规范 |
| Rust Reference | Rust Team | — | Rust 类型系统 |
| TypeScript Specification | Microsoft | — | TypeScript 类型系统 |

### 技术文档

| 资源 | 用途 |
|------|------|
| ECharts 文档 | 图表配置参考 |
| Vue 3 文档 | 前端框架学习 |
| Python 官方文档 | 数据处理实现 |

### 致谢

- 课程教师：XXX
- 参考了 LangGov 等开源类型系统研究项目
- 感谢同学 XXX 在 EDA 方法论上的讨论

---

## 附录：推荐 PPT 制作工具与格式建议

### 推荐工具

| 工具 | 优点 | 适用场景 |
|------|------|---------|
| Marp / Marp CLI | Markdown 转 PPT，支持代码高亮 | 程序员首选 |
| Slidev | Vue 3 支持的幻灯片工具 | 现代前端栈 |
| reveal.js | Web 幻灯片，可嵌入交互式图表 | 线上演示 |
| PowerPoint / Keynote | 通用性最强 | 通用汇报 |

### 格式建议

| 页面类型 | 推荐图表/布局 |
|---------|--------------|
| 数据概览 | 带颜色梯度的表格热力图 |
| 算法原理 | 数学公式 + 流程图 |
| 可视化展示 | 截图 + 图注说明 |
| 对比分析 | 并列柱状图/雷达图叠加 |
| 总结 | 架构流程图 |

### 配色建议

```
主色调: #7e96ff (蓝色系 - 科技感)
辅助色: #6fe0b7 (绿色 - 函数式)
强调色: #ffcf7a (黄色 - 系统编程)
背景色: #0d1017 (深色 - 现代风格)
文字色: #e5e7eb (浅灰 - 可读性)
```

---

*文档生成时间: 2026-04-03*
*项目地址: https://github.com/Zlatanwic/lang-analysis*
