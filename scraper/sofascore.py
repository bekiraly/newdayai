import requests
from datetime import datetime

BASE = "https://api.sofascore.com/api/v1"


def find_team(team: str):
    """
    Takım arama. Sofascore search/all endpoint ile ID ve isim bulur.
    """
    url = f"{BASE}/search/all?q={team}"
    r = requests.get(url).json()

    for item in r.get("topTeams", []):
        return item["id"], item["name"]

    for item in r.get("teams", []):
        return item["id"], item["name"]

    return None, None


def get_last5(team: str):
    """
    Bir takımın Sofascore'daki son 5 maçını ve G/B/M formunu döndürür.
    """
    team_id, team_name = find_team(team)
    if not team_id:
        return None

    url = f"{BASE}/team/{team_id}/events/last/0"
    r = requests.get(url).json()
    events = r.get("events", [])[:5]

    form_letters = []
    matches = []

    for m in events:
        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]
        score = f"{m['homeScore']['current']} - {m['awayScore']['current']}"

        winner_code = m.get("winnerCode", 0)  # 0=beraber,1=ev,2=dep

        if winner_code == 0:
            form_letters.append("B")
        else:
            # kullanıcının takımı evde mi, deplasmanda mı?
            if winner_code == 1 and home.lower() == team_name.lower():
                form_letters.append("G")
            elif winner_code == 2 and away.lower() == team_name.lower():
                form_letters.append("G")
            else:
                form_letters.append("M")

        matches.append({
            "home": home,
            "away": away,
            "score": score
        })

    logo_url = f"{BASE}/team/{team_id}/image"

    return {
        "team": team_name,
        "form": " ".join(form_letters),
        "matches": matches,
        "logoUrl": logo_url,
    }


def get_h2h(team1: str, team2: str):
    id1, _ = find_team(team1)
    id2, _ = find_team(team2)
    if not id1 or not id2:
        return None

    # Sofascore h2h endpoint (yaklaşık, gerekirse debug edilerek iyileştirilir)
    url = f"{BASE}/team/{id1}/h2h-standings/{id2}"
    r = requests.get(url).json()
    return r


def get_lineup(team: str):
    team_id, _ = find_team(team)
    if not team_id:
        return None

    # Son maç ID'sini bul
    url = f"{BASE}/team/{team_id}/events/last/0"
    r = requests.get(url).json()
    events = r.get("events", [])
    if not events:
        return None

    match_id = events[0]["id"]
    lineup_url = f"{BASE}/event/{match_id}/lineups"
    return requests.get(lineup_url).json()


def get_coach(team: str):
    team_id, _ = find_team(team)
    if not team_id:
        return None

    url = f"{BASE}/team/{team_id}"
    r = requests.get(url).json()
    # managers anahtarını dönen JSON'a göre uyarlamak gerekebilir
    return r.get("managers", r)


def get_players(team: str):
    team_id, _ = find_team(team)
    if not team_id:
        return None

    url = f"{BASE}/team/{team_id}/players"
    r = requests.get(url).json()
    return r


def get_stats(team: str):
    team_id, _ = find_team(team)
    if not team_id:
        return None

    url = f"{BASE}/team/{team_id}/statistics"
    r = requests.get(url).json()
    return r


def get_today_fixtures():
    """
    Bugünün fikstürü (tüm dünyadan). Sofascore scheduled-events endpoint.
    """
    today = datetime.utcnow().strftime("%Y-%m-%d")
    url = f"{BASE}/sport/football/scheduled-events/{today}"
    r = requests.get(url).json()
    events = r.get("events", [])
    out = []

    for e in events:
        out.append({
            "id": e["id"],
            "home": e["homeTeam"]["name"],
            "away": e["awayTeam"]["name"],
            "tournament": e["tournament"]["name"],
            "startTimestamp": e["startTimestamp"]
        })

    return out


def get_random_fixture_prediction():
    """
    Fikstürden rastgele maç seçer ve basit fake tahmin üretir.
    Ticker için kullanılacak.
    """
    import random

    fixtures = get_today_fixtures()
    if not fixtures:
        return None

    match = random.choice(fixtures)

    # Çok basit fake yüzdeler (ileride gerçek modele bağlanacak)
    home_prob = random.randint(35, 60)
    away_prob = random.randint(15, 45)
    draw_prob = max(0, 100 - home_prob - away_prob)

    return {
        "home": match["home"],
        "away": match["away"],
        "tournament": match["tournament"],
        "homeProb": home_prob,
        "awayProb": away_prob,
        "drawProb": draw_prob,
    }
