# 05: LLM Coach Integration

## What to build
The ability for a player to receive human-readable, strategic, concept-driven poker advice explaining *why* the GTO solver preferred a particular action over another, using an asynchronous LLM client to bridge cold GTO numbers with theoretical game logic.

## Acceptance criteria
*   Integrates an asynchronous LLM API wrapper inside `/api/evaluate`.
*   Generates a structured prompt describing the board cards, player position, user decision, and solver frequencies.
*   Instructs the LLM as an expert poker coach to explain range advantages, blockers, or equity shifts.
*   The explanation string is returned inside the `/api/evaluate` JSON response.
*   Tested by mocking the LLM API client to prevent real execution costs in tests.

## Blocked by
*   `04-gto-evaluation-endpoint`

## Status
ready-for-agent
