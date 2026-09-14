# Scientific Figure System

[English](README.md) | [中文](README_zh.md)

这是一个小型工具包，用来生成面向论文排版的科研数据图和可编辑的技术示意图。

它适合已经有 Python/MATLAB 代码、结果文件和绘图需求的研究生、博士生和科研人员。你可以让 Codex 读取自己的项目并重建图形，同时保持科研数据不变。它不是通用绘图库，也不替代作者的科学判断。

仓库中的预览图全部由项目自己的合成数据或合成示意图规格生成，只用于展示，不是科研证据。

## 这个项目能做什么

仓库里有两个独立的 Codex Skill：

- **scientific-figure**：读取科研图规格并生成矢量数据图。目前真正经过 production 测试的 renderer 只有：
  - 密集时间序列（DENSE_TIMESERIES）
  - 离散比较（DISCRETE_COMPARISON）
  - 点/须区间图（ERRORBAR_POINTWHISKER）
- **scientific-schematic**：读取明确的语义示意图规格，生成可编辑的原生 .drawio 文件。目前登记了九类语义 grammar，覆盖控制图、流程、系统架构和相关技术图。

最重要的原则很简单：**先保证数据，再保证含义，最后处理样式**。系统会检查绘图和矢量处理有没有偷偷改变横纵坐标、区间端点、阈值或事件位置等受保护数值。如果输入含义不清楚或不在支持范围内，系统会停止并解释问题，而不是猜一个结果继续画图。

<a href="docs/readme_assets/chart_archetype_atlas.png"><img src="docs/readme_assets/chart_archetype_atlas.png" alt="科研图表类型参考图谱" width="100%"></a>

这张图表图谱用于帮助选择科研结果的表达方式。它覆盖了开发中探索的49类图型，但不表示已有49个 production renderer。当前正式测试过的 renderer 只有上面列出的三类。点击图片可以打开高清总览，family 细分图见[资源目录](docs/readme_assets/README.md)。

<a href="docs/readme_assets/schematic_quality_overview.png"><img src="docs/readme_assets/schematic_quality_overview.png" alt="合成科研示意图示例" width="100%"></a>

这里展示的是开发阶段生成的合成控制、FDI/FTC、observer 和 method 图。可编辑源是原生 .drawio XML；这张总览图不会扩大九类 grammar 的支持范围。

## 快速开始（推荐）

最简单的流程是：下载仓库、安装核心依赖、把两个 Skill 复制到 Codex 的 Skill 目录，然后在 Codex 中打开**你自己的科研项目**。不需要把科研数据复制到本仓库。

### 1. 下载仓库

~~~bash
git clone https://github.com/miku01031/scientific-figure-system.git
cd scientific-figure-system
~~~

仓库当前是私有的，clone 需要相应访问权限。公开发布前应删除或更新这句说明。

### 2. 安装核心依赖

推荐 Python 3.10 或 3.11。

Windows PowerShell：

~~~powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-core.txt
~~~

macOS/Linux：

~~~bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-core.txt
~~~

核心依赖足以生成 SVG 数据图和原生可编辑 .drawio 示意图。第一步不需要 CairoSVG、PyMuPDF 或 draw.io Desktop。

### 3. 安装 Codex Skill

仓库包含 skills/scientific-figure 和 skills/scientific-schematic。把它们复制到本机 Codex Skill 目录，然后重启 Codex，让它重新发现 Skill。

Windows PowerShell：

~~~powershell
$skillRoot = "$env:USERPROFILE\.codex\skills"
New-Item -ItemType Directory -Force $skillRoot | Out-Null
Copy-Item ".\skills\scientific-figure" "$skillRoot\scientific-figure" -Recurse -Force
Copy-Item ".\skills\scientific-schematic" "$skillRoot\scientific-schematic" -Recurse -Force
~~~

macOS/Linux：

~~~bash
mkdir -p ~/.codex/skills
cp -R skills/scientific-figure ~/.codex/skills/
cp -R skills/scientific-schematic ~/.codex/skills/
~~~

复制后重启 Codex，让两个 Skill 被发现。

### 4. 打开自己的科研项目

在 Codex 中打开包含已有 Python/MATLAB 代码、CSV/MAT/JSON/NPY 文件和结果目录的项目。科研数据不需要搬到这个仓库里。

### 5. 用一句话开始

把下面这段话复制到你想处理的项目中：

> 请使用 scientific-figure Skill 检查当前项目，读取已有结果数据和绘图代码，并生成适合论文使用的科研图。不得修改、平滑、重构或编造科研数据。优先使用当前正式支持的绘图方式和默认视觉规范。同时保存可复现的绘图代码/spec 和 SVG 结果。

如果项目结构很清楚，也可以先说：

> 使用 scientific-figure 帮我把这个项目中的科研图重新生成并优化。

如果科研含义、数据来源、区间定义或图型是否受支持不清楚，Codex 应先提问，而不是自行猜测。

## 高级用法

前面的快速开始足以完成第一次运行。下面介绍已有代码迁移、批量处理、表达方式、schematic grammar、配色和人工检查。

## 三种常见用法

### 重新生成已有科研图

如果项目里已有 MATLAB 或 Python 绘图代码：

> 请使用 scientific-figure 检查当前项目已有的绘图代码。保持所有科研数据和计算结果不变，只重新组织图形表达、排版、配色和矢量输出，不要修改任何科学计算。

这是迁移旧图最推荐的方式之一。Skill 改的是图形构造和输出，不是科研计算。

### 从项目结果生成新图

> 请检查当前项目，找到论文图使用的结果数据。逐张判断它们是否符合 scientific-figure 当前支持的 production renderer。对符合的图生成新图，保留原始数据和区间，保存可复现的代码/spec，并清楚说明不支持或需要我决定的部分。不要修改科研结果。

批量检查绘图脚本可以说：

> 请检查当前项目的所有绘图脚本和结果图。符合 production renderer 的部分使用 scientific-figure；不支持的图型不要声称是经过验证的 scientific-figure 输出，请说明限制并保留科研结果。不要修改计算。

### 生成可编辑的科研示意图

> 请使用 scientific-schematic 检查当前项目，生成一张用于解释主要方法或系统架构的可编辑技术示意图。不要添加项目中不存在的科学模块，输出可编辑的 .drawio 文件。

如果要从代码整理流程：

> 请检查当前项目的源代码和文档，生成一张概括实际处理、控制或故障诊断流程的 scientific-schematic 图。绘图前先列出你推断出的模块和连接；如果关系不确定，请先问我，不要自行编造。

scientific-schematic 要求 semantic spec 提供真实模块、关系和布局坐标。grammar 只是组织图形的方式，不是自动理解科研结构或任意布局的引擎。

## 当前可以生成什么

### 正式测试过的数据图

| 用户容易理解的名称 | 代码名称 | 典型用途 |
| --- | --- | --- |
| 密集时间序列 | DENSE_TIMESERIES | 至少32个样本的连续时间信号 |
| 离散比较 | DISCRETE_COMPARISON | 最多8条有独立编码的离散/分类序列 |
| 点/须区间 | ERRORBAR_POINTWHISKER | 有明确上下端点的估计量 |

renderer 会 fail closed。热图、混淆矩阵、任意流程图、网络、3D、雷达图、Sankey 等不支持的图型不会被静默套进这三种 recipe。49 项 chart registry 是参考和规划材料，用来讨论表达方式，不代表49种 production renderer。

### Schematic grammar

当前 registry 有九类：

- CONTROL_BLOCK_DIAGRAM：控制回路和带名称的信号路径；
- ALGORITHM_DECISION_LOOP：带终止判断的迭代算法；
- STAGED_METHOD_PIPELINE：顺序方法阶段和中间对象；
- BRANCH_MERGE_WORKFLOW：并行分支最终合并；
- OFFLINE_ONLINE_SWIMLANE：离线训练与在线部署；
- HIERARCHICAL_ARCHITECTURE：分层系统接口；
- DUAL_STREAM_FUSION：互补的数据流和模型流；
- SEMANTIC_METHOD_OVERVIEW：方法或模型的变换关系；
- EXPERIMENTAL_DATA_LIFECYCLE：采集、清洗、分析和验证。

grammar 不会凭空发明拓扑。用户或 Codex 必须根据项目提供真实模块、连接、标签和布局坐标。

## 配色和视觉规范

公共候选当前内置的默认 categorical palette 是 our_moderate_vivid。多数用户不需要手动写 palette，Skill 会根据图型和 series 数量自动选择。

你可以用自然语言提出：

- “使用克制的配色。”
- “突出 Method A，其余方法作为中性背景。”
- “除了颜色，再用 marker 或线型区分。”

renderer 仍会检查编码是否唯一、是否容易区分；如果当前 palette 不能安全区分这些科研对象，它会停止。Tol 和 Okabe–Ito 的内部研究数值表不属于当前公共候选的 bundled palette。

有些颜色承担语义角色，而不是表示一个 series，例如：fault_event、threshold、reference、neutral、baseline、missing 和 text。通常不需要自己指定 hex 值。

representation advisor 目前只给建议，例如：

- 曲线高度重合 → 中心绝对趋势 + spread summary；
- 两个 endpoint 同时带区间和分母/数量 → forest 风格图并对齐附加信息；
- 概率/区间结果与参考值比较 → 横向区间图加 reference line。

这些建议不会在没有作者确认时自动改变真实论文的科学表达。

## 输出格式

核心输出：

- 数据图：SVG，同时保留可复现代码/spec 和 QA 记录；
- 示意图：原生可编辑 .drawio XML。

SVG 可以继续在 Illustrator、Inkscape 或其他矢量软件中检查和精修。手工精修时不要修改科研数值。.drawio 可以在 draw.io Desktop 中移动原生节点、修改文字和调整间距。

可选出版物导出：

~~~powershell
.venv\Scripts\python -m pip install -r requirements-publication.txt
~~~

macOS/Linux：

~~~bash
.venv/bin/python -m pip install -r requirements-publication.txt
~~~

PDF/PNG 导出还需要操作系统提供 native Cairo。只安装 Python CairoSVG 包并不能保证 native Cairo 可用。PDF 检查和 PDF-QA 是另一层可选能力：

~~~powershell
.venv\Scripts\python -m pip install -r requirements-pdfqa.txt
~~~

更多信息见[安装说明](docs/INSTALLATION.md)、[runtime 分发政策](docs/RUNTIME_DISTRIBUTION_POLICY.md)和[第三方 notices](THIRD_PARTY_NOTICES.md)。

## 你应该得到什么

一次正常的 Codex 协作通常会返回：

1. SVG 或 .drawio；
2. 可复现的绘图代码或 semantic spec；
3. QA/能力检查结果和警告；
4. 只有在可选出版物能力可用时才有 PDF/PNG。

机器 QA 是安全检查，不是期刊录用结论。请在目标物理尺寸下检查图，也要自己确认图注、解释和科学结论。

## 哪些情况会主动停止

停止是有意设计的。常见情况包括：

- series 太多，无法用独立编码区分；
- 区间无效或上下界颠倒；
- 来源追溯缺失或 SHA 不一致；
- 使用未知图型或未知 grammar；
- 缺少 CJK glyph，或出现禁止的栅格/矢量结构。

系统宁愿解释问题，也不会生成一张看起来合理但含义未经核实的图。

## 后续修改可以这样说

- “图例挡住曲线了，保持数据不变，重新排版。”
- “突出 Method A，其余方法作为中性背景。”
- “不要改变曲线，只调整字体、间距和图例。”
- “给我一个适合单栏论文的版本。”
- “生成可编辑的 .drawio 版本。”

## 不使用 Codex 时的手动方式

Codex 是推荐工作流，但仓库也提供确定性的合成示例：

~~~powershell
.venv\Scripts\python examples/synthetic/figure_minimal/run_example.py
.venv\Scripts\python examples/synthetic/schematic_minimal/run_example.py
~~~

第一条命令会在 examples/synthetic/figure_minimal/output/ 写出 SVG；如果可选出版物导出不可用，会写出明确命名的 diagnostic SVG。第二条会写出 examples/synthetic/schematic_minimal/output/diagram.drawio。这些示例使用合成数据，不能替代对自己项目进行来源追溯和语义确认。

详细提示词、故障排查和项目工作流见[完整 Codex 使用指南](docs/CODEX_USAGE_zh.md)。英文用户可看[English guide](docs/CODEX_USAGE.md)。

## 推荐流程

1. 找到科研数据和已有绘图代码。
2. 让 Codex 检查项目并说明它找到了什么。
3. 生成图或示意图。
4. 阅读 QA 和能力结果。
5. 在目标物理尺寸下检查输出。
6. 如需人工修改，记录修改内容。
7. 将人工检查后的结果用于 manuscript。

## 测试环境

Hosted core CI 已在 Windows、Ubuntu 和 macOS 上用 Python 3.10 和 3.11 通过。Python 和 Matplotlib 的约束分别存在；请以 requirements-core.txt 为准。Ubuntu integration 还测试 native Cairo 出版物导出和可选的 PyMuPDF PDF-QA。

原生 .drawio XML 生成属于核心能力，不需要 draw.io Desktop。Desktop 导出是可选能力，此前在 draw.io Desktop 31.4.5 上本地测试过；hosted CI 不运行 Desktop E2E。

## 仓库目录

- skills/ — 两个 Codex Skill；
- registries/ — palette、chart reference、representation advisor 和 grammar registry；
- schemas/ — 小型 contract schema；
- examples/synthetic/ — 确定性的合成示例；
- tests/ — 核心和 hygiene 检查；
- docs/ — 安装、审查、runtime 和详细使用说明。

修改代码或添加示例前，请先读 [CONTRIBUTING.md](CONTRIBUTING.md)。安全报告状态见 [SECURITY.md](SECURITY.md)。

## 作者

Li Yingxi ([@miku01031](https://github.com/miku01031))

## 引用

如果使用 renderer 或 schematic backend，请按 [CITATION.cff](CITATION.cff) 引用本软件。

## 许可证状态

许可证仍明确保持为待作者确认。请看 [LICENSE_DECISION_REQUIRED.md](LICENSE_DECISION_REQUIRED.md)。

详细使用和故障排查见 [docs/CODEX_USAGE_zh.md](docs/CODEX_USAGE_zh.md)。
