# cognitive-bias

Build a reusable Glassroom bias-analysis pack from a case excerpt and candidate bias list.

## What it does

This module helps turn a loose “there might be bias here” intuition into a structured artifact that downstream modules can reuse.

Default output fields are aligned with the shared Glassroom case object, especially:

- `biases`
- `assumptions`
- bias-oriented interpretation notes

## Usage

```bash
python3 packages/cognitive-bias/build_bias_analysis.py \
  --input examples/bias-input.json \
  --out-json /tmp/bias-analysis.json \
  --out-md /tmp/bias-analysis.md
```
