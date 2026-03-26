[English](./README.md) | [简体中文](./README.zh-CN.md)

# Glassroom

[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](#quick-start)
[![Markdown](https://img.shields.io/badge/Markdown-Docs-111827?style=flat-square&logo=markdown&logoColor=white)](#what-glassroom-is)
[![Node.js CLI](https://img.shields.io/badge/Node.js-CLI-339933?style=flat-square&logo=node.js&logoColor=white)](#installation)

> 🧭 *A structured intelligence analysis CLI and workflow core for turning raw sources into reusable analytic artifacts.*

Glassroom is a CLI and workflow core for structured intelligence analysis.

It helps move from raw sources to reusable outputs such as source bundles, bias analysis, structured analysis, shared case objects, and downstream teaching or writing artifacts.

## Install

```bash
npx glassroom install openclaw
npx glassroom install project
```

Current working commands:

- `glassroom install openclaw`
- `glassroom install project`
- `glassroom list-skills`
- `glassroom assemble case`

Version commands:

- `glassroom --version`
- `glassroom version`

Install only selected skills:

```bash
npx glassroom install openclaw --skills glassroom-router,glassroom-source-intake
```

List available skills:

```bash
npx glassroom list-skills
```

Assemble a shared case object:

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

If npm is unavailable, see [Installation](#installation) for GitHub and manual fallback paths.

<a id="what-glassroom-is"></a>
## ✨ What Glassroom is

Glassroom is not just an agent prompt pack and not just a single skill.

It is a project with two layers:

- a workflow core
  - shared case object
  - intermediate artifacts
  - reusable analysis modules

- an integration layer
  - mountable OpenClaw skills
  - a CLI surface
  - public-safe docs and templates

Use Glassroom when you want a workflow that can:

- turn fragmented analysis outputs into a shared case object
- keep source, bias, mitigation, and structured-analysis layers connected
- support downstream HTML teaching pages or writing deliverables
- expose a reusable schema instead of trapping logic inside one-off prompts
- preserve teaching patterns that can survive beyond a single class artifact

<a id="what-glassroom-is-not"></a>
## 🚫 What Glassroom is not

It is not trying to be:

- a generic essay generator
- a pile of unrelated classroom prompts
- a direct republication channel for classroom-owned artifacts
- a finished end-user platform before the core workflow contract is stable

The open-source rule is simple: publish the portable backbone first, then add public-safe modules that can stand on their own.

<a id="quick-start"></a>
## ⚡ Quick start

The fastest path right now is to assemble a shared case object from public-safe example inputs.

### CLI path

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

### Package script path

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

You can also run the public analysis modules directly:

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
## 📦 Installation

Glassroom ships with an installer CLI.

The preferred install path is npm.

### Install from npm

Install into an OpenClaw workspace:

```bash
npx glassroom install openclaw
```

Install into the current project workspace:

```bash
npx glassroom install project
```

Install only selected skills:

```bash
npx glassroom install openclaw --skills glassroom-router,glassroom-source-intake
```

List available Glassroom skills:

```bash
npx glassroom list-skills
```

### GitHub fallback

If npm is unavailable, you can still run Glassroom directly from GitHub:

```bash
npx github:NanAquarius/Glassroom install openclaw
npx github:NanAquarius/Glassroom install project
npx github:NanAquarius/Glassroom list-skills
```

### One-sentence install prompt for AI CLIs

For Claude Code, OpenCode, or similar coding-agent CLIs:

```text
Run `npx glassroom install project` in this workspace and tell me which Glassroom skills are now available.
```

If the tool has access to your OpenClaw workspace:

```text
Run `npx glassroom install openclaw` and tell me which Glassroom skills were installed into ~/.openclaw/workspace/skills/.
```

### Manual install fallback

If you want a manual path instead of the installer CLI, you can still clone the repository and copy or symlink the folders under `skills/` into either:

- `~/.openclaw/workspace/skills/`
- `./skills/`

The installer exists to make that process shorter, cleaner, and easier to repeat.

<a id="current-public-scope"></a>
## 🧩 Current public scope

This public release includes:

- a shared Glassroom case schema
- a workflow contract describing how modules enrich that schema
- `case-assembler`
- `cognitive-bias`
  - now includes an expanded built-in bias catalog with tradecraft-oriented mitigation steps
- `structured-analysis`
- `source-intake`
- a de-identified UI template reference library
- a mountable open-source `skills/` layer
- a CLI with install commands and a first real analysis command: `assemble case`

The goal is not to dump everything at once, but to open the stable backbone first and expand from there.

<a id="workflow-artifact-map"></a>
## 🗺 Workflow artifact map

The current core flow looks like this:

```text
partial analysis artifacts
  → shared case object
  → reusable intermediate outputs
  → HTML pages / writing deliverables / teaching artifacts
```

A more concrete version of that flow is:

```text
base-case.json
  + source-card.json
  + bias-analysis.json
  + mitigation-pack.json
  + structured-analysis.json
    → glassroom-case.json
    → glassroom-case.md
```

What this structure buys you:

- one reusable unit of work instead of many disconnected outputs
- cleaner handoff between modules
- easier rendering into multiple downstream formats
- less prompt-only logic trapped in one place

<a id="shared-unit-of-work"></a>
## 🔧 Shared unit of work

Glassroom uses a shared **case object** as the default unit of work.

See:

- [`schemas/glassroom-case.schema.json`](./schemas/glassroom-case.schema.json)
- [`docs/workflow-contract.md`](./docs/workflow-contract.md)

Not every module needs every field.

But the shared schema is the backbone that lets source intake, bias analysis, structured analysis, mitigations, rendering, and writing outputs keep talking to each other.

<a id="module-families"></a>
## 🧱 Module families

### Package layer

- [`packages/case-assembler/`](./packages/case-assembler/)
  - merges partial outputs into one reusable case object

- [`packages/cognitive-bias/`](./packages/cognitive-bias/)
  - turns candidate biases and excerpts into a reusable bias-analysis artifact

- [`packages/structured-analysis/`](./packages/structured-analysis/)
  - turns a policy question, hypotheses, assumptions, and evidence into a structured-analysis artifact

- [`packages/source-intake/`](./packages/source-intake/)
  - fetches, classifies, and structures source materials with provider-aware retrieval for stronger upstream evidence

### Integration layer

- [`skills/glassroom-router/`](./skills/glassroom-router/)
- [`skills/glassroom-source-intake/`](./skills/glassroom-source-intake/)
- [`skills/glassroom-case-assembler/`](./skills/glassroom-case-assembler/)
- [`skills/glassroom-cognitive-bias/`](./skills/glassroom-cognitive-bias/)
- [`skills/glassroom-structured-analysis/`](./skills/glassroom-structured-analysis/)
- [`bin/glassroom.js`](./bin/glassroom.js)

These integration surfaces sit on top of the package layer.

That means the executable path lives in `packages/`, while `skills/` and `bin/` provide mountable and CLI-facing entry points.

<a id="ui-template-library"></a>
## 🎨 UI template library

Glassroom also includes the beginning of a public-safe UI template library:

- [`docs/ui-template-library/README.md`](./docs/ui-template-library/README.md)
- [`docs/ui-template-library/templates/`](./docs/ui-template-library/templates/)
- [`docs/ui-template-library/reference-pages/`](./docs/ui-template-library/reference-pages/)

This library is for preserving reusable teaching-page structure after de-identification.

It is not a dump of classroom-owned pages.

The rule is to preserve instructional flow, information architecture, and reusable UI logic while removing personal, instructor, course-owner, and source-specific identity markers.

<a id="repository-layout"></a>
## 🗂 Repository layout

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
## 🛣 Roadmap direction

Near-term priorities:

1. strengthen the CLI around real analysis commands
2. expand source-ingestion coverage
3. expose more reusable renderer and delivery layers
4. keep OpenClaw integration thin and package-backed

Planned public-facing module families still include:

- OSINT pitfalls and mitigations
- case HTML rendering
- course writing outputs

<a id="design-principles"></a>
## 📐 Design principles

- prefer stable structure over clever inference
- make intermediate artifacts reusable
- keep the shared schema recoverable across modules
- separate workflow orchestration from presentation layers
- open-source only what is public-safe, portable, and maintainable

<a id="status"></a>
## 📌 Status

Glassroom is still in an early extraction phase.

But it is now past the “docs-only” stage: the core contract is public, the first analysis modules are public, the first de-identified UI reference pattern is public, and the CLI now includes both install flows and a first real analysis command.

Expect the schema, examples, module boundaries, and public-safe renderer layer to keep improving as more of the local Glassroom system is opened up.

## License

MIT

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Security

See [SECURITY.md](./SECURITY.md).

---

<div align="center">

*If Glassroom helps your teaching, analysis, or workflow design, consider giving it a Star, opening an issue, or sharing how you use it.*

<sub>⭐ <a href="https://github.com/NanAquarius/Glassroom">Star</a> &nbsp;·&nbsp; 🐛 <a href="https://github.com/NanAquarius/Glassroom/issues">Issue</a> &nbsp;·&nbsp; 🤝 <a href="https://github.com/NanAquarius/Glassroom/pulls">PR</a></sub>

</div>
