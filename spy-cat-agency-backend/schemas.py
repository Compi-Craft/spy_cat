from pydantic import BaseModel
from typing import List, Optional

class SpyCatBase(BaseModel):
    name: str
    years_experience: int
    breed: str
    salary: float

class SpyCatCreate(SpyCatBase):
    pass

class SpyCatUpdate(BaseModel):
    salary: float

class SpyCatOut(SpyCatBase):
    id: int
    class Config:
        orm_mode = True

class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = ""
    
class TargetCreate(TargetBase):
    pass

class TargetOut(TargetBase):
    id: int
    completed: bool
    model_config = {
        "orm_mode": True,
        "from_attributes": True
    }


class MissionCreate(BaseModel):
    targets: List[TargetCreate]

class MissionOut(BaseModel):
    id: int
    completed: bool
    cat_id: Optional[int]
    targets: List[TargetOut]

    class Config:
        orm_mode = True
