[English](./README.md) | [简体中文](./README.zh-CN.md)

# Glassroom

[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Open source](https://img.shields.io/badge/open%20source-Glassroom-4f46e5)](#-what-glassroom-is-for)
[![Shared schema](https://img.shields.io/badge/schema-case%20object-7c3aed)](#-shared-unit-of-work)
[![Modules](https://img.shields.io/badge/modules-case--assembler%20%7C%20bias%20%7C%20structured-111827)](#-current-public-scope)
[![Skills](https://img.shields.io/badge/skills-mountable-0f766e)](#-module-families)
[![Examples](https://img.shields.io/badge/examples-public--safe-0f766e)](#-quick-start)
[![UI templates](https://img.shields.io/badge/ui%20templates-deidentified-9a3412)](#-ui-template-library)

> 🧭 *An open-source workflow core for turning case-based intelligence analysis into structured, teachable, reusable artifacts.*

## 📚 Contents

- [✨ What Glassroom is for](#-what-glassroom-is-for)
- [🚫 What Glassroom is not for](#-what-glassroom-is-not-for)
- [⚡ Quick start](#-quick-start)
- [🧩 Current public scope](#-current-public-scope)
- [🗺 Workflow artifact map](#-workflow-artifact-map)
- [🔧 Shared unit of work](#-shared-unit-of-work)
- [🧱 Module families](#-module-families)
- [🎨 UI template library](#-ui-template-library)
- [🗂 Repository layout](#-repository-layout)
- [🛣 Roadmap direction](#-roadmap-direction)
- [📐 Design principles](#-design-principles)
- [📌 Status](#-status)
- [License](#license)

Glassroom is the open-source version of a case-based teaching and analysis workflow.

It is built for projects that need more than “generate some course text” — they need a shared case object, stable intermediate artifacts, structured analytic outputs, and room for downstream rendering into HTML pages, worksheets, or writing deliverables.

## ✨ What Glassroom is for

Use Glassroom when you want a workflow that can:

- turn fragmented analysis outputs into a shared case object
- keep source, bias, mitigation, and structured-analysis layers connected
- support downstream HTML teaching pages or writing deliverables
- expose a reusable schema instead of trapping logic inside one-off prompts
- preserve teaching patterns that can survive beyond a single class artifact

## 🚫 What Glassroom is not for

It is **not** trying to be:

- a generic essay generator
- a pile of unrelated course prompts
- a direct republishing channel for classroom-owned artifacts
- a promise that every private teaching asset should become public
- a finished platform before the core contract is stable

The open-source rule is simple: publish the portable backbone first, then add public-safe modules that can stand on their own.

## ⚡ Quick start

The fastest path right now is to assemble a shared case object from public-safe example inputs.

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

You can also run the two public analysis modules directly:

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

The repository already includes public-safe example inputs under [`examples/`](./examples/), so the current open-source modules can be exercised immediately.

## 🧩 Current public scope

This initial public release includes:

- a shared Glassroom case schema
- a workflow contract describing how modules enrich that schema
- `case-assembler`
- `cognitive-bias`
- `structured-analysis`
- a de-identified UI template reference library
- a first mountable open-source `skills/` layer for router + reusable analysis skills

This repository is intentionally starting small.

The goal is not to dump everything at once, but to open the stable backbone first and expand from there.

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

## 🔧 Shared unit of work

Glassroom uses a shared **case object** as the default unit of work.

See:

- [`schemas/glassroom-case.schema.json`](./schemas/glassroom-case.schema.json)
- [`docs/workflow-contract.md`](./docs/workflow-contract.md)

Not every module needs every field.

But the shared schema is the backbone that lets source intake, bias analysis, structured analysis, mitigations, rendering, and writing outputs keep talking to each other.

## 🧱 Module families

### Package layer

- [`packages/case-assembler/`](./packages/case-assembler/)
  - merges partial outputs into one reusable case object

- [`packages/cognitive-bias/`](./packages/cognitive-bias/)
  - turns candidate biases and excerpts into a reusable bias-analysis artifact

- [`packages/structured-analysis/`](./packages/structured-analysis/)
  - turns a policy question, hypotheses, assumptions, and evidence into a structured-analysis artifact

### Mountable skill layer

- [`skills/glassroom-router/`](./skills/glassroom-router/)
- [`skills/glassroom-case-assembler/`](./skills/glassroom-case-assembler/)
- [`skills/glassroom-cognitive-bias/`](./skills/glassroom-cognitive-bias/)
- [`skills/glassroom-structured-analysis/`](./skills/glassroom-structured-analysis/)

These skills are package-backed.

That means the executable path lives in `packages/`, while `skills/` provides the mountable skill shape and task-routing surface.

### Planned expansion

- source intake
- OSINT pitfalls and mitigations
- case HTML rendering
- course writing outputs

## 🎨 UI template library

Glassroom now also includes the beginning of a public-safe UI template library:

- [`docs/ui-template-library/README.md`](./docs/ui-template-library/README.md)
- [`docs/ui-template-library/templates/`](./docs/ui-template-library/templates/)
- [`docs/ui-template-library/reference-pages/`](./docs/ui-template-library/reference-pages/)

This library is for preserving reusable teaching-page structure after de-identification.

It is **not** a dump of classroom-owned pages.

The rule is to preserve instructional flow, information architecture, and reusable UI logic while removing personal, instructor, course-owner, and source-specific identity markers.

## 🗂 Repository layout

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
└── README.md
```

## 🛣 Roadmap direction

Planned public-facing module families include:

- source intake
- cognitive bias analysis
- OSINT pitfalls and mitigations
- structured analytic techniques
- case HTML rendering
- course writing outputs

The repo is being opened in layers.

That means the order matters:

1. shared schema
2. workflow contract
3. reusable analysis modules
4. de-identified UI patterns
5. downstream renderers and delivery modules

## 📐 Design principles

- prefer stable structure over clever inference
- make intermediate artifacts reusable
- keep the shared schema recoverable across modules
- separate workflow orchestration from presentation layers
- open-source only what is public-safe, portable, and maintainable

## 📌 Status

Glassroom is still in an early extraction phase.

The core contract is now public, the first analysis modules are public, and the first de-identified UI reference pattern is public.

Expect the schema, examples, module boundaries, and public-safe renderer layer to keep improving as more of the local Glassroom system is opened up.

## License

MIT

---

<div align="center">

*If Glassroom helps your teaching, analysis, or workflow design, consider giving it a Star, opening an issue, or sharing how you use it.*

<sub>⭐ <a href="https://github.com/NanAquarius/Glassroom">Star</a> &nbsp;·&nbsp; 🐛 <a href="https://github.com/NanAquarius/Glassroom/issues">Issue</a> &nbsp;·&nbsp; 🤝 <a href="https://github.com/NanAquarius/Glassroom/pulls">PR</a></sub>

</div>
