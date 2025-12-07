import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

class APIFootball:

    def get_team_id(self, name):
        url = f"{BASE_URL}/teams?search={name}"
        res = requests.get(url, headers=HEADERS)
        data = res.json()

        if data["results"] == 0:
            return None

        return data["response"][0]["team"]["id"]

    def get_last_matches(self, team_id, last=5):
        url = f"{BASE_URL}/fixtures?team={team_id}&last={last}"
        res = requests.get(url, headers=HEADERS)
        return res.json()

    def get_head_to_head(self, team1, team2):
        url = f"{BASE_URL}/fixtures/headtohead?h2h={team1}-{team2}"
        res = requests.get(url, headers=HEADERS)
        return res.json()
