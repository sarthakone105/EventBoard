# backend/routes_players.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import SessionLocal
from backend.models import Player
from backend.schemas import PlayerCreate, PlayerUpdate, PlayerOut

router = APIRouter(prefix="/players", tags=["Players"])


# Dependency - create a new DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------
# Create Player
# ------------------------------
@router.post("", response_model=PlayerOut, status_code=status.HTTP_201_CREATED)
def create_player(payload: PlayerCreate, db: Session = Depends(get_db)):
    existing = db.query(Player).filter(Player.player_id == payload.player_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Player ID already exists")

    player = Player(
        player_id=payload.player_id,
        name=payload.name,
        age=payload.age,
        force=payload.force,
        rank=payload.rank,
    )
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


# ------------------------------
# Get All Players
# ------------------------------
@router.get("", response_model=List[PlayerOut])
def list_players(db: Session = Depends(get_db)):
    return db.query(Player).all()


# ------------------------------
# Get Single Player
# ------------------------------
@router.get("/{player_id}", response_model=PlayerOut)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


# ------------------------------
# Update Player
# ------------------------------
@router.patch("/{player_id}", response_model=PlayerOut)
def update_player(player_id: int, payload: PlayerUpdate, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(player, key, value)

    db.commit()
    db.refresh(player)
    return player


# ------------------------------
# Delete Player
# ------------------------------
@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    db.delete(player)
    db.commit()
    return None
