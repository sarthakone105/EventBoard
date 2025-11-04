from fastapi import FastAPI
from backend.routes_players import router as players_router
from backend.routes_judges import router as judges_router
from backend.routes_events import router as events_router
from backend.routes_scores import router as scores_router

app = FastAPI(title="EventBoard API")

@app.get("/status")
def status():
    return {"message": "✅ EventBoard backend is running"}

# Register routers
app.include_router(players_router)
app.include_router(judges_router)
app.include_router(events_router)
app.include_router(scores_router)
