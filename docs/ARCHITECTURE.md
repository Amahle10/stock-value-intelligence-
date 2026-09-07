# Architecture

The project is organized as a monorepo with a FastAPI backend and a React + Vite frontend.

## Backend
- `app/main.py`: application entry point.
- `app/api/routes`: REST endpoints.
- `app/analytics`: price, time, valuation, reversal, and feature logic.
- `app/data`: CSV and external providers plus cleaning and scraping modules.
- `app/ml`: model training and prediction baseline.
- `app/db`: SQLAlchemy data access layer.

## Frontend
- `src/pages/Dashboard.tsx`: dashboard layout and main analytics display.
- `src/services/api.ts`: API client wrapper.
- `src/types`: shared TypeScript interfaces.

## Why these libraries
- Pandas: DataFrame operations and cleaning.
- NumPy: vectorized calculations.
- SciPy: distribution and statistical helpers.
- Scikit-learn: logistic model baseline.
- FastAPI: REST API and docs.
- Plotly: browser-based visualisations.
