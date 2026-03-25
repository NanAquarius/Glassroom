# Glassroom workflow contract

This file keeps the Glassroom module suite aligned around a shared backbone.

## Shared unit of work

The default shared unit is a **course case object**.

Use [`../schemas/glassroom-case.schema.json`](../schemas/glassroom-case.schema.json) as the common conceptual schema.

Not every task needs every field, but all Glassroom modules should treat that schema as the common backbone.

## Module responsibilities

### source-intake

Produces or enriches:

- sourceCards
- title
- context
- keyActors
- recommendedDeliverables

### cognitive-bias

Produces or enriches:

- biases
- assumptions
- expertAnalysis (bias-oriented interpretation)

### osint-pitfalls

Produces or enriches:

- osintPitfalls
- mitigations
- evidence.ignored / provenance concerns

### structured-analysis

Produces or enriches:

- structuredAnalysis.method
- structuredAnalysis.outputs
- policyQuestion
- assumptions

### case-html

Consumes:

- case metadata
- evidence blocks
- biases
- mitigations
- structuredAnalysis outputs
- discussionPrompts
- expertAnalysis

### course-writing

Consumes:

- sourceCards
- evidence
- biases
- mitigations
- structuredAnalysis outputs
- expertAnalysis

## Design rule

Each Glassroom module should improve a shared case object, not create an unrelated standalone output by default.

Standalone outputs are fine, but the shared schema should remain recoverable from them.
