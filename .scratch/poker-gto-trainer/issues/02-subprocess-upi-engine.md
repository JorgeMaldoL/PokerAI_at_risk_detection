# 02: Automated Local PioSOLVER Subprocess UPI Engine

## What to build
A background pipeline automation harness that spawns local headless PioSOLVER instances via CLI, communicates using Universal Poker Interface (UPI) text commands, extracts strategy node matrices, and automatically runs the UPI String Parser (from Ticket 01) to save parsed files.

## Acceptance criteria
*   Launches PioSOLVER as a headless background subprocess with standard I/O streams redirected.
*   Successfully issues sequences of UPI instructions (`load_tree`, `show_strategy`, etc.) programmatically.
*   Seamlessly feeds stdout stream matrices into the UPI String Parser to generate local scenario JSON files.
*   Verified end-to-end using mock standard I/O streams in CI/CD without needing a real solver binary.

## Blocked by
*   `01-upi-string-parser`

## Status
ready-for-agent
