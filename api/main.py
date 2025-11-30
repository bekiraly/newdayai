from fastapi import FastAPI
from scraper.api_football import get_last_five_matches

app = FastAPI()


@app.get("/form/{team}")
def form(team: str):
    data = get_last_five_matches(team)

    if not data:
        return {"error": "Takım bulunamadı"}

    return {
        "team": data["team_name"],
        "form": data["form_string"],
        "matches": data["matches"],
        "logo": data["logo"],
    }


@app.get("/form/{team}")
def form(team: str):
    team_id = get_team_id_by_name(team)

    if not team_id:
        return {"error": "Takım bulunamadı"}

    form_data = get_form_sequence(team_id)

    return {
        "team": team,
        "form": form_data
    }

