from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal
import models, schemas

router = APIRouter(prefix="/scores", tags=["Scores"])


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create or Update Score ✅
@router.post("", response_model=schemas.ScoreOut, status_code=status.HTTP_201_CREATED)
def add_or_update_score(score: schemas.ScoreCreate, db: Session = Depends(get_db)):
    # Foreign key validation
    if not db.query(models.Player).filter(models.Player.player_id == score.player_id).first():
        raise HTTPException(status_code=404, detail="Player not found")
    if not db.query(models.Judge).filter(models.Judge.judge_id == score.judge_id).first():
        raise HTTPException(status_code=404, detail="Judge not found")
    if not db.query(models.Event).filter(models.Event.event_id == score.event_id).first():
        raise HTTPException(status_code=404, detail="Event not found")

    # If score exists, update
    existing = (
        db.query(models.Score)
        .filter(
            models.Score.event_id == score.event_id,
            models.Score.player_id == score.player_id,
            models.Score.judge_id == score.judge_id,
        )
        .first()
    )
    if existing:
        existing.score = score.score
        db.commit()
        db.refresh(existing)
        return existing

    # Else, create
    new_score = models.Score(**score.dict())
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score


# Get All Scores ✅
@router.get("", response_model=list[schemas.ScoreOut])
def get_all_scores(db: Session = Depends(get_db)):
    return db.query(models.Score).all()


# Get Leaderboard by Event ✅
@router.get("/leaderboard/{event_id}")
def get_leaderboard(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    results = (
        db.query(
            models.Score.player_id,
            models.Player.name.label("player_name"),
            func.round(func.avg(models.Score.score), 2).label("avg_score"),
        )
        .join(models.Player, models.Player.player_id == models.Score.player_id)
        .filter(models.Score.event_id == event_id)
        .group_by(models.Score.player_id, models.Player.name)
        .order_by(func.avg(models.Score.score).desc())
        .all()
    )

    return [
        {"player_id": r.player_id, "player_name": r.player_name, "avg_score": float(r.avg_score)}
        for r in results
    ]
