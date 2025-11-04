# backend/routes_judges.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import SessionLocal
from backend.models import Judge
from backend.schemas import JudgeCreate, JudgeUpdate, JudgeOut

router = APIRouter(prefix="/judges", tags=["Judges"])

# Dependency - get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------
# Create Judge
# ------------------------------
@router.post("", response_model=JudgeOut, status_code=status.HTTP_201_CREATED)
def create_judge(payload: JudgeCreate, db: Session = Depends(get_db)):
    judge = Judge(
        name=payload.name,
        age=payload.age,
        force=payload.force,
        rank=payload.rank,
    )
    db.add(judge)
    db.commit()
    db.refresh(judge)
    return judge


# ------------------------------
# Get All Judges
# ------------------------------
@router.get("", response_model=List[JudgeOut])
def list_judges(db: Session = Depends(get_db)):
    return db.query(Judge).all()


# ------------------------------
# Get Single Judge
# ------------------------------
@router.get("/{judge_id}", response_model=JudgeOut)
def get_judge(judge_id: int, db: Session = Depends(get_db)):
    judge = db.query(Judge).filter(Judge.judge_id == judge_id).first()
    if not judge:
        raise HTTPException(status_code=404, detail="Judge not found")
    return judge


# ------------------------------
# Update Judge
# ------------------------------
@router.patch("/{judge_id}", response_model=JudgeOut)
def update_judge(judge_id: int, payload: JudgeUpdate, db: Session = Depends(get_db)):
    judge = db.query(Judge).filter(Judge.judge_id == judge_id).first()
    if not judge:
        raise HTTPException(status_code=404, detail="Judge not found")

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(judge, key, value)

    db.commit()
    db.refresh(judge)
    return judge


# ------------------------------
# Delete Judge
# ------------------------------
@router.delete("/{judge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_judge(judge_id: int, db: Session = Depends(get_db)):
    judge = db.query(Judge).filter(Judge.judge_id == judge_id).first()
    if not judge:
        raise HTTPException(status_code=404, detail="Judge not found")

    db.delete(judge)
    db.commit()
    return None
