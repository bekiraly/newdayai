from ..data_providers.api_football import APIFootball

api = APIFootball()

def predict_match(league, season, home, away):

    home_id = api.get_team_id(home)
    away_id = api.get_team_id(away)

    last_home = api.get_last_matches(home_id)
    last_away = api.get_last_matches(away_id)

    h2h = api.get_head_to_head(home_id, away_id)

    return {
        "home_id": home_id,
        "away_id": away_id,
        "last_home_matches": last_home,
        "last_away_matches": last_away,
        "head_to_head": h2h
    }

def predict_match(league, season, home, away):
    # 1) Veriyi çek
    # 2) Normalize et
    # 3) Feature hesapla
    # 4) Tahmin üret
    # 5) JSON döndür

    return {
        "status": "ok",
        "match": f"{home} vs {away}",
        "prediction": "engine v1 skeleton ready"
    }
