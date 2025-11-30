from fastapi import FastAPI
from scraper.sofascore import (
    get_last5, get_h2h, get_lineup,
    get_coach, get_players, get_stats
)

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "service": "NewDayAI Sofascore API"}


@app.get("/form/{team}")
def form(team: str):
    data = get_last5(team)
    if not data:
        return {"error": "Takım bulunamadı"}
    return data


@app.get("/last5/{team}")
def last5(team: str):
    return get_last5(team)


@app.get("/h2h/{team1}/{team2}")
def h2h(team1: str, team2: str):
    return get_h2h(team1, team2)


@app.get("/lineup/{team}")
def lineup(team: str):
    return get_lineup(team)


@app.get("/coach/{team}")
def coach(team: str):
    return get_coach(team)


@app.get("/players/{team}")
def players(team: str):
    return get_players(team)


@app.get("/stats/{team}")
def stats(team: str):
    return get_stats(team)
