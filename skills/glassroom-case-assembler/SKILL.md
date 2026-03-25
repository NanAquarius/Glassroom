---
name: glassroom-case-assembler
description: Assemble outputs from Glassroom skills into a shared case object. Use when source cards, bias analysis, OSINT mitigation packs, structured analysis outputs, or case metadata need to be merged into one reusable case bundle for HTML rendering or writing.
---

# glassroom-case-assembler

Use this skill to merge Glassroom intermediate outputs into a single shared case object.

## What it does

It combines outputs such as:

- source cards
- bias analysis
- OSINT mitigation packs
- structured analysis
- case metadata

into one assembled case JSON that downstream modules can consume.

## Rule

Prefer stable merging over clever inference.

If a field is missing, preserve that absence explicitly instead of inventing content.

## Default executable workflow

```bash
python3 scripts/assemble_case.py \
  --base-case /tmp/base-case.json \
  --source-card /tmp/source-card.json \
  --bias-analysis /tmp/bias-analysis.json \
  --mitigation-pack /tmp/mitigation-pack.json \
  --structured-analysis /tmp/structured-analysis.json \
  --out-json /tmp/glassroom-case.json \
  --out-md /tmp/glassroom-case.md
```

## Read on demand

- `references/assembler-inputs.md`
- `../../schemas/glassroom-case.schema.json`
- `../../docs/workflow-contract.md`
