# FX Price Intelligence

FX Price Intelligence is a research-oriented forex analytics project focused on studying price behaviour, statistical regimes, and baseline machine-learning probabilities.

It is not an automated trading bot and does not execute trades.

## Project structure
```text
fx-price-intelligence/
├── backend/
├── frontend/
├── docs/
├── README.md
└── .gitignore
```

## Linux setup
This project was validated on Python 3.12.14. Python 3.14 currently crashes with the pinned scientific stack in this environment, so use a Python 3.12 virtual environment for the backend.

```bash
mkdir fx-price-intelligence
cd fx-price-intelligence
python3.12 -m venv .venv312
source .venv312/bin/activate
python -m pip install --upgrade pip setuptools wheel
cd backend
pip install -r requirements.txt
cd ../frontend
npm install
```

## Environment variables
```bash
cd backend
cp .env.example .env
```

## Backend startup
```bash
cd backend
source ../.venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger documentation: http://localhost:8000/docs

## Frontend startup
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

## Data loading
Sample CSV files in `backend/data/sample` are loaded automatically when an external provider is not configured.

## Model training
```bash
curl -X POST http://localhost:8000/api/models/train/EUR/USD
```

## Tests
```bash
cd backend
pytest
```

## Main analytics signals
- statistically expensive
- statistically cheap
- upward pressure
- downward pressure
- historical reversal probability
- historical continuation probability
- model-estimated probability

This project intentionally reports historical patterns and model estimates rather than guaranteed trade directions.
