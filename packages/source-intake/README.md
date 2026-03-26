# source-intake

Fetch, classify, and structure source materials for Glassroom.

## What it does

This module is responsible for moving from "I have a link or a weak source" to a structured source object with enough provenance and enough captured text to support deeper analysis.

It can:

- classify the source type
- estimate whether the source is primary-like or secondary
- fetch fuller text from supported live sources
- score retrieval quality
- produce a source card for downstream Glassroom modules

## Usage

```bash
python3 packages/source-intake/fetch_source_bundle.py \
  --input /tmp/source-input.json \
  --out-json /tmp/source-bundle.json \
  --out-md /tmp/source-bundle.md

python3 packages/source-intake/build_source_card.py \
  --input /tmp/source-bundle.json \
  --out-json /tmp/source-card.json \
  --out-md /tmp/source-card.md
```

## Current provider-aware extraction

- FRUS / `history.state.gov`
- WikiLeaks PlusD cable pages
- generic HTML fallback
