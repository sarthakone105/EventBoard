# backend/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# -------------------------------------------------
# PLAYER SCHEMAS
# -------------------------------------------------
class PlayerBase(BaseModel):
    name: str
    age: int
    force: str
    rank: str


class PlayerCreate(PlayerBase):
    player_id: int = Field(..., description="Chest number (unique ID for player)")


class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    force: Optional[str] = None
    rank: Optional[str] = None


class PlayerOut(PlayerBase):
    player_id: int

    class Config:
        orm_mode = True
        from_attributes = True


# -------------------------------------------------
# JUDGE SCHEMAS
# -------------------------------------------------
class JudgeBase(BaseModel):
    name: str
    age: int
    force: str
    rank: str


class JudgeCreate(JudgeBase):
    pass


class JudgeUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    force: Optional[str] = None
    rank: Optional[str] = None


class JudgeOut(JudgeBase):
    judge_id: int

    class Config:
        orm_mode = True
        from_attributes = True


# -------------------------------------------------
# EVENT SCHEMAS
# -------------------------------------------------
class EventBase(BaseModel):
    name: str
    round_name: Optional[str] = None
    event_date: Optional[datetime] = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: Optional[str] = None
    round_name: Optional[str] = None
    event_date: Optional[datetime] = None


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
    score: float = Field(..., ge=0, le=10, description="Score must be between 0 and 10")


class ScoreCreate(ScoreBase):
    score_date: datetime = Field(default_factory=datetime.utcnow)


class ScoreUpdate(BaseModel):
    score: Optional[float] = Field(None, ge=0, le=10, description="Updated score between 0 and 10")


class ScoreOut(ScoreBase):
    score_id: int
    score_date: datetime

    class Config:
        orm_mode = True
        from_attributes = True


# -------------------------------------------------
# NESTED OUTPUT (for leaderboards or detailed score view)
# -------------------------------------------------
class ScoreDetailed(ScoreOut):
    player: Optional[PlayerOut] = None
    judge: Optional[JudgeOut] = None
    event: Optional[EventOut] = None
