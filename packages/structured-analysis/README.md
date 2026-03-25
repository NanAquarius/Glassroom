# structured-analysis

Build a reusable Glassroom structured-analysis pack from a policy question, assumptions, hypotheses, and evidence.

## What it does

This module turns a loose interpretation into a more disciplined analytic artifact.

Default output fields are aligned with the shared Glassroom case object, especially:

- `structuredAnalysis`
- `policyQuestion`
- assumption checks

## Usage

```bash
python3 packages/structured-analysis/build_structured_analysis.py \
  --input examples/structured-analysis-input.json \
  --out-json /tmp/structured-analysis.json \
  --out-md /tmp/structured-analysis.md
```
