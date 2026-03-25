# case-assembler

Merge partial Glassroom outputs into a single reusable case object.

## What it does

It combines artifacts such as:

- base case metadata
- source cards
- bias analysis
- mitigation packs
- structured analysis

into one assembled case JSON that downstream modules can consume.

## Rule

Prefer stable merging over clever inference.

If a field is missing, preserve that absence explicitly instead of inventing content.

## Usage

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
