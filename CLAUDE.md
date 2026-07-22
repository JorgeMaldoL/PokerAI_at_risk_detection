# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Poker AI Coach with Addiction Screening — an AI poker training tool that teaches GTO (Game Theory Optimal) strategy while silently logging behavioral telemetry (bet sizes, previous outcomes, response times) for downstream gambling addiction screening analysis.

Three components:
1. **FastAPI backend** (`src/poker_coach/api/`) — serves GTO scenarios, evaluates user actions against solver frequencies, logs telemetry
2. **Streamlit prototype** (`streamlit/app.py`) — interactive poker decision trainer (to be wired to the FastAPI backend)
3. **Data analysis notebooks** (`notebooks/`) — exploratory analysis of bustabit gambling data for loss-chasing behavior patterns

Backend spec in `plans/backend_spec.md`. Issue specs in `.scratch/poker-gto-trainer/issues/`.

## Commands

### Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Run the FastAPI backend
```bash
uvicorn poker_coach.api.main:app --reload
```

### Ingest GTO scenario data
```bash
python -m poker_coach.ingest <path-to-json-or-directory>
```

### Run the Streamlit app
```bash
python -m streamlit run streamlit/app.py
```

### Run tests
```bash
pytest
```

## Architecture

- `src/poker_coach/api/main.py` — FastAPI app with endpoints: `GET /api/scenarios/next`, `POST /api/evaluate`, `POST /api/users`
- `src/poker_coach/api/database.py` — SQLite connection, schema init, and query functions. DB stored at `data/poker_coach.db`
- `src/poker_coach/api/models.py` — Pydantic request/response schemas
- `src/poker_coach/ingest.py` — CLI to load GTO scenario JSON files into SQLite
- `streamlit/app.py` — single-file Streamlit app; `get_recommendation()` is the function to replace with API calls
- `config.py` defines the visualization palette (GRAPE_SODA, MUTED_TEAL, etc.) — use these for visual consistency

## Key Technical Details

- Python >=3.10 required
- SQLite database with JSON columns for GTO strategy storage; DB file is gitignored
- The `/api/evaluate` endpoint auto-creates users and logs telemetry on each call
- Telemetry schema (user_id, bet_size, prev_outcome, response_time_ms) matches `02_loss_chasing_analysis.ipynb` format
- Google Cloud/Vertex AI environment configured in `.env` for Gemini LLM coach integration (not yet wired)
- Tests use FastAPI `TestClient`; PioSOLVER subprocess tests use mock stdin/stdout
