# Poker AI Coach with Addiction Screening

## How to Install and Setup

### 1. Clone the repo

**HTTPS**
```bash
git clone https://github.com/althexshi/chess.com-but-for-poker.git
```

**SSH**
```bash
git clone git@github.com:althexshi/chess.com-but-for-poker.git
```

### 2. Create a virtual environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -e ".[dev]"
```

This installs the project's dependencies (pandas, seaborn, matplotlib, scipy), the `jupyter`/`jupyterlab` dev tooling, and makes `poker_coach` (the code in `src/poker_coach`) importable from the notebooks.