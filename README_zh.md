# Scientific Figure System（公共候选）

公共仓库版本：**0.1.0-rc1**。两个内部产品仍分别是
scientific-figure 1.1.x 和 scientific-schematic 0.1.x。

这是一个以语义输入、来源追溯和 fail-closed 校验为核心的科研图与
schematic 工具候选。它不是论文生产服务，也不保证期刊接受或替代作者的
科学判断；仓库示例全部是 synthetic demonstration。

## 五分钟首用：数据图

在仓库根目录运行：

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-core.txt
.venv\Scripts\python examples/synthetic/figure_minimal/run_example.py
```

命令生成一个确定性的 synthetic SVG。这个核心流程不安装可选的出版物导出
或 PDF-QA 依赖。

## 五分钟首用：schematic

无需 draw.io 即可生成原生可编辑 XML：

```powershell
.venv\Scripts\python examples/synthetic/schematic_minimal/run_example.py
```

输出 `examples/synthetic/schematic_minimal/output/diagram.drawio`。需要应用
导出时再单独安装 draw.io，并设置 `DRAWIO_EXECUTABLE`。本候选在 draw.io
Desktop 31.4.5 上测试过，不声明所有版本都支持。

## 可选能力

需要 PDF/PNG 出版物导出时，再安装 `requirements-publication.txt` 和平台的
native Cairo。需要 PDF 检查/QA 时，再安装 `requirements-pdfqa.txt`。
`pip install CairoSVG` 只安装 Python 包装层，并不保证 native Cairo 可用。
生成原生 `.drawio` 不需要 draw.io Desktop；应用导出是可选能力。

## 支持边界

`scientific-figure` 当前支持：离散比较、密集时间序列、errorbar
point-whisker。`scientific-schematic` 使用九类已登记语义 grammar；节点、
拓扑和布局坐标由 spec 提供，不是智能自动排版。未知图型、容量不足、区间
错误、来源 SHA 不一致、缺少 CJK 字体、缺少 native Cairo 或禁止的栅格/矢量
结构会给出明确错误并停止。公共候选只内置项目自有
`our_moderate_vivid`；其他 palette 需要用户自行提供并记录出处。

机器 QA 不等于人工视觉验收。真实数据使用前应冻结来源、科学意图和不变量。
