from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import schemas, models
from utils.catapi import validate_breed

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.SpyCatOut, status_code=status.HTTP_201_CREATED)
async def create_spy_cat(cat: schemas.SpyCatCreate, db: Session = Depends(get_db)):
    if not await validate_breed(cat.breed):
        raise HTTPException(status_code=400, detail="Invalid breed name.")

    db_cat = models.SpyCat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@router.get("/", response_model=List[schemas.SpyCatOut])
def list_spy_cats(db: Session = Depends(get_db)):
    return db.query(models.SpyCat).all()

@router.get("/{cat_id}", response_model=schemas.SpyCatOut)
def get_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(models.SpyCat).get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat

@router.put("/{cat_id}", response_model=schemas.SpyCatOut)
def update_spy_cat_salary(cat_id: int, update: schemas.SpyCatUpdate, db: Session = Depends(get_db)):
    cat = db.query(models.SpyCat).get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    cat.salary = update.salary
    db.commit()
    db.refresh(cat)
    return cat

@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(models.SpyCat).get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    db.delete(cat)
    db.commit()
