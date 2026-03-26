[English](./README.md) | [简体中文](./README.zh-CN.md)

# Glassroom

[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Shared schema](https://img.shields.io/badge/schema-case%20object-7c3aed)](#shared-unit-of-work)
[![Mountable skills](https://img.shields.io/badge/skills-mountable-0f766e)](#module-families)
[![UI templates](https://img.shields.io/badge/ui%20templates-deidentified-9a3412)](#ui-template-library)

> 🧭 *把案例型情报分析组织成结构化、可教学、可复用、可挂载的开源工作流核心与 Skill 套件。*

## 📚 目录

- [✨ Glassroom 到底是什么](#what-glassroom-is)
- [🚫 它不是什么](#what-glassroom-is-not)
- [⚡ 快速开始](#quick-start)
- [📦 安装方式](#installation)
- [🧩 当前已公开能力](#current-public-scope)
- [🗺 Workflow artifact map](#workflow-artifact-map)
- [🔧 共享工作单元](#shared-unit-of-work)
- [🧱 模块族谱](#module-families)
- [🎨 UI 模板库](#ui-template-library)
- [🗂 仓库结构](#repository-layout)
- [🛣 路线图方向](#roadmap-direction)
- [📐 设计原则](#design-principles)
- [📌 当前状态](#status)
- [License](#license)

Glassroom 是一个面向案例型情报分析的开源 workflow core。

但更准确地说，它同时也是一套**可挂载的 Skill 套件**：仓库里既有可复用的 `packages/`、共享 schema、参考文档，也有可挂载到 agent 工作区里的 `skills/` 层。

<a id="what-glassroom-is"></a>
## ✨ Glassroom 到底是什么

Glassroom **不是单个 Agent**，也**不是单个 Skill**。

它更像一个两层结构的项目：

- **workflow core**
  - shared case object
  - 中间产物
  - 可复用分析模块

- **mountable skill suite**
  - `skills/glassroom-router`
  - `skills/glassroom-case-assembler`
  - `skills/glassroom-cognitive-bias`
  - `skills/glassroom-structured-analysis`

如果你要的只是“让 AI 写点内容”，这不是它的重点。

Glassroom 更适合下面这些事情：

- 把分散的分析结果收束成共享 case object
- 让 source、bias、mitigation、structured analysis 这些层彼此连通
- 为后续 HTML 教学页、课程写作、讲授材料保留稳定输入
- 把“流程能力”沉淀成 schema 和模块，而不是只藏在 prompt 里
- 保留真正可复用的教学界面结构，而不是反复做一次性课件

<a id="what-glassroom-is-not"></a>
## 🚫 它不是什么

它 **不是**：

- 通用型作文生成器
- 一堆彼此无关的课堂 prompt 集合
- 课堂原始资产的直接公开通道
- 任何私有教学材料都应该无差别开源的理由
- 在核心契约还没稳定前就急着做成大而全平台

Glassroom 的开源思路很明确：

先公开可移植的骨架，再逐步放出真正 public-safe、能独立成立的模块。

<a id="quick-start"></a>
## ⚡ 快速开始

当前最快的体验方式，是用仓库里已经准备好的 public-safe 示例输入，先组装一个共享 case object：

```bash
python3 packages/case-assembler/assemble_case.py \
  --base-case examples/base-case.json \
  --source-card examples/source-card.json \
  --bias-analysis examples/bias-analysis.json \
  --mitigation-pack examples/mitigation-pack.json \
  --structured-analysis examples/structured-analysis.json \
  --out-json /tmp/glassroom-case.json \
  --out-md /tmp/glassroom-case.md
```

如果你想分别看分析模块，也可以直接跑：

```bash
python3 packages/cognitive-bias/build_bias_analysis.py \
  --input examples/bias-input.json \
  --out-json /tmp/bias-analysis.json \
  --out-md /tmp/bias-analysis.md

python3 packages/structured-analysis/build_structured_analysis.py \
  --input examples/structured-analysis-input.json \
  --out-json /tmp/structured-analysis.json \
  --out-md /tmp/structured-analysis.md
```

也就是说，现阶段公开出来的模块不是摆设，已经能直接跑通。

<a id="installation"></a>
## 📦 安装方式

Glassroom 现在有两种常见用法：

- 直接把仓库当成 `packages/` 来使用
- 把 `skills/` 下面的技能挂载到 agent workspace

### 面向 OpenClaw / workspace 型 agent 的手动安装

OpenClaw 会从 workspace 的 `skills/` 目录加载技能。最直接的做法，是 clone 本仓库后，把需要的 Glassroom skill 文件夹复制或软链接进你的活动工作区。

#### Linux / macOS / WSL

```bash
git clone https://github.com/NanAquarius/Glassroom.git
cd Glassroom
mkdir -p ~/.openclaw/workspace/skills
ln -s "$(pwd)/skills/glassroom-router" ~/.openclaw/workspace/skills/glassroom-router
ln -s "$(pwd)/skills/glassroom-case-assembler" ~/.openclaw/workspace/skills/glassroom-case-assembler
ln -s "$(pwd)/skills/glassroom-cognitive-bias" ~/.openclaw/workspace/skills/glassroom-cognitive-bias
ln -s "$(pwd)/skills/glassroom-structured-analysis" ~/.openclaw/workspace/skills/glassroom-structured-analysis
```

如果你不想用软链接，也可以直接复制：

```bash
cp -R skills/glassroom-router ~/.openclaw/workspace/skills/
cp -R skills/glassroom-case-assembler ~/.openclaw/workspace/skills/
cp -R skills/glassroom-cognitive-bias ~/.openclaw/workspace/skills/
cp -R skills/glassroom-structured-analysis ~/.openclaw/workspace/skills/
```

#### Windows PowerShell

```powershell
git clone https://github.com/NanAquarius/Glassroom.git
cd Glassroom
New-Item -ItemType Directory -Force "$HOME/.openclaw/workspace/skills" | Out-Null
Copy-Item .\skills\glassroom-router "$HOME/.openclaw/workspace/skills\glassroom-router" -Recurse -Force
Copy-Item .\skills\glassroom-case-assembler "$HOME/.openclaw/workspace/skills\glassroom-case-assembler" -Recurse -Force
Copy-Item .\skills\glassroom-cognitive-bias "$HOME/.openclaw/workspace/skills\glassroom-cognitive-bias" -Recurse -Force
Copy-Item .\skills\glassroom-structured-analysis "$HOME/.openclaw/workspace/skills\glassroom-structured-analysis" -Recurse -Force
```

### 安装到项目本地 `skills/` 目录

如果你的 agent runtime 把当前项目目录本身当作 workspace，也可以直接把 Glassroom 的 skill 文件夹挂到 `./skills/`。

#### Linux / macOS / WSL

```bash
mkdir -p ./skills
ln -s "$(pwd)/skills/glassroom-router" ./skills/glassroom-router
ln -s "$(pwd)/skills/glassroom-case-assembler" ./skills/glassroom-case-assembler
ln -s "$(pwd)/skills/glassroom-cognitive-bias" ./skills/glassroom-cognitive-bias
ln -s "$(pwd)/skills/glassroom-structured-analysis" ./skills/glassroom-structured-analysis
```

#### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force .\skills | Out-Null
Copy-Item .\skills\glassroom-router .\skills\glassroom-router -Recurse -Force
Copy-Item .\skills\glassroom-case-assembler .\skills\glassroom-case-assembler -Recurse -Force
Copy-Item .\skills\glassroom-cognitive-bias .\skills\glassroom-cognitive-bias -Recurse -Force
Copy-Item .\skills\glassroom-structured-analysis .\skills\glassroom-structured-analysis -Recurse -Force
```

### 发给 Claude Code / OpenCode / 类似 CLI 的“一句话安装”

如果你是在 Claude Code、OpenCode 或类似 coding-agent CLI 里让 AI 帮你安装，可以直接发这句话：

```text
Clone https://github.com/NanAquarius/Glassroom into this machine, then mount the folders under Glassroom/skills/ into the current workspace skills/ directory, and summarize which Glassroom skills are now available.
```

如果 AI 对你的 OpenClaw workspace 有访问权，也可以直接说：

```text
Clone https://github.com/NanAquarius/Glassroom and mount the folders under Glassroom/skills/ into ~/.openclaw/workspace/skills/, then tell me which Glassroom skills were installed.
```

这里故意用的是通用说法，不依赖特定 CLI 的私有包管理命令，所以更容易跨 OpenCode、Claude Code 等环境复用。

<a id="current-public-scope"></a>
## 🧩 当前已公开能力

当前这版公开出来的 Glassroom，已经包含：

- 共享 Glassroom case schema
- 描述模块如何围绕该 schema 协作的 workflow contract
- `case-assembler`
- `cognitive-bias`
- `structured-analysis`
- 一套去标识化后的 UI 模板参考库
- 第一批可挂载的开源 `skills/` 层

这套公开版本故意从“小而稳”开始。

目标不是一口气把所有本地能力扔出来，而是先把最稳、最适合公开、最能形成骨架的部分开出来。

<a id="workflow-artifact-map"></a>
## 🗺 Workflow artifact map

当前核心流可以理解成：

```text
partial analysis artifacts
  → shared case object
  → reusable intermediate outputs
  → HTML pages / writing deliverables / teaching artifacts
```

更具体一点，就是：

```text
base-case.json
  + source-card.json
  + bias-analysis.json
  + mitigation-pack.json
  + structured-analysis.json
    → glassroom-case.json
    → glassroom-case.md
```

这套结构的价值在于：

- 不再把工作结果困在一堆互不相认的小文件里
- 模块之间的交接更清楚
- 同一份 case object 可以被多个下游输出复用
- 关键逻辑不再只活在某一轮 prompt 里

<a id="shared-unit-of-work"></a>
## 🔧 共享工作单元

Glassroom 默认使用共享 **case object** 作为工作单元。

相关文件在这里：

- [`schemas/glassroom-case.schema.json`](./schemas/glassroom-case.schema.json)
- [`docs/workflow-contract.md`](./docs/workflow-contract.md)

不是每个模块都必须填满所有字段。

但这个共享 schema 是整个 Glassroom 能顺畅扩展的前提，因为它让 source intake、bias analysis、structured analysis、mitigation、renderer、writing outputs 这些层有共同语境。

<a id="module-families"></a>
## 🧱 模块族谱

### Package 层

- [`packages/case-assembler/`](./packages/case-assembler/)
  - 把零散输出合并成可复用的 case object

- [`packages/cognitive-bias/`](./packages/cognitive-bias/)
  - 把候选偏差与文本片段整理成可复用的 bias-analysis artifact

- [`packages/structured-analysis/`](./packages/structured-analysis/)
  - 把 policy question、hypotheses、assumptions 与 evidence 组织成 structured-analysis artifact

### 可挂载 Skill 层

- [`skills/glassroom-router/`](./skills/glassroom-router/)
- [`skills/glassroom-case-assembler/`](./skills/glassroom-case-assembler/)
- [`skills/glassroom-cognitive-bias/`](./skills/glassroom-cognitive-bias/)
- [`skills/glassroom-structured-analysis/`](./skills/glassroom-structured-analysis/)

这些 Skills 是 **package-backed** 的。

也就是说：真正的执行逻辑在 `packages/`，而 `skills/` 负责提供可挂载的 skill 形态与任务路由入口。

### 后续扩展方向

- source intake
- OSINT pitfalls and mitigations
- case HTML rendering
- course writing outputs

<a id="ui-template-library"></a>
## 🎨 UI 模板库

Glassroom 现在也开始有一套 public-safe UI template library：

- [`docs/ui-template-library/README.md`](./docs/ui-template-library/README.md)
- [`docs/ui-template-library/templates/`](./docs/ui-template-library/templates/)
- [`docs/ui-template-library/reference-pages/`](./docs/ui-template-library/reference-pages/)

这套库的定位，不是拿来原样复刻课堂页面。

它的作用是：

在去标识化之后，把真正可复用的教学结构、信息架构和 UI 逻辑保留下来。

也就是说，保留的是教学骨架，不是个人归属信息，也不是某门课的私有页面皮肤。

<a id="repository-layout"></a>
## 🗂 仓库结构

```text
Glassroom/
├── docs/
│   └── ui-template-library/
├── examples/
├── packages/
│   ├── case-assembler/
│   ├── cognitive-bias/
│   └── structured-analysis/
├── schemas/
├── skills/
│   ├── glassroom-router/
│   ├── glassroom-case-assembler/
│   ├── glassroom-cognitive-bias/
│   └── glassroom-structured-analysis/
├── .gitignore
├── LICENSE
├── README.md
└── README.zh-CN.md
```

<a id="roadmap-direction"></a>
## 🛣 路线图方向

Glassroom 后续适合继续公开的模块族，大致包括：

- source intake
- cognitive bias analysis
- OSINT pitfalls and mitigations
- structured analytic techniques
- case HTML rendering
- course writing outputs

但它不会乱序推进。

目前更合理的节奏是：

1. shared schema
2. workflow contract
3. reusable analysis modules
4. de-identified UI patterns
5. downstream renderers and delivery modules

<a id="design-principles"></a>
## 📐 设计原则

- 优先稳定结构，而不是炫技推断
- 中间产物要可复用
- 共享 schema 必须可回溯、可恢复
- workflow orchestration 和 presentation layer 要分开
- 只公开 public-safe、可移植、可维护的部分

<a id="status"></a>
## 📌 当前状态

Glassroom 现在还处在早期 extraction 阶段。

核心 contract 已公开，第一批分析模块已公开，第一批去标识化 UI 参考模式也已公开，同时仓库已经开始具备可挂载 Skill 套件的形态。

接下来会继续把本地 Glassroom 里更成熟、也更适合公开的部分一点点抽出来，而不是一股脑倒进去。

## License

MIT

---

<div align="center">

*如果 Glassroom 对你的教学、分析流程或 workflow 设计有帮助，欢迎点个 Star、提个 issue，或者告诉我你怎么在用它。*

<sub>⭐ <a href="https://github.com/NanAquarius/Glassroom">Star</a> &nbsp;·&nbsp; 🐛 <a href="https://github.com/NanAquarius/Glassroom/issues">Issue</a> &nbsp;·&nbsp; 🤝 <a href="https://github.com/NanAquarius/Glassroom/pulls">PR</a></sub>

</div>
