from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analytics import router as analytics_router
from app.api.routes.health import router as health_router
from app.api.routes.market import router as market_router
from app.api.routes.models import router as models_router

app = FastAPI(title="FX Price Intelligence", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(market_router)
app.include_router(analytics_router)
app.include_router(models_router)


@app.get("/")
def root():
    return {"message": "FX Price Intelligence backend is running."}
