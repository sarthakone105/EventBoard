from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


# -------------------------------------------------------
# PLAYER MODEL
# -------------------------------------------------------
class Player(Base):
    __tablename__ = "Player"

    player_id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ Auto-increment enabled
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    force = Column(String(50))
    rank = Column(String(50))

    # Relationships
    scores = relationship(
        "Score",
        back_populates="player",
        cascade="all, delete-orphan"
    )


# -------------------------------------------------------
# JUDGE MODEL
# -------------------------------------------------------
class Judge(Base):
    __tablename__ = "Judge"

    judge_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    force = Column(String(50))
    rank = Column(String(50))

    # Relationships
    scores = relationship(
        "Score",
        back_populates="judge",
        cascade="all, delete-orphan"
    )


# -------------------------------------------------------
# EVENT MODEL
# -------------------------------------------------------
class Event(Base):
    __tablename__ = "Event"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    round_name = Column(String(50))
    event_date = Column(DateTime)

    # Relationships
    scores = relationship(
        "Score",
        back_populates="event",
        cascade="all, delete-orphan"
    )


# -------------------------------------------------------
# SCORE MODEL
# -------------------------------------------------------
class Score(Base):
    __tablename__ = "Score"

    score_id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("Event.event_id", ondelete="CASCADE"), nullable=False)
    player_id = Column(Integer, ForeignKey("Player.player_id", ondelete="CASCADE"), nullable=False)
    judge_id = Column(Integer, ForeignKey("Judge.judge_id", ondelete="CASCADE"), nullable=False)
    score = Column(Numeric(5, 2), nullable=False)
    score_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    player = relationship("Player", back_populates="scores")
    judge = relationship("Judge", back_populates="scores")
    event = relationship("Event", back_populates="scores")
