# 03: GTO Scenario Database Setup & Next Scenario API Endpoint

## What to build
The ability for an interactive client to request a fresh training scenario (board, hole cards, active positions, pot size) over HTTP, backed by a local SQLite database that stores pre-parsed scenario JSON structures.

## Acceptance criteria
*   Local SQLite database schema is defined to store GTO scenario nodes (with JSON support).
*   Includes a CLI script to ingest pre-parsed scenario JSON files into the database.
*   Endpoint `GET /api/scenarios/next` is exposed in FastAPI and returns a randomized, complete training spot to the user.
*   Verifiable end-to-end using FastAPI `TestClient` to fetch a full scenario payload over HTTP.

## Blocked by
*   `01-upi-string-parser`

## Status
ready-for-agent
