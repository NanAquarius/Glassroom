# Changelog

All notable changes to Glassroom will be documented in this file.

## [0.2.5] - 2026-03-30

### Fixed

- Removed duplicate `cognitive-bias` and `structured-analysis` sections in `docs/workflow-contract.md`.
- Converted `schemas/glassroom-case.schema.json` from an empty-value skeleton to a proper JSON Schema (draft 2020-12) with types and descriptions.
- Added network error handling to `fetch_source_bundle.py` so fetch failures return a structured error instead of crashing.
- Refactored overly long line in `build_source_card.py` for readability.
- Expanded `.gitignore` with `.env`, `*.egg-info/`, `.pytest_cache/`, `coverage/`, `.mypy_cache/`.

## [0.2.4] - 2026-03-26

### Changed

- Added a Shell badge to the README header, matching the existing flat-square badge style.

## [0.2.3] - 2026-03-26

### Changed

- Added two working reference books to the README reference section: *OSINT Techniques* (2024) and *Structured Analytic Techniques for Intelligence Analysis* (2020).

## [0.2.2] - 2026-03-26

### Changed

- Rewrote the project About / short description to: "Glassroom is a structured intelligence analysis CLI and workflow core. It turns raw sources into reusable case objects and analytic outputs."

## [0.2.1] - 2026-03-26

### Changed

- Expanded the built-in Glassroom cognitive-bias catalog from 8 to 12 bias types.
- Upgraded mitigations from short generic advice to more explicit intelligence-tradecraft-oriented corrective steps.
- Added `recommendedTechnique`, `mitigationSteps`, and `sourceBasis` to bias-analysis outputs.
- Added `docs/bias-catalog.md` and refreshed bias examples and package docs.

## [0.2.0] - 2026-03-26

### Added

- `glassroom assemble case` CLI command as the first real analysis-oriented command.
- `glassroom --version` and `glassroom version` support.
- npm package metadata: homepage, repository, bugs, and keywords.
- Community-facing project files: `CHANGELOG.md`, `CONTRIBUTING.md`, and `SECURITY.md`.

### Changed

- Repositioned Glassroom more clearly as a structured intelligence analysis CLI and workflow core.
- Tightened README top section so install, current capabilities, and roadmap are easier to scan.
- Kept GitHub and npm release flow aligned with the project sync rule.

## [0.1.1] - 2026-03-26

### Changed

- Polished README badges for a cleaner GitHub presentation.

## [0.1.0] - 2026-03-26

### Added

- Initial npm release.
- Installer CLI with `install openclaw`, `install project`, and `list-skills`.
- Public package layer for case assembler, cognitive bias, structured analysis, and source intake.
