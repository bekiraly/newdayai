from fastapi import FastAPI
from scraper.api_football import get_last_five_matches

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "service": "newdayai api running"}

@app.get("/form/{team}")
def form(team: str):
    data = get_last_five_matches(team)

    if "error" in data:
        return {"error": "Takım bulunamadı"}

    return data

from scraper.api_football import get_super_lig_season

@app.get("/ligtest")
def ligtest():
    return get_super_lig_season()
