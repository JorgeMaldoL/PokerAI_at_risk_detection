# 01: UPI String Parser (PioSOLVER Extraction)

## What to build
The ability to process raw text matrices outputted by PioSOLVER's Universal Poker Interface (UPI) `show_strategy` command and parse them into a lightweight, minimized JSON representation. This allows the backend to handle complex GTO solver data in a compact web-ready format.

## Acceptance criteria
*   A parser module receives a text representation of a PioSOLVER UPI strategy matrix.
*   The parser outputs a clean JSON dictionary adhering to the specified GTO strategy schema (combos mapped to their exact action weights, totaling 1.0/100%).
*   Parsed and serialized outputs for a single node must stay under 50KB to preserve web performance.
*   Verified via automated unit tests mocking stream outputs (Pipeline Seam).

## Blocked by
*   None — can start immediately.

## Status
ready-for-agent
