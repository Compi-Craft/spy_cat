from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class SpyCat(Base):
    __tablename__ = "spy_cats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    years_experience = Column(Integer)
    breed = Column(String, nullable=False)
    salary = Column(Float)
    missions = relationship("Mission", back_populates="cat")

class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True, index=True)
    completed = Column(Boolean, default=False)
    cat_id = Column(Integer, ForeignKey("spy_cats.id"), nullable=True)

    cat = relationship("SpyCat", back_populates="missions")
    targets = relationship("Target", back_populates="mission")

class Target(Base):
    __tablename__ = "targets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    country = Column(String)
    notes = Column(String)
    completed = Column(Boolean, default=False)

    mission_id = Column(Integer, ForeignKey("missions.id"))
    mission = relationship("Mission", back_populates="targets")
