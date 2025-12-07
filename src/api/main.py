from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import router

app = FastAPI(
    title="NewDayAI - Match Prediction Engine",
    description="API-Football verileriyle maç analizi ve tahmin motoru",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router bağlama
app.include_router(router)

@app.get("/")
async def root():
    return {"status": "ok", "service": "NewDayAI Engine"}
