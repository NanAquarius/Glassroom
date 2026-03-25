---
name: glassroom-router
description: Route tasks for case-based intelligence analysis workflows in Glassroom. Use when the user needs help deciding whether a case should go through source intake, bias analysis, structured analysis, HTML case-page building, or course-writing output.
---

# glassroom-router

Use this as the **entry skill** for Glassroom workflows.

Its job is to decide which specialized Glassroom skill should handle the task.

## Route by task type

### 1. Source ingestion / classification

Use `glassroom-source-intake` when the task is about:

- identifying what a source is
- extracting metadata
- deciding whether material is primary / secondary / official / commentary
- turning raw case materials into structured source cards

### 2. Cognitive traps / bias analysis

Use `glassroom-cognitive-bias` when the task is about:

- confirmation bias
- anchoring
- mirror imaging
- overconfidence
- availability heuristic
- groupthink
- bias-aware reading of official text, cables, memos, or reporting

### 3. Structured analytic techniques

Use `glassroom-structured-analysis` when the task is about:

- ACH
- devil's advocacy
- key assumptions check
- indicators and signposts
- alternative analysis
- chronology / timeline / scenario framing

### 4. Interactive case pages / HTML teaching output

Use `glassroom-case-html` when the task is about:

- turning a case into an HTML learning page
- building an interactive bias explorer
- creating a teaching/demo page from analysis materials

### 5. Course writing deliverables

Use `glassroom-course-writing` when the task is about:

- analytic memo
- short essay
- discussion post
- presentation script
- course-ready prose based on prior analysis outputs

## Default sequence

When the user gives raw case material and no clear task:

1. classify sources with `glassroom-source-intake`
2. analyze cognitive traps with `glassroom-cognitive-bias`
3. apply one structured technique with `glassroom-structured-analysis`
4. if needed, convert to either HTML (`glassroom-case-html`) or prose (`glassroom-course-writing`)

## Read on demand

- `references/task-routing.md`
- `references/course-output-map.md`
- `../../schemas/glassroom-case.schema.json`
- `../../docs/workflow-contract.md`
