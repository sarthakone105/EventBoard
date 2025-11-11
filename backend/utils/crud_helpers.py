# backend/utils/crud_helpers.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

# -------------------------------
# 🟢 CREATE
# -------------------------------
def create_object(db: Session, model, payload, label: str, id_field: str = None):
    """
    Generic create helper for SQLAlchemy models.
    Automatically supports models with auto-incrementing IDs.
    Optionally checks for existing record if `id_field` is explicitly provided.
    """
    try:
        if id_field and hasattr(payload, id_field):
            # Optional uniqueness check only if id_field exists in payload
            existing = db.query(model).filter(
                getattr(model, id_field) == getattr(payload, id_field)
            ).first()
            if existing:
                raise HTTPException(
                    status_code=400, detail=f"{label} with this {id_field} already exists"
                )

        obj = model(**payload.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create {label}: {str(e)}")


# -------------------------------
# 🟡 UPDATE
# -------------------------------
def update_object(db: Session, model, id_field: str, id_value: int, payload, label: str):
    """
    Generic update helper for SQLAlchemy models.
    """
    obj = db.query(model).filter(getattr(model, id_field) == id_value).first()
    if not obj:
        raise HTTPException(status_code=404, detail=f"{label} not found")

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


# -------------------------------
# 🔴 DELETE
# -------------------------------
def delete_object(db: Session, model, id_field: str, id_value: int, label: str):
    """
    Generic delete helper for SQLAlchemy models.
    """
    obj = db.query(model).filter(getattr(model, id_field) == id_value).first()
    if not obj:
        raise HTTPException(status_code=404, detail=f"{label} not found")

    db.delete(obj)
    db.commit()
    return {"message": f"✅ {label} {id_value} deleted successfully"}
