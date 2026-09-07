import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings:
    def __init__(self) -> None:
        self.api_url = os.getenv("FX_API_URL", "")
        self.api_key = os.getenv("FX_API_KEY", "")
        self.default_pair = os.getenv("DEFAULT_PAIR", "EUR/USD")
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./fx_price_intelligence.db")
        self.csv_data_dir = os.getenv("CSV_DATA_DIR", str(BASE_DIR / "data" / "sample"))
        self.supported_pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "USD/ZAR", "EUR/ZAR"]


settings = Settings()
