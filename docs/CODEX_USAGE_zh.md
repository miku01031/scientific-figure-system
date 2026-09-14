# Codex 使用指南

这份指南用尽量直白的方式说明日常使用流程。它假设你的科研项目已经有代码和结果文件。

## 1. 只需安装一次

在仓库根目录：

~~~bash
python -m venv .venv
# Windows PowerShell：.venv\Scripts\python -m pip install -r requirements-core.txt
# macOS/Linux：      .venv/bin/python -m pip install -r requirements-core.txt
~~~

把两个 Skill 文件夹复制到 Codex 的 Skill 目录，然后重启 Codex。

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

Skill 文件夹不需要复制进你的科研项目。

## 2. 在 Codex 中打开你要处理的项目

在 Codex 中打开真正包含科研工作的目录：绘图脚本、仿真结果、CSV/MAT/JSON/NPY 文件和输出目录。不要为了使用 Skill 把数据复制到本仓库。

第一次可以直接说：

> 请使用 scientific-figure Skill 检查当前项目，读取已有结果数据和绘图代码，并生成适合论文使用的科研图。不得修改、平滑、重构或编造科研数据。优先使用当前正式支持的绘图方式和默认视觉规范。同时保存可复现的绘图代码/spec 和 SVG 结果。

如果只是想先试一句更短的话：

> 使用 scientific-figure 帮我把这个项目中的科研图重新生成并优化。

Codex 应该先检查项目。如果单位、区间含义、来源追溯、事件位置或系统拓扑不清楚，它应该先问你。

## 3. 三种实用模式

### 模式1：重新生成已有图

> 请使用 scientific-figure 检查当前项目已有的绘图代码。保持所有科研数据和计算结果不变，只重新组织图形表达、排版、配色和矢量输出，不要修改任何科学计算。

正常结果应包含来源明确的图规格、可复现绘图代码、SVG 和 QA/能力记录。若原图不符合受支持的图型，Skill 可能主动停止。

### 模式2：从结果批量生成图

> 请检查当前项目，找到论文图使用的结果数据。逐张判断它们是否符合 scientific-figure 当前支持的 production renderer。对符合的图生成新图，保留原始数据和区间，保存可复现的代码/spec，并清楚说明不支持或需要我决定的部分。不要修改科研结果。

批量检查绘图脚本可以说：

> 请检查当前项目的所有绘图脚本和结果图。符合 production renderer 的部分使用 scientific-figure；不支持的图型不要声称是经过验证的 scientific-figure 输出，请说明限制并保留科研结果。不要修改计算。

### 模式3：生成可编辑 schematic

> 请使用 scientific-schematic 检查当前项目，生成一张用于解释主要方法或系统架构的可编辑技术示意图。不要添加项目中不存在的科学模块，输出可编辑的 .drawio 文件。

如果要从代码整理流程：

> 请检查当前项目的源代码和文档，生成一张概括实际处理、控制或故障诊断流程的 scientific-schematic 图。绘图前先列出你推断出的模块和连接；如果关系不确定，请先问我，不要自行编造。

schematic Skill 不需要 draw.io Desktop 就能生成原生 .drawio XML。Desktop 只是打开、编辑或导出时的可选工具。

## 4. 如何选择表达方式

当前正式测试过的数据图 renderer 只有：

- DENSE_TIMESERIES：至少32个样本的连续时间信号；
- DISCRETE_COMPARISON：有明确离散/分类含义、最多8条独立编码的 series；
- ERRORBAR_POINTWHISKER：有明确上下端点的估计量。

Chart atlas 和 chart registry 是参考资料。如果目标图型不在这三类中，请让 Codex 说明限制，不要把普通图强行套进受支持 recipe。

Representation advisor 目前只有三条建议：

- 高度重合的曲线 → 中心绝对趋势 + spread summary；
- 两个 endpoint 同时带区间和分母/数量 → forest 风格并对齐附加信息；
- 概率/区间结果与参考值比较 → 横向区间图加 reference line。

它们只是帮助讨论表达方式，不会未经作者确认就改变真实科研表达。

## 5. 如何控制配色

公共候选内置 our_moderate_vivid 作为默认 categorical palette。普通使用不需要填写颜色参数：

> 使用默认 palette，并在必要时用 marker/线型提供冗余区分。

也可以说：

> 使用克制的配色。

> 突出 Method A，其余方法作为中性背景。

> 除了颜色，再用 marker 或线型区分。

语义颜色包括 fault_event、threshold、reference、neutral、baseline、missing 和 text。它们和 series 的分类颜色是分开的。如果当前 palette 不能安全区分不同科研对象，系统会停止，而不是循环使用颜色。

当前公共候选不 bundled 内部研究过的 Tol 或 Okabe–Ito 数值表。

## 6. 如何选择 schematic grammar

只有在科研关系确实匹配时才指定 grammar：

- CONTROL_BLOCK_DIAGRAM：控制/被控对象反馈和命名信号；
- ALGORITHM_DECISION_LOOP：带终止判断的迭代方法；
- STAGED_METHOD_PIPELINE：顺序方法阶段；
- BRANCH_MERGE_WORKFLOW：并行分支再合并；
- OFFLINE_ONLINE_SWIMLANE：离线训练与在线推理；
- HIERARCHICAL_ARCHITECTURE：分层系统接口；
- DUAL_STREAM_FUSION：互补的数据流/模型流；
- SEMANTIC_METHOD_OVERVIEW：方法或模型变换；
- EXPERIMENTAL_DATA_LIFECYCLE：采集到验证的数据生命周期。

grammar 只是组织方式，不会自动推断任意科研拓扑。semantic spec 必须提供真实模块、关系、标签和坐标。

## 7. 输出与人工检查

一次正常运行应保留：

- 科研数组和区间端点；
- 来源和 provenance 记录；
- SVG 或 .drawio；
- 可复现代码/spec；
- QA 和能力结果。

请在目标物理尺寸下检查输出。机器 QA 不决定期刊相似度、科学解释或是否应该替换正式论文图。

可以用这些后续指令：

- “保持数据不变，把图例移开。”
- “突出 Method A，其余作为中性背景。”
- “只调整字体、间距和 panel 平衡。”
- “如果标签仍然清楚，给我一个单栏版本。”
- “给我可编辑的 .drawio 源文件。”

## 8. 不使用 Codex 时的手动运行

在仓库根目录运行：

~~~powershell
.venv\Scripts\python examples/synthetic/figure_minimal/run_example.py
.venv\Scripts\python examples/synthetic/schematic_minimal/run_example.py
~~~

第一条会在 examples/synthetic/figure_minimal/output/ 生成 SVG；如果可选出版物转换不可用，会生成明确命名的 diagnostic SVG 并报告能力状态。第二条会生成 examples/synthetic/schematic_minimal/output/diagram.drawio。

## 9. 可选能力与故障排查

**SVG 可以生成，但 PDF/PNG 不行。** 核心 SVG 不需要 CairoSVG。安装 requirements-publication.txt，并安装操作系统提供的 native Cairo。只安装 Python CairoSVG 包不够。

**PDF 检查不可用。** 安装 requirements-pdfqa.txt。PyMuPDF 属于 PDF-QA 层，不是核心依赖。

**没有 draw.io。** 原生 .drawio 仍然可以生成。只有需要应用编辑或导出时才安装 draw.io Desktop。

**图型不支持。** 让 Codex 说明碰到了哪条 renderer 边界。不要把普通图重新标成经过验证的 scientific-figure 输出。

**series 太多。** 只有在科研上确实允许合并身份时才减少 series；否则请求人工审查，不要静默循环颜色。

**中文 glyph 缺失。** 配置可用的中文字体并重新做 glyph 检查。不要接受缺字的图。

**Codex 没发现 Skill。** 检查目录是否正好是 ~/.codex/skills/scientific-figure 和 ~/.codex/skills/scientific-schematic，然后重启 Codex。

更多安装信息见 docs/INSTALLATION.md 和 docs/RUNTIME_DISTRIBUTION_POLICY.md。

## 10. 这个工作流不会做什么

它不保证期刊接受，不会猜测缺失科研值，不会自动替换 manuscript 图片，不支持所有图型，也不会凭空发明控制或故障诊断拓扑。人工检查仍然是必须的。
