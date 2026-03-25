# Glassroom

> An open-source workflow core for case-based intelligence analysis teaching artifacts.

Glassroom is the open-source version of a case-based teaching and analysis workflow.

It is designed for projects that need more than “generate some course text” — they need a shared case object, stable intermediate artifacts, structured analytic outputs, and room for downstream rendering into HTML pages, worksheets, or writing deliverables.

## What this repository is for

Use Glassroom when you want to build or extend a workflow that can:

- turn fragmented analysis outputs into a shared case object
- keep source, bias, mitigation, and structured-analysis layers connected
- support downstream HTML teaching pages or writing deliverables
- expose a reusable schema instead of trapping logic inside one-off prompts

## Current scope

This initial open-source release includes:

- a shared Glassroom case schema
- a workflow contract describing how modules enrich that schema
- a first reusable module: `case-assembler`
- a public-safe `cognitive-bias` module
- a public-safe `structured-analysis` module

The repository is intentionally starting small.

The goal is to open the stable backbone first, then progressively add more public-safe modules.

## Roadmap direction

Planned public-facing module families include:

- source intake
- cognitive bias analysis
- OSINT pitfalls and mitigations
- structured analytic techniques
- case HTML rendering
- course writing outputs

## Repository layout

```text
Glassroom/
├── docs/
├── examples/
├── packages/
│   ├── case-assembler/
│   ├── cognitive-bias/
│   └── structured-analysis/
├── schemas/
├── .gitignore
├── LICENSE
└── README.md
```

## Shared unit of work

Glassroom uses a shared **case object** as the default unit of work.

See:

- [`schemas/glassroom-case.schema.json`](./schemas/glassroom-case.schema.json)
- [`docs/workflow-contract.md`](./docs/workflow-contract.md)

## First imported module: case-assembler

The first extracted module is the case assembler.

It merges partial outputs such as:

- source cards
- bias analysis
- mitigation packs
- structured analysis
- base case metadata

into one reusable Glassroom case object.

See:

- [`packages/case-assembler/README.md`](./packages/case-assembler/README.md)
- [`packages/case-assembler/assemble_case.py`](./packages/case-assembler/assemble_case.py)

## Quick examples

### Assemble a shared case object

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

### Build a bias-analysis pack

```bash
python3 packages/cognitive-bias/build_bias_analysis.py \
  --input packages/cognitive-bias/bias-input-template.json \
  --out-json /tmp/bias-analysis.json \
  --out-md /tmp/bias-analysis.md
```

### Build a structured-analysis pack

```bash
python3 packages/structured-analysis/build_structured_analysis.py \
  --input packages/structured-analysis/analysis-input-template.json \
  --out-json /tmp/structured-analysis.json \
  --out-md /tmp/structured-analysis.md
```

The repository includes public-safe example inputs under [`examples/`](./examples/) so the first module can be run immediately.

## Design principles

- prefer stable structure over clever inference
- make intermediate artifacts reusable
- keep the shared schema recoverable across modules
- separate workflow orchestration from presentation layers
- open-source only what is public-safe, portable, and maintainable

## Status

This repository is in an early extraction phase.

Expect the schema and module boundaries to keep improving as more Glassroom capabilities are opened up.
