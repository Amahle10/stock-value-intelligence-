# API

The backend exposes the research endpoints for market, analytics, and model analysis.

## Endpoints
- GET /api/health
- GET /api/market/pairs
- GET /api/market/latest/{pair}
- GET /api/market/history/{pair}
- GET /api/market/data-quality/{pair}
- GET /api/analytics/summary/{pair}
- GET /api/analytics/time/{pair}
- GET /api/analytics/valuation/{pair}
- GET /api/analytics/reversal/{pair}
- GET /api/analytics/distribution/{pair}
- GET /api/models/status/{pair}
- GET /api/models/prediction/{pair}
- POST /api/models/train/{pair}

Swagger is available at /docs.
