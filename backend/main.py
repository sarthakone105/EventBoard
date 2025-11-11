from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes_players import router as players_router
from routes_judges import router as judges_router
from routes_events import router as events_router
from routes_scores import router as scores_router
from routes_stats import router as stats_router  # ✅ new router
from routes_admin import router as admin_router
from database import engine  # used for /db-check route

# -------------------------------------------------
# Initialize FastAPI App
# -------------------------------------------------
app = FastAPI(
    title="EventBoard API",
    version="1.0.0",
    description="A live tournament scorekeeping API with player, judge, event, and score management.",
)

# -------------------------------------------------
# Enable CORS (for your frontend)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ allow frontend (localhost or Render)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Health check route
# -------------------------------------------------
@app.get("/status")
def status():
    return {"message": "✅ EventBoard backend is running"}

# -------------------------------------------------
# Database connectivity check
# -------------------------------------------------
@app.get("/db-check")
def check_db():
    """
    Verifies that the database connection is active.
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
app.include_router(stats_router)  # ✅ new stats routes (leaderboard, summaries, etc.)
app.include_router(admin_router)
