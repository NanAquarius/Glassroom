# Contributing

Thanks for contributing to Glassroom.

## What belongs here

Glassroom is for structured intelligence analysis workflows.

Good contributions usually improve one of these layers:

- source ingestion
- bias analysis
- structured analytic techniques
- shared case assembly
- public-safe renderers
- OpenClaw integration surfaces

## Contribution rules

- Prefer stable structure over clever prompt tricks.
- Keep intermediate artifacts reusable.
- Preserve the shared case object contract.
- Only contribute public-safe, portable, maintainable material.
- Do not submit classroom-owned or personally identifying teaching assets.

## Before opening a PR

- Run the CLI help surface:
  - `node bin/glassroom.js --help`
- Verify the current install surface:
  - `node bin/glassroom.js list-skills --json`
- Verify the first analysis command:
  - `node bin/glassroom.js assemble case --out-json /tmp/glassroom-case.json --out-md /tmp/glassroom-case.md --base-case examples/base-case.json --source-card examples/source-card.json --bias-analysis examples/bias-analysis.json --mitigation-pack examples/mitigation-pack.json --structured-analysis examples/structured-analysis.json`
- Verify packaging:
  - `npm pack --dry-run`

## PR guidance

Include:

- what changed
- why it matters to the workflow
- whether it changes the case schema, CLI surface, or package boundaries
- any follow-on migration or release implications

If the change affects published behavior, update `CHANGELOG.md`.
