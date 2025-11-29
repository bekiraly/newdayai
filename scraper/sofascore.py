import requests

BASE_URL = "https://api.sofascore.com/api/v1"
headers = {"User-Agent": "Mozilla/5.0"}

SUPER_LIG_URL = f"{BASE_URL}/unique-tournament/36/season/52486/standings/total"


def get_team_id_by_name(team_name: str):
    """
    Süper Lig takımlarını lig tablosundan bulur.
    """
    resp = requests.get(SUPER_LIG_URL, headers=headers)

    if resp.status_code != 200:
        print("Standings fetch error:", resp.text)
        return None

    data = resp.json()

    teams = data["standings"][0]["rows"]

    for t in teams:
        name = t["team"]["name"]
        tid = t["team"]["id"]

        # örn: “konyaspor” == “Konyaspor”
        if team_name.lower() in name.lower():
            return tid

    return None
