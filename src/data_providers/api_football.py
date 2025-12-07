import os
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"


class APIFootballClient:
    """API-Football üzerinden veri çeken basit client."""

    def __init__(self) -> None:
        if not API_KEY:
            raise RuntimeError(
                "API_FOOTBALL_KEY ortam değişkeni tanımlı değil. Railway/ENV kontrol et."
            )
        self.headers = {
            "x-apisports-key": API_KEY
        }

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{BASE_URL}/{endpoint}"
        resp = requests.get(url, headers=self.headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if "response" not in data:
            raise RuntimeError(f"API beklenmeyen cevap döndürdü: {data}")
        return data

    # -------- Takım & Maç Fonksiyonları -------- #

    def search_team(self, name: str, country: Optional[str] = None) -> Optional[Dict[str, Any]]:
        data = self._get("teams", {"search": name})
        teams = data.get("response", [])
        if not teams:
            return None

        if country:
            for item in teams:
                t = item.get("team", {})
                if t.get("country", "").lower() == country.lower():
                    return item

        return teams[0]

    def get_team_id(self, name: str, country: Optional[str] = None) -> int:
        team = self.search_team(name, country)
        if not team:
            raise ValueError(f"Takım bulunamadı: {name}")
        return int(team["team"]["id"])

    def get_last_fixtures(self, team_id: int, last: int = 5) -> List[Dict[str, Any]]:
        data = self._get("fixtures", {"team": team_id, "last": last})
        return data.get("response", [])

    def get_head_to_head(self, home_id: int, away_id: int, last: int = 5) -> List[Dict[str, Any]]:
        data = self._get("fixtures/headtohead", {"h2h": f"{home_id}-{away_id}", "last": last})
        return data.get("response", [])
