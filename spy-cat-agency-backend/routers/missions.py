from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
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
    # Валідація кількості цілей
    if not (1 <= len(mission_data.targets) <= 3):
        raise HTTPException(status_code=400, detail="Mission must have 1 to 3 targets.")

    mission = models.Mission(completed=False)
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
        raise HTTPException(status_code=404, detail="Mission or Cat not found")

    if mission.cat_id is not None:
        raise HTTPException(status_code=400, detail="Mission already assigned to a cat")

    active = db.query(models.Mission).filter_by(cat_id=cat_id, completed=False).first()
    if active:
        raise HTTPException(status_code=400, detail="Cat already has an active mission")

    mission.cat_id = cat_id
    db.commit()
    db.refresh(mission)
    return {"detail": "Cat assigned successfully", "mission_id": mission.id}

@router.put("/targets/{target_id}/notes")
def update_target_notes(target_id: int, notes: str, db: Session = Depends(get_db)):
    target = db.query(models.Target).get(target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    if target.completed or target.mission.completed:
        raise HTTPException(status_code=400, detail="Cannot update notes on completed target or mission")

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

    mission = target.mission
    if all(t.completed for t in mission.targets):
        mission.completed = True
        db.commit()
        db.refresh(mission)

    return schemas.TargetOut.from_orm(target)

@router.get("/", response_model=List[schemas.MissionOut])
def list_missions(db: Session = Depends(get_db)):
    return db.query(models.Mission).all()

@router.get("/{mission_id}", response_model=schemas.MissionOut)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(models.Mission).get(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission