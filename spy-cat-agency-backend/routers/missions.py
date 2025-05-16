from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal
import models, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.MissionOut, status_code=status.HTTP_201_CREATED)
def create_mission(mission_data: schemas.MissionCreate, db: Session = Depends(get_db)):
    mission = models.Mission()
    db.add(mission)
    db.commit()
    db.refresh(mission)

    for target_data in mission_data.targets:
        target = models.Target(**target_data.dict(), mission_id=mission.id)
        db.add(target)

    db.commit()
    db.refresh(mission)
    return mission

@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(models.Mission).get(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if mission.cat_id is not None:
        raise HTTPException(status_code=400, detail="Cannot delete assigned mission")
    db.delete(mission)
    db.commit()

@router.put("/{mission_id}/assign_cat", status_code=status.HTTP_200_OK)
def assign_cat_to_mission(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
    mission = db.query(models.Mission).get(mission_id)
    cat = db.query(models.SpyCat).get(cat_id)
    if not mission or not cat:
        raise HTTPException(status_code=404, detail="Mission or cat not found")
    if mission.cat_id is not None:
        raise HTTPException(status_code=400, detail="Mission already assigned")
    mission.cat_id = cat_id
    db.commit()
    db.refresh(mission)
    return {"detail": "Cat assigned successfully"}

@router.put("/targets/{target_id}/notes")
def update_target_notes(target_id: int, notes: str, db: Session = Depends(get_db)):
    target = db.query(models.Target).get(target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    if target.completed or target.mission.completed:
        raise HTTPException(status_code=400, detail="Cannot update notes on completed target/mission")

    target.notes = notes
    db.commit()
    db.refresh(target)
    return target

@router.put("/targets/{target_id}/complete")
def complete_target(target_id: int, db: Session = Depends(get_db)):
    target = db.query(models.Target).get(target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    target.completed = True
    db.commit()
    db.refresh(target)

    # Якщо всі цілі виконані — завершити місію
    mission = target.mission
    if all(t.completed for t in mission.targets):
        mission.completed = True
        db.commit()
        db.refresh(mission)

    return target

@router.get("/", response_model=List[schemas.MissionOut])
def list_missions(db: Session = Depends(get_db)):
    return db.query(models.Mission).all()

@router.get("/{mission_id}", response_model=schemas.MissionOut)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(models.Mission).get(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission
