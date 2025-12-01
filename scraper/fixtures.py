import requests
import random
import os
from datetime import datetime

SPORTMONKS_KEY = os.getenv("SPORTMONKS_KEY")

BASE = "https://api.sportmonks.com/v3/football"


def get_today_fixtures():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    url = (
        f"{BASE}/fixtures/date/{today}"
        f"?api_token={SPORTMONKS_KEY}"
        "&include=participants;league"
    )

    res = requests.get(url).json()

    if "data" not in res:
        return []

    fixtures = []
    for f in res["data"]:
        try:
            home = f["participants"][0]["name"]
            away = f["participants"][1]["name"]
            tournament = f["league"]["name"]

            fixtures.append({
                "home": home,
                "away": away,
                "tournament": tournament
            })
        except:
            pass

    return fixtures


def get_random_fixture_prediction():
    matches = get_today_fixtures()
    if not matches:
        return None

    match = random.choice(matches)

    # Basit fake tahmin
    home_p = random.randint(35, 60)
    away_p = random.randint(20, 40)
    draw_p = max(0, 100 - home_p - away_p)

    return {
        "home": match["home"],
        "away": match["away"],
        "tournament": match["tournament"],
        "homeProb": home_p,
        "awayProb": away_p,
        "drawProb": draw_p,
    }
