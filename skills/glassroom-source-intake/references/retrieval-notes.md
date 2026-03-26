# Retrieval notes

## Goal

Do not stop at a weak snippet if the upstream page can be fetched as a fuller text source.

## Current provider-aware extraction

### FRUS / history.state.gov

- prefer document pages, not only collection indexes
- extract from the main content area
- preserve subject and document title when available

### WikiLeaks PlusD

- prefer direct cable pages (`/plusd/cables/...`)
- extract from `tagged-text` or the main cable text container
- treat the direct cable page as stronger than the generic search form

## Retrieval-quality rule

Classify retrieval quality from extracted text length:

- `high` >= 4000 chars
- `medium` >= 1500 chars
- `low` >= 500 chars
- `insufficient` < 500 chars

If retrieval quality is `insufficient`, do not present the source as fully captured.

## Workflow rule

Preferred sequence when the user gives a URL and wants real source access:

1. fetch a fuller source bundle
2. check retrieval quality
3. only then build the source card
4. if needed, recommend stronger upstream alternatives
