---
name: glassroom-cognitive-bias
description: Analyze cognitive traps and biases in case materials for Glassroom. Use when the task is to identify, explain, compare, or teach biases such as confirmation bias, anchoring, mirror imaging, overconfidence, availability heuristic, groupthink, or related reasoning failures in a source or case.
---

# glassroom-cognitive-bias

Use this skill when the task is to explain how reasoning goes wrong in a source, argument, memo, or case.

## Core workflow

1. identify the decision frame or claim
2. locate the vulnerable assumptions
3. map those assumptions to one or more bias types
4. explain why the bias is plausible in this case
5. suggest a more disciplined reading or mitigation step

## Output

Default target: enrich the shared Glassroom case object, especially `biases`, `assumptions`, and bias-oriented interpretation.

For each bias, produce:

- bias name
- evidence in the text
- why it fits
- what a better analytic move would be

## Default executable workflow

```bash
python3 scripts/build_bias_analysis.py \
  --input /tmp/bias-input.json \
  --out-json /tmp/bias-analysis.json \
  --out-md /tmp/bias-analysis.md
```

Use `references/bias-input-template.json` as the input shape.

## Read on demand

- `references/bias-input-template.json`
