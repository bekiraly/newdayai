import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"


class APIFootball:
    def __init__(self):
        self.headers = {
            "x-apisports-key": API_KEY
        }

    def get(self, endpoint, params=None):
        url = f"{BASE_URL}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} → {response.text}")

        return response.json()

    def get_team_id(self, team_name, country="Turkey"):
        data = self.get("teams", {"search": team_name})

        for item in data["response"]:
            if country.lower() in item["team"]["country"].lower():
                return item["team"]["id"]

        # fallback — ülkeyi tutturamazsa ilkini döner
        return data["response"][0]["team"]["id"]

    def get_last_matches(self, team_id, limit=5):
        return self.get("fixtures", {
            "team": team_id,
            "last": limit
        })

    def get_head_to_head(self, home_id, away_id):
        return self.get("fixtures/headtohead", {
            "h2h": f"{home_id}-{away_id}"
        })

    def get_standings(self, league_id, season):
        return self.get("standings", {
            "league": league_id,
            "season": season
        })

    def get_odds(self, fixture_id):
        return self.get("odds", {
            "fixture": fixture_id
        })
