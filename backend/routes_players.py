from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models import Player
from schemas import PlayerCreate, PlayerUpdate, PlayerOut
from utils.crud_helpers import create_object, update_object, delete_object

router = APIRouter(prefix="/players", tags=["Players"])


# Dependency - create new DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Player ✅
@router.post("", response_model=PlayerOut, status_code=status.HTTP_201_CREATED)
def create_player(payload: PlayerCreate, db: Session = Depends(get_db)):
    return create_object(db, Player, payload, label="Player", id_field="player_id")


# Get All Players ✅
@router.get("", response_model=List[PlayerOut])
def list_players(db: Session = Depends(get_db)):
    return db.query(Player).all()


# Get Single Player ✅
@router.get("/{player_id}", response_model=PlayerOut)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if not player:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Player not found")
    return player


# Update Player ✅
@router.patch("/{player_id}", response_model=PlayerOut)
def update_player(player_id: int, payload: PlayerUpdate, db: Session = Depends(get_db)):
    return update_object(db, Player, "player_id", player_id, payload, "Player")


# Delete Player ✅
@router.delete("/{player_id}", status_code=status.HTTP_200_OK)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    return delete_object(db, Player, "player_id", player_id, "Player")
