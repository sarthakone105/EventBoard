from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models import Judge
from schemas import JudgeCreate, JudgeUpdate, JudgeOut
from utils.crud_helpers import create_object, update_object, delete_object

router = APIRouter(prefix="/judges", tags=["Judges"])


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Judge ✅
@router.post("", response_model=JudgeOut, status_code=status.HTTP_201_CREATED)
def create_judge(payload: JudgeCreate, db: Session = Depends(get_db)):
    return create_object(db, Judge, payload, label="Judge")


# Get All Judges ✅
@router.get("", response_model=List[JudgeOut])
def list_judges(db: Session = Depends(get_db)):
    return db.query(Judge).all()


# Get Single Judge ✅
@router.get("/{judge_id}", response_model=JudgeOut)
def get_judge(judge_id: int, db: Session = Depends(get_db)):
    judge = db.query(Judge).filter(Judge.judge_id == judge_id).first()
    if not judge:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Judge not found")
    return judge


# Update Judge ✅
@router.patch("/{judge_id}", response_model=JudgeOut)
def update_judge(judge_id: int, payload: JudgeUpdate, db: Session = Depends(get_db)):
    return update_object(db, Judge, "judge_id", judge_id, payload, "Judge")


# Delete Judge ✅
@router.delete("/{judge_id}", status_code=status.HTTP_200_OK)
def delete_judge(judge_id: int, db: Session = Depends(get_db)):
    return delete_object(db, Judge, "judge_id", judge_id, "Judge")
