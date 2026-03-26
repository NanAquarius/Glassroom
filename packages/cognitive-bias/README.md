# cognitive-bias

Build a reusable Glassroom bias-analysis pack from a case excerpt and candidate bias list.

## What it does

This module turns a loose “there might be bias here” intuition into a structured artifact that downstream modules can reuse.

The current built-in bias catalog is now anchored to public intelligence-analysis tradecraft sources, especially:

- CIA — *Psychology of Intelligence Analysis*
- CIA — *Tradecraft Primer: Structured Analytic Techniques for Improving Intelligence Analysis*
- ODNI — analytic objectivity / ICD 203 analytic standards guidance

Default output fields are aligned with the shared Glassroom case object, especially:

- `biases`
- `assumptions`
- bias-oriented interpretation notes
- recommended mitigation technique
- mitigation steps

## Built-in cognitive traps

The package currently recognizes these built-in bias types:

- confirmation bias
- anchoring
- mirror imaging
- availability heuristic
- overconfidence
- groupthink
- wishful thinking
- premature closure
- framing effect
- satisficing
- recency bias
- fundamental attribution error

## Usage

```bash
python3 packages/cognitive-bias/build_bias_analysis.py \
  --input examples/bias-input.json \
  --out-json /tmp/bias-analysis.json \
  --out-md /tmp/bias-analysis.md
```

## Output shape

Each bias item now includes:

- `bias`
- `evidence`
- `whyItFits`
- `mitigation`
- `recommendedTechnique`
- `mitigationSteps`
