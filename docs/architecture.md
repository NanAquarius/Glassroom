# Glassroom architecture notes

Glassroom is being opened in layers.

## Near-term architecture

- **Shared schema layer**: one reusable case object
- **Workflow modules**: each module enriches part of that object
- **Renderer / output layers**: HTML pages, worksheets, writing outputs

## Why this structure

The open-source version should not begin as a pile of isolated prompts or opaque scripts.

The stable thing to publish first is the shared data contract and a few clean modules that can be composed.

## Current extraction order

1. shared schema
2. workflow contract
3. case assembler
4. next modules after public-safe cleanup
