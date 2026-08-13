# Deep Research Engine Specification

Status: proposed

## Purpose

Jarvis must eventually support serious research rather than simple search.

## Required Capabilities

- multi-source search
- source collection
- source ranking
- source credibility evaluation
- document extraction
- PDF analysis
- webpage analysis
- video/transcript analysis
- cross-source comparison
- contradiction detection
- evidence extraction
- citation tracking
- research memory
- report generation
- iterative research
- follow-up research
- research tasks running in the background

## Background Execution

A research task must be able to continue working while the user performs
other activities — this makes it a long-running task under
`task_system_spec.md`, with checkpoints, progress reporting, and
notification on completion or on finding something notable.

## Relationship to Other Systems

- Findings populate Research Memory (`memory_spec.md`).
- Research uses the AI Router (`ai_provider_spec.md`) to select appropriate
  models per sub-task (e.g. vision for document images, reasoning for
  contradiction detection).
- Source access over the network requires the `NETWORK` capability
  (`permissions_model.md`).
