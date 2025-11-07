from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal
import models

router = APIRouter(prefix="/stats", tags=["Stats"])


# -------------------------------------------------
# Database session dependency
# -------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------
# 1️⃣ Overall Leaderboard: Total score per player
# -------------------------------------------------
@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Player.name.label("player_name"),
            func.sum(models.Score.score).label("total_score")
        )
        .join(models.Score, models.Player.player_id == models.Score.player_id)
        .group_by(models.Player.player_id)
        .order_by(func.sum(models.Score.score).desc())
        .all()
    )

    return [
        {"rank": i + 1, "player": r.player_name, "total_score": float(r.total_score)}
        for i, r in enumerate(results)
    ]


# -------------------------------------------------
# 2️⃣ Event Averages: Average score per event
# -------------------------------------------------
@router.get("/event-averages")
def get_event_averages(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Event.name.label("event_name"),
            func.avg(models.Score.score).label("avg_score")
        )
        .join(models.Score, models.Event.event_id == models.Score.event_id)
        .group_by(models.Event.event_id)
        .order_by(models.Event.event_id)
        .all()
    )

    return [
        {"event": r.event_name, "average_score": round(float(r.avg_score), 2)}
        for r in results
    ]


# -------------------------------------------------
# 3️⃣ Summary Stats: Totals for dashboard metrics
# -------------------------------------------------
@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    return {
        "total_players": db.query(func.count(models.Player.player_id)).scalar(),
        "total_events": db.query(func.count(models.Event.event_id)).scalar(),
        "total_judges": db.query(func.count(models.Judge.judge_id)).scalar(),
        "total_scores": db.query(func.count(models.Score.score_id)).scalar(),
    }


# -------------------------------------------------
# Helper function: build leaderboard for one or all events
# -------------------------------------------------
def _fetch_leaderboard_data(db: Session, event_id: int | None = None):
    query = (
        db.query(
            models.Event.event_id,
            models.Event.name.label("event_name"),
            models.Player.name.label("player_name"),
            models.Score.score
        )
        .join(models.Score, models.Event.event_id == models.Score.event_id)
        .join(models.Player, models.Score.player_id == models.Player.player_id)
    )

    if event_id:
        query = query.filter(models.Event.event_id == event_id)

    return query.order_by(models.Event.event_id, models.Score.score.desc()).all()


# -------------------------------------------------
# 4️⃣ Leaderboard by Event (All Events)
# -------------------------------------------------
@router.get("/leaderboard-by-event")
def get_leaderboard_by_event(db: Session = Depends(get_db)):
    results = _fetch_leaderboard_data(db)

    if not results:
        raise HTTPException(status_code=404, detail="No scores found.")

    leaderboard_by_event = {}
    for row in results:
        leaderboard_by_event.setdefault(row.event_name, []).append({
            "player": row.player_name,
            "score": float(row.score)
        })

    return [
        {
            "event": event,
            "leaderboard": [
                {"rank": i + 1, **player}
                for i, player in enumerate(sorted(players, key=lambda x: x["score"], reverse=True))
            ]
        }
        for event, players in leaderboard_by_event.items()
    ]


# -------------------------------------------------
# 5️⃣ Leaderboard for a Specific Event
# -------------------------------------------------
@router.get("/leaderboard-by-event/{event_id}")
def get_leaderboard_for_event(event_id: int, db: Session = Depends(get_db)):
    results = _fetch_leaderboard_data(db, event_id=event_id)

    if not results:
        raise HTTPException(status_code=404, detail="No scores found for this event.")

    event_name = results[0].event_name
    leaderboard = [
        {"rank": i + 1, "player": r.player_name, "score": float(r.score)}
        for i, r in enumerate(results)
    ]

    return {"event": event_name, "leaderboard": leaderboard}



