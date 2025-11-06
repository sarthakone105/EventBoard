from fastapi import FastAPI
from routes_players import router as players_router
from routes_judges import router as judges_router
from routes_events import router as events_router
from routes_scores import router as scores_router
from database import engine  # ✅ optional, used for /db-check route

app = FastAPI(
    title="EventBoard API",
    version="1.0.0",
    description="A live tournament scorekeeping API with player, judge, event, and score management."
)

# -------------------------------------------------
# Simple health check route
# -------------------------------------------------
@app.get("/status")
def status():
    return {"message": "✅ EventBoard backend is running"}


# -------------------------------------------------
# Optional database connectivity check route
# -------------------------------------------------
@app.get("/db-check")
def check_db():
    """
    Simple endpoint to verify DB connection.
    Works locally and on Render.
    """
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return {"status": "✅ Database connection successful"}
    except Exception as e:
        return {"status": "❌ Database connection failed", "error": str(e)}


# -------------------------------------------------
# Register routers
# -------------------------------------------------
app.include_router(players_router)
app.include_router(judges_router)
app.include_router(events_router)
app.include_router(scores_router)
