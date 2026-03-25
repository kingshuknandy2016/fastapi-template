from fastapi import FastAPI

from app.api.v1.controller import router
from app.db.base import Base
from app.db.session import engine
from app.models import User  # noqa: F401

app = FastAPI(title="Layered FastAPI App")


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


app.include_router(router, prefix="/api/v1")
