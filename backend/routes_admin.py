from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base

router = APIRouter(prefix="/admin", tags=["Admin"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/reset-db", status_code=status.HTTP_200_OK)
def reset_database(db: Session = Depends(get_db)):
    """
    ⚠️ ADMIN ONLY:
    Drops all existing tables and recreates them fresh.
    Use only for development/testing or seeding purposes.
    """
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        return {"message": "✅ Database reset complete!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
