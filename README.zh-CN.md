[English](./README.md) | [简体中文](./README.zh-CN.md)

# Glassroom

[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](#quick-start)
[![Markdown](https://img.shields.io/badge/Markdown-Docs-111827?style=flat-square&logo=markdown&logoColor=white)](#what-glassroom-is)
[![Node.js CLI](https://img.shields.io/badge/Node.js-CLI-339933?style=flat-square&logo=node.js&logoColor=white)](#installation)

> 🧭 *一个面向结构化情报分析的 CLI 与工作流内核，把原始来源组织成可复用的分析产物。*

Glassroom 是一个面向结构化情报分析的 CLI 与工作流内核。

它的目标，是把原始来源逐步组织成可复用的分析产物：source bundle、bias analysis、structured analysis、shared case object，以及后续教学页或写作输出。

## 安装

```bash
npx glassroom install openclaw
npx glassroom install project
```

当前已经可用的命令：

- `glassroom install openclaw`
- `glassroom install project`
- `glassroom list-skills`
- `glassroom assemble case`

版本命令：

- `glassroom --version`
- `glassroom version`

只安装指定 skills：

```bash
npx glassroom install openclaw --skills glassroom-router,glassroom-source-intake
```

查看可用 skills：

```bash
npx glassroom list-skills
```

组装共享 case object：

```bash
glassroom assemble case \
  --base-case examples/base-case.json \
  --source-card examples/source-card.json \
  --bias-analysis examples/bias-analysis.json \
  --mitigation-pack examples/mitigation-pack.json \
  --structured-analysis examples/structured-analysis.json \
  --out-json /tmp/glassroom-case.json \
  --out-md /tmp/glassroom-case.md
```

如果 npm 暂时不可用，见下方 [安装方式](#installation) 中的 GitHub 与手动 fallback。

<a id="what-glassroom-is"></a>
## ✨ Glassroom 到底是什么

Glassroom 不是单个 Agent，也不是单个 Skill。

它更像一个两层结构的项目：

- workflow core
  - shared case object
  - 中间产物
  - 可复用分析模块

- integration layer
  - 可挂载的 OpenClaw skills
  - CLI 入口
  - public-safe 文档与模板

如果你需要的是一条从原始来源走向结构化分析产物的路径，Glassroom 更适合下面这些事情：

- 把分散的分析结果收束成共享 case object
- 让 source、bias、mitigation、structured analysis 这些层彼此连通
- 为后续 HTML 教学页、课程写作、讲授材料保留稳定输入
- 把流程能力沉淀成 schema 和模块，而不是只藏在 prompt 里
- 保留真正可复用的教学界面结构，而不是反复做一次性课件

<a id="what-glassroom-is-not"></a>
## 🚫 它不是什么

它不是：

- 通用型作文生成器
- 一堆彼此无关的课堂 prompt 集合
- 课堂原始资产的直接公开通道
- 在核心工作流契约还没稳定前就急着做成大而全平台

Glassroom 的开源思路很明确：先公开可移植的骨架，再逐步放出真正 public-safe、能独立成立的模块。

<a id="quick-start"></a>
## ⚡ 快速开始

当前最快的体验方式，是用仓库里已经准备好的 public-safe 示例输入，先组装一个共享 case object。

### CLI 路径

```bash
glassroom assemble case \
  --base-case examples/base-case.json \
  --source-card examples/source-card.json \
  --bias-analysis examples/bias-analysis.json \
  --mitigation-pack examples/mitigation-pack.json \
  --structured-analysis examples/structured-analysis.json \
  --out-json /tmp/glassroom-case.json \
  --out-md /tmp/glassroom-case.md
```

### Package 脚本路径

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

如果你想分别跑分析模块，也可以直接执行：

```bash
python3 packages/cognitive-bias/build_bias_analysis.py \
  --input examples/bias-input.json \
  --out-json /tmp/bias-analysis.json \
  --out-md /tmp/bias-analysis.md

python3 packages/structured-analysis/build_structured_analysis.py \
  --input examples/structured-analysis-input.json \
  --out-json /tmp/structured-analysis.json \
  --out-md /tmp/structured-analysis.md

python3 packages/source-intake/fetch_source_bundle.py \
  --input examples/source-input.json \
  --out-json /tmp/source-bundle.json \
  --out-md /tmp/source-bundle.md
```

<a id="installation"></a>
## 📦 安装方式

Glassroom 已经带有安装器 CLI。

推荐安装路径现在是 npm。

### 从 npm 安装

安装到 OpenClaw workspace：

```bash
npx glassroom install openclaw
```

安装到当前项目 workspace：

```bash
npx glassroom install project
```

只安装指定 skills：

```bash
npx glassroom install openclaw --skills glassroom-router,glassroom-source-intake
```

查看可用 Glassroom skills：

```bash
npx glassroom list-skills
```

### GitHub fallback

如果 npm 暂时不可用，仍然可以直接从 GitHub 运行：

```bash
npx github:NanAquarius/Glassroom install openclaw
npx github:NanAquarius/Glassroom install project
npx github:NanAquarius/Glassroom list-skills
```

### 发给 AI CLI 的一句话安装

如果你是在 Claude Code、OpenCode 或类似 coding-agent CLI 里让 AI 帮你安装：

```text
Run `npx glassroom install project` in this workspace and tell me which Glassroom skills are now available.
```

如果工具可以访问你的 OpenClaw workspace：

```text
Run `npx glassroom install openclaw` and tell me which Glassroom skills were installed into ~/.openclaw/workspace/skills/.
```

### 手动安装 fallback

如果你暂时不想走 installer CLI，也依然可以 clone 仓库后，手动把 `skills/` 下面的目录复制或软链接到：

- `~/.openclaw/workspace/skills/`
- `./skills/`

安装器的价值，就是把这套过程变得更短、更干净，也更方便重复执行。

<a id="current-public-scope"></a>
## 🧩 当前已公开能力

当前这版公开出来的 Glassroom，已经包含：

- 共享 Glassroom case schema
- 描述模块如何围绕该 schema 协作的 workflow contract
- `case-assembler`
- `cognitive-bias`
- `structured-analysis`
- `source-intake`
- 一套去标识化后的 UI 模板参考库
- 一层可挂载的开源 `skills/`
- 一个已经具备安装命令与首个真实分析命令 `assemble case` 的 CLI

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

Glassroom 默认使用共享 case object 作为工作单元。

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

- [`packages/source-intake/`](./packages/source-intake/)
  - 抓取、分类并结构化来源材料，支持更强的上游原始材料获取

### Integration 层

- [`skills/glassroom-router/`](./skills/glassroom-router/)
- [`skills/glassroom-source-intake/`](./skills/glassroom-source-intake/)
- [`skills/glassroom-case-assembler/`](./skills/glassroom-case-assembler/)
- [`skills/glassroom-cognitive-bias/`](./skills/glassroom-cognitive-bias/)
- [`skills/glassroom-structured-analysis/`](./skills/glassroom-structured-analysis/)
- [`bin/glassroom.js`](./bin/glassroom.js)

这些 Integration surface 架在 package 层之上。

也就是说：真正的执行逻辑在 `packages/`，而 `skills/` 与 `bin/` 分别提供可挂载入口和 CLI 入口。

<a id="ui-template-library"></a>
## 🎨 UI 模板库

Glassroom 现在也开始有一套 public-safe UI template library：

- [`docs/ui-template-library/README.md`](./docs/ui-template-library/README.md)
- [`docs/ui-template-library/templates/`](./docs/ui-template-library/templates/)
- [`docs/ui-template-library/reference-pages/`](./docs/ui-template-library/reference-pages/)

这套库的定位，不是拿来原样复刻课堂页面。

它的作用，是在去标识化之后，把真正可复用的教学结构、信息架构和 UI 逻辑保留下来。

<a id="repository-layout"></a>
## 🗂 仓库结构

```text
Glassroom/
├── bin/
├── docs/
│   └── ui-template-library/
├── examples/
├── packages/
│   ├── case-assembler/
│   ├── cognitive-bias/
│   ├── source-intake/
│   └── structured-analysis/
├── schemas/
├── skills/
│   ├── glassroom-router/
│   ├── glassroom-source-intake/
│   ├── glassroom-case-assembler/
│   ├── glassroom-cognitive-bias/
│   └── glassroom-structured-analysis/
├── package.json
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── .gitignore
├── LICENSE
├── README.md
└── README.zh-CN.md
```

<a id="roadmap-direction"></a>
## 🛣 路线图方向

近阶段优先级：

1. 继续把 CLI 往真实分析命令扩展
2. 扩大 source-ingestion coverage
3. 逐步公开更多 renderer 与 delivery 层
4. 继续保持 OpenClaw integration 的轻薄与 package-backed 结构

后续适合继续公开的模块族，仍然包括：

- OSINT pitfalls and mitigations
- case HTML rendering
- course writing outputs

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

但它已经不再是“只有文档的仓库”了：核心 contract 已公开，第一批分析模块已公开，第一批去标识化 UI 参考模式已公开，而 CLI 现在也已经同时具备安装命令和首个真实分析命令。

接下来会继续把本地 Glassroom 里更成熟、也更适合公开的部分一点点抽出来，而不是一股脑倒进去。

## License

MIT

## Changelog

见 [CHANGELOG.md](./CHANGELOG.md)。

## Contributing

见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## Security

见 [SECURITY.md](./SECURITY.md)。

---

<div align="center">

*如果 Glassroom 对你的教学、分析流程或 workflow 设计有帮助，欢迎点个 Star、提个 issue，或者告诉我你怎么在用它。*

<sub>⭐ <a href="https://github.com/NanAquarius/Glassroom">Star</a> &nbsp;·&nbsp; 🐛 <a href="https://github.com/NanAquarius/Glassroom/issues">Issue</a> &nbsp;·&nbsp; 🤝 <a href="https://github.com/NanAquarius/Glassroom/pulls">PR</a></sub>

</div>
