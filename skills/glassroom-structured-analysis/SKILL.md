---
name: glassroom-structured-analysis
description: Apply structured analytic techniques for Glassroom workflows. Use when the user wants ACH, devil's advocacy, key assumptions checks, indicators/signposts, timelines, alternative hypotheses, or other disciplined analysis frameworks applied to a case.
---

# glassroom-structured-analysis

Use this skill to convert loose interpretation into a structured analytic method.

## Main use cases

Default target: enrich the shared Glassroom case object, especially `structuredAnalysis`, `policyQuestion`, and assumption checks.

- ACH
- devil's advocacy
- key assumptions check
- indicators and signposts
- chronology / timeline
- alternative explanation framing

## Rule

Choose the lightest method that will actually improve the judgment.

Do not use ACH by reflex if a simpler assumptions check or timeline would do.

## Default executable workflow

```bash
python3 scripts/build_structured_analysis.py \
  --input /tmp/structured-analysis-input.json \
  --out-json /tmp/structured-analysis.json \
  --out-md /tmp/structured-analysis.md
```

Use `references/analysis-input-template.json` as the input shape.

## Read on demand

- `references/analysis-input-template.json`
- `references/technique-selector.md`
