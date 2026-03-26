---
name: glassroom-source-intake
description: Ingest and classify source materials for the Data-Driven Intelligence Analysis course. Use when the user provides raw files, links, cables, official statements, PDFs, or articles and needs source type identification, metadata extraction, reliability framing, structured source cards, or help finding course-appropriate primary materials from professional archives and official repositories.
---

# glassroom-source-intake

Use this skill to turn raw course materials into structured source objects **and** to locate better raw materials when the current source base is weak.

## Main tasks

- identify source type
- extract basic metadata
- distinguish primary vs secondary material
- note whether a source is official, leaked, academic, journalistic, or commentary
- fetch fuller text from supported live sources when the task requires real source access
- produce a source card before deeper analysis starts
- recommend stronger primary-source replacements when the current material is too shallow or too derivative

## Source priority rule

For this course, prefer sources in this order:

1. official archives and declassified records
2. official government / international organization statements
3. academic or institutional primary-document collections
4. reputable journalism and secondary analysis
5. commentary / blogs / summaries

If stronger upstream material exists, say so explicitly instead of treating a weak secondary source as the best available evidence.

## Professional-source discovery rule

When the user asks for "original materials", "raw materials", or gives a weak derivative source, search professional repositories first.

Typical high-value source families:

- diplomatic cables and declassified archives
- intelligence reading rooms
- official press releases and policy statements
- court / legal records when relevant
- academic repositories for scholarly source trails

## Default executable workflow

When the task requires fuller source capture from a live URL, fetch a source bundle first:

```bash
python3 scripts/fetch_source_bundle.py \
  --input /tmp/source-input.json \
  --out-json /tmp/source-bundle.json \
  --out-md /tmp/source-bundle.md
```

Then build the source card from that richer bundle:

```bash
python3 scripts/build_source_card.py \
  --input /tmp/source-bundle.json \
  --out-json /tmp/source-card.json \
  --out-md /tmp/source-card.md
```

If enough metadata already exists and no live fetch is needed, you can still build a source card directly with:

```bash
python3 scripts/build_source_card.py \
  --input /tmp/source-input.json \
  --out-json /tmp/source-card.json \
  --out-md /tmp/source-card.md
```

Use `references/source-input-template.json` as the input shape.
Use `references/source-bundle-template.json` as the fetched-bundle shape.

## Output

Default target: enrich the shared Glassroom case object, especially `sourceCards` and basic case metadata.

Produce either:

- a fuller `source bundle` when live retrieval is required
- or a concise `source card` when metadata is already sufficient

A richer `source bundle` should include:

- canonical title or subject
- provider / fetch status
- extraction method
- fuller text capture
- retrieval quality
- whether the captured text is sufficient for deeper analysis

A `source card` should include:

- title
- source type
- date
- author / institution
- likely audience
- reliability note
- why it matters for the course
- whether it should be treated as primary evidence
- recommended next step

If discovery was required, also provide a short ranked list of candidate upstream sources.

## Read on demand

- `references/source-input-template.json`
- `references/source-bundle-template.json`
- `references/source-card-template.json`
- `references/source-types.md`
- `references/source-provider-map.md`
- `references/source-search-playbook.md`
- `references/retrieval-notes.md`
