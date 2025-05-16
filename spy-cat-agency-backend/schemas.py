from pydantic import BaseModel, Field
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
    class Config:
        orm_mode = True

class MissionCreate(BaseModel):
    targets: List[TargetCreate]

class MissionOut(BaseModel):
    id: int
    completed: bool
    targets: List[TargetOut]
    cat_id: Optional[int] = None
    class Config:
        orm_mode = True
