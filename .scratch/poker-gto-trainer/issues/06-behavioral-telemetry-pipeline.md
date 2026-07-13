# 06: Behavioral Telemetry Pipeline

## What to build
The ability to silently capture, measure, and record a player's behavior (including timestamp, chosen action, bet sizing, previous outcomes, and decision response time) to support downstream analysis of loss-chasing and tilt by the addiction screening team.

## Acceptance criteria
*   Asynchronously captures player action timestamp and response duration during evaluation.
*   Logs telemetry records (`UserID`, `Bet` size, `PrevOutcome`, `ResponseTime`) to a dedicated local SQLite table or CSV.
*   Format is fully aligned with the requirements of the `02_loss_chasing_analysis.ipynb` data format.
*   Verified via integration test hitting `/api/evaluate` and verifying the resulting telemetry record is correctly appended without increasing API latency.

## Blocked by
*   `04-gto-evaluation-endpoint`

## Status
ready-for-agent
