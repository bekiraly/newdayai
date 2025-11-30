import os
import requests

API_BASE = "https://v3.football.api-sports.io"

API_KEY = os.getenv("API_FOOTBALL_KEY")
if not API_KEY:
    raise RuntimeError("API_FOOTBALL_KEY environment variable missing")

HEADERS = {
    "x-apisports-key": API_KEY
}

def get_super_lig_season():
    url = f"{API_BASE}/leagues?country=Turkey&name=Super%20Lig"
    res = requests.get(url, headers=HEADERS).json()

    try:
        league_id = res["response"][0]["league"]["id"]
        season = res["response"][0]["seasons"][-1]["year"]
        return league_id, season
    except:
        raise RuntimeError("Super Lig league/season not found")


def get_last_five_matches(team):
    # 1) Takımı genel arama ile bul
    url_team = f"{API_BASE}/teams?search={team}"
    res_team = requests.get(url_team, headers=HEADERS).json()

    if not res_team["response"]:
        return {"error": "Takım bulunamadı"}

    team_data = res_team["response"][0]["team"]
    team_id = team_data["id"]
    team_name = team_data["name"]
    logo = team_data["logo"]

    # 2) Süper Lig ID ve sezonlar
    league_id, guessed_season = get_super_lig_season()

    # önce yeni sezonu dene (guessed_season)
    seasons_to_try = [guessed_season, guessed_season - 1]

    matches_response = None
    selected_season = guessed_season

    for season in seasons_to_try:
        url_matches = f"{API_BASE}/fixtures?team={team_id}&season={season}&league={league_id}&last=5"
        try_res = requests.get(url_matches, headers=HEADERS).json()

        if try_res["response"]:
            matches_response = try_res
            selected_season = season
            break

    # Eğer hiçbir sezon veri vermediyse fallback
    if not matches_response:
        return {
            "team_name": team_name,
            "logo": logo,
            "form_string": "",
            "matches": [],
            "season_used": None
        }

    form_letters = []
    matches = []

    for m in matches_response["response"]:
        home = m["teams"]["home"]
        away = m["teams"]["away"]
        score = m["goals"]

        # Kazanan?
        if home["winner"] is True:
            winner = home["name"]
        elif away["winner"] is True:
            winner = away["name"]
        else:
            winner = None

        # Form harfi
        if winner is None:
            form_letters.append("B")
        elif winner.lower() == team_name.lower():
            form_letters.append("G")
        else:
            form_letters.append("M")

        matches.append({
            "home": home["name"],
            "away": away["name"],
            "score": f"{score['home']} - {score['away']}"
        })

    return {
        "team_name": team_name,
        "logo": logo,
        "form_string": " ".join(form_letters),
        "matches": matches,
        "season_used": selected_season
    }
