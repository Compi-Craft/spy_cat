from fastapi import FastAPI
from database import Base, engine
from routers import cats, missions

app = FastAPI(title="Spy Cat Agency")

Base.metadata.create_all(bind=engine)

app.include_router(cats.router, prefix="/cats", tags=["Spy Cats"])
app.include_router(missions.router, prefix="/missions", tags=["Missions"])
