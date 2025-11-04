# backend/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# -------------------------------------------------
# PLAYER SCHEMAS
# -------------------------------------------------
class PlayerBase(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    force: Optional[str] = None
    rank: Optional[str] = None


class PlayerCreate(PlayerBase):
    player_id: int   # You manually assign chest number (unique ID for player)


class PlayerUpdate(PlayerBase):
    pass  # Allows partial updates (PATCH)


class PlayerOut(PlayerBase):
    player_id: int

    class Config:
        orm_mode = True
        from_attributes = True  # works with SQLAlchemy ORM objects


# -------------------------------------------------
# JUDGE SCHEMAS
# -------------------------------------------------
class JudgeBase(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    force: Optional[str] = None
    rank: Optional[str] = None


class JudgeCreate(JudgeBase):
    pass


class JudgeUpdate(JudgeBase):
    pass


class JudgeOut(JudgeBase):
    judge_id: int

    class Config:
        orm_mode = True
        from_attributes = True


# -------------------------------------------------
# EVENT SCHEMAS
# -------------------------------------------------
class EventBase(BaseModel):
    name: Optional[str] = None
    round_name: Optional[str] = None
    event_date: Optional[datetime] = None


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventOut(EventBase):
    event_id: int

    class Config:
        orm_mode = True
        from_attributes = True


# -------------------------------------------------
# SCORE SCHEMAS
# -------------------------------------------------
class ScoreBase(BaseModel):
    event_id: int
    player_id: int
    judge_id: int
    score: float


class ScoreCreate(ScoreBase):
    score_date: Optional[datetime] = datetime.utcnow()


class ScoreUpdate(BaseModel):
    score: Optional[float] = None


class ScoreOut(ScoreBase):
    score_id: int
    score_date: datetime

    class Config:
        orm_mode = True
        from_attributes = True


# -------------------------------------------------
# NESTED OUTPUT (optional, for leaderboards)
# -------------------------------------------------
class ScoreDetailed(ScoreOut):
    player: Optional[PlayerOut] = None
    judge: Optional[JudgeOut] = None
    event: Optional[EventOut] = None
