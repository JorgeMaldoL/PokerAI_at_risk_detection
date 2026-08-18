# Poker AI Coach with Addiction Screening

Learn about us: <https://jorgemaldol.github.io/PokerAI_at_risk_detection/>

A poker app that helps people learn Poker while also studying gambling behavior.

The app collects gameplay information such as bet sizes, results, and how long a player takes to make a decision. This information can be used to look for behaviors linked to risky gambling, such as increasing bets after losing.

The project has two main parts:

* **Poker game:** A Streamlit app where you can play Poker against a computer or another player. It also has an optional Learning Coach that gives feedback on your decisions.
* **Research:** Jupyter notebooks that analyze the Bustabit gambling dataset and look for risky betting patterns. The project also uses an XGBoost model to place players into different risk levels.

There is also a FastAPI backend for a GTO poker trainer. The backend works, but it is not connected to the Streamlit app yet.

## Project Layout

| Folder/File                     | What it does                           |
| ------------------------------- | -------------------------------------- |
| `streamlit/`                    | Poker game and multiplayer backend     |
| `src/poker_coach/api/`          | Backend for the GTO trainer            |
| `src/poker_coach/upi_parser.py` | Reads PioSOLVER data                   |
| `src/poker_coach/upi_engine.py` | Turns solver data into poker scenarios |
| `src/poker_coach/pipeline.py`   | Handles the solver data process        |
| `notebooks/`                    | Data analysis and machine learning     |
| `Data/`                         | Datasets and sample poker scenarios    |
| `models/`                       | Trained XGBoost model                  |
| `tests/`                        | Tests for the project                  |
| `plans/backend_spec.md`         | Backend plan                           |

## Setup

### 1. Clone the Repository

HTTPS:

```bash
git clone https://github.com/althexshi/chess.com-but-for-poker.git
```

SSH:

```bash
git clone git@github.com:althexshi/chess.com-but-for-poker.git
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the Dependencies

```bash
pip install -e ".[dev]"
```

This installs the libraries needed for the project, including:

* pandas
* NumPy
* Matplotlib
* SciPy
* scikit-learn
* XGBoost
* imbalanced-learn
* FastAPI
* Streamlit
* Jupyter
* pytest

You do not need to install the Streamlit requirements separately.

### 4. Environment Variables

The GTO trainer uses Gemini through Google Vertex AI for its AI coaching feature.

If you want to use this feature, create a `.env` file in the main project folder:

```env
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=global
GOOGLE_GENAI_USE_VERTEXAI=True
```

The Learning Coach in the Streamlit app does not need an API key.

## Running the Poker App

Start the app with:

```bash
python -m streamlit run streamlit/app.py
```

You can then play against the computer using **Vs Computer** mode.

The Learning Coach can be turned on from the sidebar.

### Multiplayer

Multiplayer needs its own backend.

Open another terminal and run:

```bash
cd streamlit
python -m uvicorn backend:app --reload --port 8000
```

Then open the Streamlit app in two browser windows.

One player can create a room and the other player can join it.

If the frontend and backend are hosted separately, use the `POKER_API_URL` environment variable to tell the app where the backend is located.

More information is in `streamlit/README.md`.

## Running the GTO Trainer

Start the GTO backend with:

```bash
uvicorn poker_coach.api.main:app --reload
```

The backend gives the player poker situations and checks their decisions against poker solver results.

The main API endpoints are:

```text
/api/scenarios/next
/api/evaluate
```

Player decisions and other gameplay information are saved in a local SQLite database.

Before using the trainer, load the sample scenarios:

```bash
python -m poker_coach.ingest Data/sample_scenarios.json
```

**Note:** The GTO trainer and Streamlit app are currently separate. The Streamlit app does not use the GTO backend yet.

## Data Analysis

The research part of the project uses the Bustabit dataset to study gambling behavior.

The notebooks look at things like:

* Increasing bets after a loss
* Bet sizes
* Betting patterns
* Player activity
* Session behavior
* Win and loss streaks
* Different types of players

The main machine learning notebook is:

```text
notebooks/05_training_and_testing.ipynb
```

The project uses the data from these analyses to train an XGBoost model.

The model puts players into different **risk levels** based on their betting behavior.

## Running the Notebooks

Start Jupyter with:

```bash
jupyter lab
```

Then open the notebooks inside the `notebooks/` folder.

## Running Tests

Run the tests with:

```bash
pytest
```

## Current Status

* **Poker app:** Complete and playable
* **Play against computer:** Complete
* **Multiplayer:** Complete
* **Bustabit analysis:** Complete
* **XGBoost risk model:** Trained and tested
* **GTO backend:** Built and tested
* **GTO trainer in the Streamlit app:** Not connected yet
* **Gemini AI coaching:** Built, but not connected to the API yet

## What's Next

The next major step is connecting the GTO trainer to the Streamlit app.

This would allow players to play poker in the app and get feedback based on poker solver data.

The larger goal is to combine poker training with gambling behavior analysis. This could allow the project to teach poker strategy while also identifying betting patterns that may be linked to risky gambling behavior.
