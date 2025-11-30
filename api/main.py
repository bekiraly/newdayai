from fastapi import FastAPI
from scraper.api_football import (
    get_last_five_matches,
    get_super_lig_season,
    debug_team_search
)

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "service": "newdayai api running"}

@app.get("/form/{team}")
def form(team: str):
    data = get_last_five_matches(team)
    return data

@app.get("/ligtest")
def ligtest():
    return get_super_lig_season()

@app.get("/debug/{team}")
def debug(team: str):
    return debug_team_search(team)
