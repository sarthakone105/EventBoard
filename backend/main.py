# backend/main.py
from fastapi import FastAPI
from backend.routes_players import router as players_router
from backend.routes_judges import router as judges_router



app = FastAPI(title="Tournament API", version="1.0.0")

@app.get("/status")
def status():
    return {"status": "ok", "message": "Tournament API running successfully"}

app.include_router(players_router)
app.include_router(judges_router)

