from fastapi import FastAPI
from database import Base, engine
from routers import cats, missions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Spy Cat Agency")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # або ["*"] для всіх джерел
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(cats.router, prefix="/cats", tags=["Spy Cats"])
app.include_router(missions.router, prefix="/missions", tags=["Missions"])
