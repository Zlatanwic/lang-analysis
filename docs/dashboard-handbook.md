# Lang Analysis Dashboard 使用手册

这是一份面向仓库读者、项目维护者和 dashboard 使用者的长篇说明文档。它主要回答以下问题：

- 这个项目为什么存在
- 数据集是怎么组织的
- 14 个类型系统特性分别意味着什么
- 数据集里的各门语言大致代表什么设计路线
- 每一个 panel 在展示什么、应该怎么读
- 从这些图表里通常可以得出哪些结论

这份文档的目标不是重复界面文案，而是把 dashboard 背后的分析模型讲清楚。

## 1. 项目背景

这个项目试图从“类型系统设计”的角度研究编程语言，而不是只看：

- 语法风格
- 社区热度
- 生态规模
- 性能印象

核心问题是：

不同语言在类型系统的表达力、安全性、工程可用性和学习成本之间，分别做了怎样的取舍？

这个问题之所以重要，是因为“类型系统强不强”并不是单一维度。不同语言强调的重点完全不同：

- 有的语言追求证明能力和类型级表达力
- 有的语言强调工程安全，尤其是内存与资源安全
- 有的语言强调渐进 adoption，希望动态语言用户能低摩擦进入静态类型世界
- 有的语言故意保持类型系统克制，以换取更低的复杂度和更高的可维护性

这个仓库的做法，是把这些取舍整理成结构化数据，再通过 Vue dashboard 可视化出来。

当前数据集大致覆盖：

- 26 门语言
- 14 个类型系统特性维度
- 每门语言的评分理由
- 特性进入语言的时间线
- 一组人工整理的语言影响关系
- 一组轻量级的流行度参考指标

因此，这个项目最适合被理解成：

一个围绕“编程语言类型系统设计”构建的分析型知识图谱。

## 2. 这个数据集到底在测什么

这份数据集并不是在给语言做“好 / 坏”排名，它真正测量的是：

一门语言在若干类型系统维度上，走到了多远。

这里有三个前提非常重要。

### 2.1 复杂度不等于质量

总分高，不代表语言一定“更好”。

例如：

- `Idris` 分数极高，是因为它把 dependent types、refinement-like reasoning、effect tracking 等前沿能力都纳入了语言核心
- `Go` 分数偏低，是因为它刻意回避很多高级类型系统机制

这并不意味着 Idris 在所有工程场景里都比 Go 更合适。它只意味着：

Idris 探索了更大的类型系统设计空间，而 Go 更强调约束和简化。

### 2.2 缺失很多时候是主动设计，不是技术落后

很多语言没有某个特性，并不是“做不到”，而是“没打算这么做”。

例如：

- `Go` 避开 ADT 和 pattern matching，是为了保持语言简单、可预测
- `Elixir` 保持较弱的静态类型能力，是因为它把运行时灵活性和 BEAM 的并发模型放在更高优先级
- `TypeScript` 把 gradual typing 放在核心，是因为它的历史使命就是在 JavaScript 世界中渐进落地类型系统

### 2.3 分数既考虑理论能力，也考虑产品化程度

一个特性可能：

- 原生存在于语言核心
- 通过扩展存在
- 通过外部工具或库部分实现
- 虽然“能做”，但不够自然、不够好用

这就是为什么这里使用 `0-5` 的渐进分值，而不是简单的 `yes/no`。

## 3. 评分模型

当前 dashboard 使用六档评分：

- `0`：完全缺失
- `1`：只有极弱、边缘或非官方支持
- `2`：有基本形式，但限制较多
- `3`：常见场景可用，但仍有明显缺口
- `4`：集成度高，只有少量不足
- `5`：同类中最强，或者可以作为该能力的代表实现

这个模型意味着：

- 一个特性即便存在，也可能因为产品化不完整而只拿到中分
- 一个特性即便不是核心，也可能因工具生态而拿到低分而非 0 分
- 一个语言在某个方向拿到 5 分，通常意味着它在这一维上具有“定义类别”的意味

例如：

- `Rust` 在 ownership 上是 `5`，因为 ownership / borrow checking 就是它最核心的语言身份
- `Haskell` 在 HKT 上是 `5`，因为它的抽象体系大量建立在这之上
- `TypeScript` 在 gradual typing 上是 `5`，因为这是它区别于传统静态语言的核心能力
- `Ruby` 在 gradual typing 上只有 `2`，因为它更多依赖 RBS / Sorbet 这类外围方案，而不是统一的原生体验

## 4. 14 个类型系统特性说明

这一节相当于 dashboard 的术语表。

### 4.1 参数多态 / 泛型

英文：`Generics / parametric polymorphism`

问题本质：

能不能写一份逻辑，在不牺牲类型安全的前提下复用于多种类型？

典型表现：

- 泛型函数
- 泛型容器
- 带约束的类型参数

为什么重要：

- 它是现代静态语言可复用抽象的基础
- 很多语言即使不追求理论前沿，也至少会把这一层做好

### 4.2 Ad hoc polymorphism

英文：`Trait / typeclass / interface-based polymorphism`

问题本质：

能不能为“同一抽象行为”提供按类型分发的结构化机制？

常见形式：

- Rust `trait`
- Haskell `type class`
- 各类 interface / protocol 机制
- 某些语言中的多重派发

为什么重要：

- 它决定了行为抽象的 extensibility
- 它往往比单纯泛型更接近“真实工程复用”

### 4.3 代数数据类型

英文：`Algebraic data types`

问题本质：

能不能把一个值建模成“若干变体中的一个”，并且每个变体都能带自己的数据？

典型形式：

- Haskell `data`
- Rust `enum`
- F# discriminated union
- TypeScript discriminated union

为什么重要：

- ADT 是建模状态机、协议状态、业务领域对象最干净的方式之一

### 4.4 模式匹配

英文：`Pattern matching`

问题本质：

能不能基于值的结构、构造器或标签进行解构分支，并最好带 exhaustiveness 检查？

为什么重要：

- 它通常和 ADT 成对出现
- 它把“良好的数据建模”真正转化成“良好的控制流表达”

### 4.5 所有权 / 生命周期 / 借用检查

英文：`Ownership / lifetime / borrow checking`

问题本质：

类型系统能不能追踪资源别名、生命周期和 move 语义？

为什么重要：

- 这是无 GC 条件下实现内存安全的最强技术路径之一
- 也是非常难真正产品化的设计方向

### 4.6 依值类型

英文：`Dependent types`

问题本质：

类型能不能依赖值？

为什么重要：

- 这会让类型系统从“普通静态检查”走向“更强的证明能力”
- 它是很多高阶形式化能力的基础

### 4.7 GADT

英文：`Generalized algebraic data types`

问题本质：

构造器能不能比普通 ADT 更精确地约束和收窄类型信息？

为什么重要：

- GADT 往往意味着语言已经在向更精细的类型级表达迈进
- 在函数式和研究型生态里尤其关键

### 4.8 高阶 kind

英文：`Higher-kinded types`

问题本质：

类型系统能不能抽象“类型构造器”本身，而不只是具体类型？

为什么重要：

- 这是很多函数式抽象体系的核心
- 没有 HKT，就很难自然表达一整套通用类型类抽象

### 4.9 效应系统

英文：`Effect systems`

问题本质：

类型系统能不能把副作用、效应或 effectful computation 以某种结构追踪出来？

为什么重要：

- 它试图让“副作用”成为类型级可见的一部分
- 它是普通静态类型之后的重要前沿方向

### 4.10 精化类型

英文：`Refinement types`

问题本质：

能不能在类型之上再附加逻辑谓词，把一个类型约束得更精细？

为什么重要：

- 它连接了静态类型与轻量形式化验证
- 对业务不变量和安全约束特别有意义

### 4.11 渐进类型

英文：`Gradual typing`

问题本质：

静态类型和动态类型代码能不能有意共存？

为什么重要：

- 它是从动态生态向静态生态迁移时最关键的桥梁之一
- 在 Web、脚本和大规模存量代码世界里尤其重要

### 4.12 类型推断

英文：`Type inference`

问题本质：

编译器能自动推断多少，而不要求程序员写大量类型标注？

为什么重要：

- 推断能力直接决定“静态类型是否还好写”
- 它往往比单个高级特性更影响日常体验

### 4.13 结构类型

英文：`Structural typing`

问题本质：

类型兼容性能不能基于形状，而不是基于显式声明的名字？

为什么重要：

- 对开放接口、组件拼装、API 建模特别友好
- 很适合大型前端和多接口系统

### 4.14 流敏感类型

英文：`Flow-sensitive typing`

问题本质：

类型系统能不能随着控制流动态收窄类型？

为什么重要：

- 对 union、nullable、动态值、逐步收窄尤其关键
- TypeScript 和 Kotlin 在这一维上都非常有代表性

## 5. 当前数据集里能先看到的一些总体模式

即使不看单个 panel，仅从数据分布上也能观察到一些全局趋势。

### 5.1 表达力最高的一批语言

按总分看，当前数据集中的前列语言包括：

- Idris：51
- Haskell：43
- Scala：43
- OCaml：37
- PureScript：35
- Rust：32
- TypeScript：32
- Roc：29

这意味着：

- 研究导向和 ML-family 语言仍然占据理论表达力高地
- Rust 不是靠 dependent types 进入高分区，而是靠 systems safety + ADT + trait + match 的组合
- TypeScript 进入高分区，则主要依赖 structural typing、gradual typing 和 flow-sensitive typing 这条“工程实用路线”

### 5.2 最普遍的特性

当前数据集中，非零覆盖度最高的特性大致包括：

- ad hoc polymorphism：24 门语言
- pattern matching：24 门语言
- type inference：23 门语言
- parametric polymorphism：22 门语言
- algebraic data types：21 门语言

这说明：

- 现代语言设计已经越来越收敛到一组基础能力组合
- pattern matching 已经不再只属于纯函数式语言
- inference 已经从“高级能力”变成“基本体验要求”

### 5.3 关联最强的特性对

当前数据里相关性很高的组合包括：

- ADT 与 type inference
- generics 与 type inference
- dependent types 与 refinement-like reasoning
- generics 与 ADT
- ADT 与 pattern matching
- GADT 与 HKT

这意味着：

- 很多高级特性不是独立出现，而是成套出现
- 有些组合已经进入主流语言设计
- 有些组合则仍然停留在更小的研究型生态里

### 5.4 一个明显的“加速时刻”

当前 arms race 聚合结果里，峰值年份是 `2011`，当年有 `16` 个特性到达事件。

这个信号很重要，因为它说明：

- 类型系统创新不再只是零星学术事件
- 一批现代语言在这个时间段附近集中进入“更强类型系统”的竞争阶段

## 6. 当前数据集里的语言画像

这一节不逐行复述分数，而是从设计路线角度给每门语言一个大致定位。

### 6.1 系统与安全导向语言

- `Rust`：生产级 systems 语言里最强的 ownership + ADT + trait + matching 组合代表。
- `Go`：极简系统路线代表，有接口与泛型，但避免复杂类型系统堆叠。
- `C`：现代类型系统能力的基线对照组，说明经典 systems 语言原生类型能力有多克制。
- `Zig`：通过 comptime 打开了非常独特的表达空间，但抽象机制不像 Rust / Haskell 那样制度化。
- `C++`：能力很多，但来自长期演化叠加，不像较新语言那样统一、整洁。
- `Swift`：比很多主流 OO 语言更强，尤其在 enum、pattern matching、protocol-oriented design 上非常突出。
- `Nim`：位于 systems、脚本与元编程之间，具备不少有趣能力，但还不是理论前沿型语言。

### 6.2 ML-family 与研究型语言

- `Haskell`：ADTs、type classes、HKT、GADTs、inference 的经典代表。
- `Idris`：当前数据集中表达力最高，因为 full dependent types 几乎能覆盖更弱的许多机制。
- `OCaml`：非常强的 ML 工程化路线，ADT、match、inference 一流，并且引入了 effect handlers。
- `F#`：ML 思想在 CLR 上的工程化落地，推断和 union 非常强，但前沿程度低于 Haskell / OCaml。
- `Elm`：为前端做了大量简化的函数式类型系统，ADT、match、inference 强，但抽象面更窄。
- `PureScript`：比 Elm 更接近 Haskell，拥有 type classes、HKT 和 effect rows。
- `Gleam`：在 BEAM 上的极简类型语言，ADT 和 inference 很强，但故意保持能力面收敛。
- `Roc`：现代产品导向函数式语言，强调 inference、tag union、structural openness 和更友好的使用体验。

### 6.3 JVM / CLR / 主流 multiparadigm 语言

- `Scala`：实用世界里非常强的复杂类型系统代表。
- `Kotlin`：偏实用主义，sealed hierarchy、inference、flow typing 很强，但不追求函数式理论前沿。
- `Java`：在 records、pattern matching 等方向持续现代化，但整体仍更保守。
- `C#`：近年现代化很快，pattern matching 和实用类型特性增长显著。

### 6.4 Web 与渐进类型语言

- `TypeScript`：结构类型、渐进类型和流敏感分析的代表语言。
- `Dart`：移动 / Web 工程导向，近年来 sealed / pattern 体系补强明显。
- `Python`：静态类型能力整体较弱，但在 optional typing 和工具生态上有重要现实意义。
- `Ruby`：仍然主要是动态语言，但 pattern matching 和 typed overlay 正在增长。
- `Elixir`：本质上仍是动态世界的一员，但在 pattern matching 上极强。
- `Clojure`：以运行时灵活性为主，但 multimethod / protocol 风格的行为抽象很突出。

### 6.5 特殊定位语言

- `Julia`：在 ad hoc polymorphism 上异常强，因为 multiple dispatch 本身就是语言核心。

## 7. 推荐的 dashboard 阅读顺序

如果第一次接触这个 dashboard，建议按下面顺序阅读：

1. `Feature Matrix`
2. `Feature Co-occurrence Matrix`
3. `Radar Comparison`
4. `Feature Timeline`
5. `Type-System Arms Race Index`
6. `Similarity Network`
7. `Domain Clusters`
8. `Feature Diffusion`
9. `Language Evolution Lineage`
10. `Popularity Analysis`
11. `Interactive Feature Recommender`

这样读的好处是：

- 先看静态事实
- 再看特性结构
- 再看时间维度
- 再看空间聚类与扩散关系
- 最后回到现实世界的流行度和选型决策

## 8. 每一个 Panel 在讲什么、做什么、能得出什么结论

这一节是这份手册的核心。

每个 panel 都按三个角度来讲：

- 它展示什么
- 应该怎么读
- 通常能支持哪些结论

### 8.1 Feature Matrix

对应文件：

- [`frontend/src/components/panels/FeatureMatrixPanel.vue`](/e:/lang_analysis/frontend/src/components/panels/FeatureMatrixPanel.vue)

它展示什么：

- 所有语言与所有特性的总览矩阵
- 每个单元格是该语言在该特性上的分数
- 最右侧是总复杂度分
- hover 可查看该语言在该特性上的详细评分理由

它在做什么：

- 提供最原始、最密集的“全局对照表”
- 把 26 门语言 x 14 个特性收进一个可以直接横向比较的视图里

应该怎么读：

- 横向看一行：理解一门语言的完整类型系统画像
- 纵向看一列：理解某个特性在整个语言集合中的普及程度与强度
- 看最右侧总分：快速区分“广覆盖表达力强”和“刻意克制”的语言
- 用 tooltip：理解某个 `3` 为什么不是 `4`，某个 `1` 为什么不是 `0`

它最适合回答什么问题：

- 哪些语言总体更“复杂 / 丰富”
- 哪些语言在某些特性上特别突出
- 哪些语言是明显的 outlier

通常能得出的结论：

- Idris、Haskell、Scala、OCaml、PureScript 属于表达力前沿带
- Rust 很特殊，它不是每一项都顶格，但在 systems 语言里异常均衡
- Go 和 C 的低分更多反映的是设计取舍，而非能力落后
- TypeScript 的高分不是来自 theorem-oriented 类型能力，而是来自工程实用能力组合

### 8.2 Feature Co-occurrence Matrix

对应文件：

- [`frontend/src/components/panels/FeatureCooccurrencePanel.vue`](/e:/lang_analysis/frontend/src/components/panels/FeatureCooccurrencePanel.vue)

它展示什么：

- 14 个特性之间的相关性热力图
- tooltip 同时显示：
  - 相关系数
  - 两个特性同时出现于多少语言
  - 各自覆盖多少语言
- 顶部还有最强特性配对摘要卡

它在做什么：

- 从“语言”视角切换到“特性”视角
- 不再问“某门语言有什么”，而是问“哪些特性倾向一起出现”

应该怎么读：

- 先看对角线：它表示单个特性的普及度 / 支持面
- 再看非对角线：颜色越偏正，两个特性越倾向共同出现
- 再结合 tooltip 里的 shared languages，看这是“广泛共现”还是“少数高端语言的小圈子共现”

它最适合回答什么问题：

- ADT 和 pattern matching 是不是常常一起出现
- HKT 和 GADT 这种高级功能是不是一旦出现就经常成对出现
- dependent types 和 refinement reasoning 是否集中在小众研究型语言中

通常能得出的结论：

- ADT 与 pattern matching 是稳定组合
- generics 与 type inference 已经是现代语言的常见搭配
- dependent types 与 refinement reasoning 仍然是小范围高关联簇
- HKT / GADT 代表的是更高阶函数式抽象栈，而不是零散能力点

### 8.3 Radar Comparison

对应文件：

- [`frontend/src/components/panels/RadarComparisonPanel.vue`](/e:/lang_analysis/frontend/src/components/panels/RadarComparisonPanel.vue)

它展示什么：

- 最多四门语言在 14 个特性维度上的雷达图对比

它在做什么：

- 把矩阵中不容易一眼看到的“形状差异”直接可视化

应该怎么读：

- 不要只看面积，要看轮廓
- 尖刺型轮廓意味着强烈偏科或强烈 specialization
- 圆润型轮廓意味着整体能力更均衡

它最适合回答什么问题：

- 两门语言总分接近，但设计哲学是否完全不同
- 某门语言究竟是“全面强”，还是“只在某几项特别强”

典型对比：

- `Rust` vs `Haskell`
- `TypeScript` vs `Kotlin`
- `Go` vs `Rust`
- `Scala` vs `OCaml`

通常能得出的结论：

- 总分相近不等于类型系统相似
- 很多时候“能力形状”比“能力总量”更重要

### 8.4 Feature Timeline

对应文件：

- [`frontend/src/components/panels/FeatureTimelinePanel.vue`](/e:/lang_analysis/frontend/src/components/panels/FeatureTimelinePanel.vue)

它展示什么：

- 每门语言中，每个特性首次进入语言时间线的大致年份
- 颜色按特性分组

它在做什么：

- 给静态矩阵加上时间维度

应该怎么读：

- x 轴看年份
- y 轴看语言
- 每个点表示某项特性在该语言中的“重要进入时刻”

它最适合回答什么问题：

- 某门语言是生来就带着某一整套类型身份，还是后期逐步演化出来的
- 某个特性是什么时候开始从研究世界进入产品世界的

通常能得出的结论：

- 有些语言从第一天起就带着完整设计理念出生
- 有些语言是长期迭代后才逐渐进入现代类型系统竞争
- pattern matching、ADT、generics 已经逐步离开纯函数式小圈子

### 8.5 Type-System Arms Race Index

对应文件：

- [`frontend/src/components/panels/ArmsRacePanel.vue`](/e:/lang_analysis/frontend/src/components/panels/ArmsRacePanel.vue)

它展示什么：

- 每年新增特性事件总数
- 5 年移动平均
- 累计特性事件总量
- 峰值年份、近 5 年均值、近期动量等摘要指标

它在做什么：

- 把所有语言的特性到达事件聚合成一条宏观时间线
- 试图回答：类型系统创新有没有在“加速”

应该怎么读：

- 柱状：每年有多少特性到达事件
- 绿色线：中期趋势，避免只被单一年份噪音误导
- 蓝色累计线：长期累积速度

它最适合回答什么问题：

- 类型系统设计是在零散演化，还是在某些时期显著提速
- 新语言是不是越来越倾向于从一开始就带更多高级能力

通常能得出的结论：

- 现代语言设计确实出现过明显加速阶段
- 类型系统竞争已经从学术前沿进入主流产品语言
- 新一代语言往往以“能力打包首发”的方式出现，而不是慢慢补齐

### 8.6 Similarity Network

对应文件：

- [`frontend/src/components/panels/SimilarityNetworkPanel.vue`](/e:/lang_analysis/frontend/src/components/panels/SimilarityNetworkPanel.vue)

它展示什么：

- 语言之间基于特性向量相似度构建的力导向网络
- 节点大小和复杂度相关
- 连线粗细和相似度相关

它在做什么：

- 从“表格对比”切到“关系空间”
- 强调谁和谁构成自然邻居

应该怎么读：

- 距离近，通常代表整体特性画像相近
- 边越粗，说明特征相似度越高
- 节点颜色反映 paradigm

它最适合回答什么问题：

- 哪些语言构成自然簇
- 哪些语言是桥梁型语言
- 某门语言是主流群落的一员，还是明显的独特 outlier

通常能得出的结论：

- ML-family 语言会形成高密度关系区
- Rust 这类语言可能在系统语言和代数 / 函数式设计之间起桥梁作用
- TypeScript 可能会更靠近现代实用语言群，而不是研究型语言群

### 8.7 Popularity Analysis

对应文件：

- [`frontend/src/components/panels/PopularityAnalysisPanel.vue`](/e:/lang_analysis/frontend/src/components/panels/PopularityAnalysisPanel.vue)

它展示什么：

- 类型复杂度与外部流行度信号之间的关系
- 支持切换：
  - TIOBE Rank
  - GitHub Stars Rank
  - Stack Overflow Loved %

它在做什么：

- 把“类型系统设计”与“现实世界受欢迎程度”放到同一张图上

应该怎么读：

- x 轴是类型复杂度
- y 轴是外部信号
- 点大小又带一点喜爱度 / 热度信息

它最适合回答什么问题：

- 表达力更强是否一定意味着更流行
- 哪些语言“技术上很强但仍然 niche”
- 哪些语言“足够强且又大规模落地”

通常能得出的结论：

- 高表达力不自动转化为大规模 adoption
- 很多研究型语言更像“被敬佩”，而不是“被广泛部署”
- 真正大规模成功的语言往往是表达力、生态、工具和团队 adoption 之间的平衡体

### 8.8 Feature Diffusion

对应文件：

- [`frontend/src/components/panels/FeatureDiffusionPanel.vue`](/e:/lang_analysis/frontend/src/components/panels/FeatureDiffusionPanel.vue)

它展示什么：

- 选定一个特性后，沿时间查看该特性如何扩散到不同语言和领域
- 支持播放与手动进度控制

它在做什么：

- 把抽象“特性”当成主角，讲它的传播史

应该怎么读：

- 先选特性
- 再看最早出现在哪些语言
- 再观察它是否扩散到更多 domain group

它最适合回答什么问题：

- 某个特性是长期停留在研究圈，还是最终进入了主流语言
- 它是先在某个特定家族内传播，还是跨家族扩散

通常能得出的结论：

- 不同特性的扩散路径完全不同
- 有些特性像 gradual typing 一样更容易进入工程生态
- 有些特性像 ownership、full dependent typing 一样仍然更集中在少数路线里

### 8.9 Domain Clusters

对应文件：

- [`frontend/src/components/panels/DomainClustersPanel.vue`](/e:/lang_analysis/frontend/src/components/panels/DomainClustersPanel.vue)

它展示什么：

- 先对 14 维特性向量做聚类
- 再用 PCA 压到 2D 做散点图
- 不同 cluster 以颜色区分，不同 domain group 用不同符号表示

它在做什么：

- 把高维语言画像压缩成“可直观看到的结构空间”

应该怎么读：

- 点之间越近，表示在压缩后的空间里越相似
- cluster 反映的是整体特征组合，而不是单个特性
- domain symbol 可以帮助判断“领域标签”和“类型系统画像”是否一致

它最适合回答什么问题：

- 哪些语言虽然来自不同生态，但类型画像非常接近
- 哪些语言在其 nominal domain 之外，实际上吸收了其他路线的类型思想

通常能得出的结论：

- domain 和 type profile 常常相关，但绝非完全一致
- 某些语言会落在“看起来不像它所属生态”的位置上
- 这类偏移本身往往就是最有趣的设计信号

### 8.10 Language Evolution Lineage

对应文件：

- [`frontend/src/components/panels/LineageGraphPanel.vue`](/e:/lang_analysis/frontend/src/components/panels/LineageGraphPanel.vue)

它展示什么：

- 语言之间的有向影响图
- 包含一组虚拟根节点，如 `ML`、`Lisp`
- 支持 focus 某门语言，只看它的上下游邻域

它在做什么：

- 给统计上的聚类关系补上“历史 / 思想来源”的解释层

应该怎么读：

- 箭头表示 influence，不一定是严格的血统继承
- 根节点是帮助阅读的大类传统，而不是精确历史实体
- focus 模式适合查看某门语言具体受了谁影响，又影响了谁

它最适合回答什么问题：

- 为什么某两门语言在特征空间里会靠得很近
- 某种现代设计到底来自哪条思想传统

通常能得出的结论：

- 很多现代语言其实是多条传统的混合产物
- Rust、Scala、TypeScript、Kotlin 这类语言特别适合用“综合体”而非“单一血统”来理解

需要注意：

这张图是人工整理的解释层，不是从分数自动推导出来的。

### 8.11 Interactive Feature Recommender

对应文件：

- [`frontend/src/components/panels/FeatureRecommenderPanel.vue`](/e:/lang_analysis/frontend/src/components/panels/FeatureRecommenderPanel.vue)

它展示什么：

- 用户选择一组关心的特性
- 设置最低阈值
- 再按 domain 过滤
- 系统按“满足程度 + 整体复杂度”做排序，并列出缺失项

它在做什么：

- 把描述型 dashboard 变成一个面向决策的工具

应该怎么读：

- 先选需求特性
- 再调阈值，区分“弱支持”和“强支持”
- 最后看推荐结果中的 matched / missing

它最适合回答什么问题：

- 如果我想要强 ADT + strong match + decent inference，应该看哪些语言
- 如果我只考虑某个 domain group，候选会怎样变化
- 哪些语言是广谱型，哪些语言只在特定要求下表现好

通常能得出的结论：

- 真正的语言选型往往不是看总分，而是看需求组合
- 某些语言在 general ranking 里不一定靠前，但在特定需求包下会非常强

## 9. 这个 Dashboard 适合支持哪些结论

这套 dashboard 很适合支持以下类型的分析：

- 哪些语言更偏“广覆盖”，哪些更偏“强 specialization”
- 哪些特性倾向于成套出现
- 哪些特性已经主流化，哪些仍然小众
- 某个特性是在扩散，还是仍然停留在少数传统中
- 类型系统复杂度与现实世界热度之间是什么关系
- 给定一组需求，哪些语言是更合理的候选

它不太适合支持以下类型的结论：

- 某门语言绝对更“好”
- 某门语言一定更适合所有工程团队
- 精确的产业 adoption 数字
- 极细颗粒度的历史因果推断

## 10. 使用时需要记住的 caveats

### 10.1 评分是解释性的，不是形式证明

这些分数是有依据的建模判断，不是数学定理。

### 10.2 时间线是摘要，不是逐版本档案

它强调的是“关键到达时刻”，而不是每个小版本的全部细节。

### 10.3 流行度指标只是 proxy

TIOBE、GitHub stars、Stack Overflow loved % 衡量的是不同维度，不应混为一谈。

### 10.4 血缘图是人工整理的解释层

它的作用是帮助理解，不是“数据自动发现的唯一事实”。

### 10.5 PCA / Network 都是分析工具，不是真实几何本体

它们能帮助人读懂高维空间，但会压缩、阈值化、丢失部分信息。

## 11. 建议怎么使用这份手册

如果你是第一次接触项目：

- 先读第 1 到第 4 节
- 再读第 8 节每个 panel 的说明
- 最后回到 dashboard 自己操作一遍

如果你要继续扩展数据集：

- 把第 3 节和第 4 节当作评分契约
- 把第 8 节当作各 panel 的语义说明书

如果你要对外介绍这个项目：

- 最适合拿来讲故事的视图通常是：
  - Feature Matrix
  - Feature Co-occurrence Matrix
  - Type-System Arms Race Index
  - Domain Clusters
  - Interactive Feature Recommender

## 12. 一段简短总结

这个 dashboard 想讲的，不只是“某些语言类型系统更强”这么简单。

它真正展示的是：

- 编程语言的类型系统设计已经分化成多条非常不同的路线
- 高级能力往往不是零散出现，而是成体系地捆绑出现
- 很多最初来自研究世界的思想，正在以不同速度进入产品化语言
- 真正大规模成功的语言，通常不是理论最强，而是 trade-off 做得最好
- 与其问“谁最强”，不如问“谁在哪个方向最强，以及它为此付出了什么代价”

这正是整个项目试图可视化出来的核心视角。
