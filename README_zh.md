# Scientific Figure System

[English](README.md) | [中文](README_zh.md)

这是一个小型工具包，用来生成面向论文排版的科研数据图和可编辑的技术示意图。

这个私有 release candidate 面向第一次接触项目的硕士生、博士生和科研人员。你会用 Python 和 Matplotlib，但希望工具能更认真地检查科研含义、来源追溯和矢量输出。

## 它解决什么问题

项目包含两个相互独立的产品：

- **scientific-figure**：根据明确的科研图规格生成数据图。当前真正经过生产测试的图型是 `DISCRETE_COMPARISON`、`DENSE_TIMESERIES` 和 `ERRORBAR_POINTWHISKER`。
- **scientific-schematic**：根据明确的语义规格生成技术示意图。可编辑源是原生 `.drawio` XML，目前登记了九类 diagram grammar。

最重要的使用原则很简单：**先保证数据，再保证含义，最后处理样式**。系统会检查绘图和矢量处理有没有偷偷改变横纵坐标、区间、阈值或事件位置等受保护的科研值。如果系统无法可靠理解输入，它会停止并说明问题，而不是猜一个结果继续画图。

## 它不是什么

它不是论文生产服务、通用图表库，也不是可以自动为所有示意图智能排版的系统，更不保证期刊接受。仓库中的例子全部使用 synthetic data，只用于演示。机器 QA 不能替代作者对数据、图注、科学解释和最终尺寸可读性的人工检查。

## 五分钟首用：第一张数据图

先从仓库根目录运行：

```powershell
git clone https://github.com/miku01031/scientific-figure-system.git
cd scientific-figure-system
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-core.txt
.venv\Scripts\python examples/synthetic/figure_minimal/run_example.py
```

这个确定性的 synthetic 示例会在 `examples/synthetic/figure_minimal/output/` 下写出 SVG。没有可选 CairoSVG 时，文件名是 `figure.DIAGNOSTIC.svg`；具备出版物导出能力时，文件名是 `figure.svg`。它不是科研证据。生成核心 SVG 不需要 CairoSVG、PyMuPDF 或 draw.io Desktop。

## 五分钟首用：第一张 schematic

同一个核心环境可以生成可编辑的原生图：

```powershell
.venv\Scripts\python examples/synthetic/schematic_minimal/run_example.py
```

输出文件是 `examples/synthetic/schematic_minimal/output/diagram.drawio`。不安装 draw.io 也能完成这一步。如果电脑上有 draw.io Desktop，可以之后用它做应用导出；这只是可选能力，生成原生 `.drawio` 并不依赖它。

## 可选的出版物输出能力

核心能力是 SVG 输出和原生 `.drawio` 生成。PDF/PNG 出版物导出属于单独的可选层：

```powershell
.venv\Scripts\python -m pip install -r requirements-publication.txt
```

这一层还需要操作系统提供的 native Cairo。只安装 Python 包 `CairoSVG`，不等于 native Cairo 一定可用。请看[安装说明](docs/INSTALLATION.md)和[runtime 分发政策](docs/RUNTIME_DISTRIBUTION_POLICY.md)。

PDF 检查和 PDF-QA 又是另一层可选能力：

```powershell
.venv\Scripts\python -m pip install -r requirements-pdfqa.txt
```

PyMuPDF 只用于 PDF 检查，不是核心依赖。第三方许可证信息见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 当前支持边界

### 数据图

公共候选的生产范围只有三类经过测试的图型：

- `DISCRETE_COMPARISON`
- `DENSE_TIMESERIES`
- `ERRORBAR_POINTWHISKER`

49 项 chart registry 是参考和规划材料，并不表示 49 类图都已经是可直接生产的 renderer。

公共候选只内置项目自己的 `our_moderate_vivid`。其他 palette 可以由用户自行提供，但需要自己记录出处并检查是否适合；它们不会被默认为项目内置 palette。

### 科研示意图

登记的 grammar 是：

`CONTROL_BLOCK_DIAGRAM`、`ALGORITHM_DECISION_LOOP`、`STAGED_METHOD_PIPELINE`、`BRANCH_MERGE_WORKFLOW`、`OFFLINE_ONLINE_SWIMLANE`、`HIERARCHICAL_ARCHITECTURE`、`DUAL_STREAM_FUSION`、`SEMANTIC_METHOD_OVERVIEW` 和 `EXPERIMENTAL_DATA_LIFECYCLE`。

Grammar 描述的是语义结构和图的组织方式。节点、关系和布局坐标由 semantic spec 提供；它不是对任意手绘图的 AI 自动排版。生成原生 XML 是核心能力。draw.io Desktop 的应用导出是可选能力，曾在 draw.io Desktop 31.4.5 上做过本地测试；GitHub hosted CI 不运行 Desktop E2E。

## 哪些情况会主动停止

当系统无法可靠保留科学含义时，它会 fail closed，也就是停止并报告问题。常见例子包括：

- series 太多，现有视觉编码无法清楚区分；
- 区间无效或上下界颠倒；
- 来源追溯缺失或 SHA 不一致；
- 使用了未知图型或未知 grammar；
- 缺少必要 glyph，或出现禁止的栅格/矢量结构。

停止意味着需要修正或人工审查输入。这样比生成一张看起来合理、但科学含义未经核实的图更安全。

## 推荐使用流程

1. 准备科研数据和 semantic specification。
2. 生成数据图或 schematic。
3. 阅读机器 QA 和能力检查结果。
4. 在目标物理尺寸和论文上下文中检查图。
5. 如需人工修改，记录修改内容。
6. 使用人工检查后的版本放入 manuscript。

Schematic 的 `.drawio` 文件是可编辑源。数据图主要以 SVG 发布，也可以在 Illustrator、Inkscape 或其他矢量软件中继续精修。不同软件对 SVG 分组和可编辑性的处理可能不同，项目不承诺所有编辑器都保持完全相同的编辑行为。

## 测试环境

Hosted core CI 已在 Windows、Ubuntu 和 macOS 上用 Python 3.10 和 3.11 通过。当前 Matplotlib 范围由 [requirements-core.txt](requirements-core.txt) 定义为 `>=3.10,<3.11`；Python 版本和 Matplotlib 版本是两个不同的约束。Ubuntu hosted integration 还测试 native Cairo 出版物导出和可选的 PyMuPDF PDF-QA 层。

## 仓库目录

- `skills/`：两个产品的实现和本地测试；
- `registries/`：参考 registry 和 advisory 记录；
- `schemas/`：JSON contract schema；
- `examples/synthetic/`：小型、确定性的演示；
- `tests/`：仓库、quickstart 和 hygiene 检查；
- `docs/`：安装、审查、runtime 和依赖说明。

修改代码或添加示例前，请先读 [CONTRIBUTING.md](CONTRIBUTING.md)。当前安全报告状态见 [SECURITY.md](SECURITY.md)。

## 作者

Li Yingxi ([@miku01031](https://github.com/miku01031))

## 引用

如果使用 renderer 或 schematic backend，请按照 [CITATION.cff](CITATION.cff) 引用本软件。

## 许可证状态

许可证选择仍明确保持为待作者确认。请看 [LICENSE_DECISION_REQUIRED.md](LICENSE_DECISION_REQUIRED.md)。
