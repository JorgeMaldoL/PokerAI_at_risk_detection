# 04: GTO Action Evaluation Endpoint

## What to build
The ability for a training player to submit a chosen action (e.g., Check, Fold, Bet size) for a specific scenario and receive immediate quantitative feedback showing how their choice compares to the GTO solver's exact percentages.

## Acceptance criteria
*   Endpoint `POST /api/evaluate` is exposed in FastAPI, accepting scenario ID and user action.
*   It queries the SQLite scenario database and compares the user's action against the actual GTO weights.
*   Returns the complete comparison metrics (e.g. "User Choice: Check. GTO Frequencies: Check 20%, Bet 33% 80%").
*   Verified via FastAPI `TestClient` asserting HTTP response data matches solver GTO frequencies.

## Blocked by
*   `03-gto-scenario-database-endpoint`

## Status
ready-for-agent
