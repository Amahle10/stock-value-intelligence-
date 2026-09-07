from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup

ALLOWED_PUBLIC_SITES = [
    "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html",
]


def fetch_reference_data(url: str = ALLOWED_PUBLIC_SITES[0], timeout: int = 15) -> List[Dict[str, Any]]:
    if url not in ALLOWED_PUBLIC_SITES:
        raise ValueError("The requested scraper target is not an allowed public reference source.")

    response = requests.get(url, timeout=timeout, headers={"User-Agent": "fx-price-intelligence/1.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    rows: List[Dict[str, Any]] = []
    for item in soup.select("td, th"):
        text = " ".join(item.get_text(" ", strip=True).split())
        if text:
            rows.append({
                "source": url,
                "retrieval_timestamp": datetime.now(timezone.utc).isoformat(),
                "raw_value": text,
                "normalized_value": text.lower(),
            })
    return rows[:20]
