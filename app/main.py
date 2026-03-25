from fastapi import FastAPI
from app.api.v1.controller import router
from app.core.dependencies import init_services

app = FastAPI(title="Layered FastAPI App")


@app.on_event("startup")
def startup_event():
    init_services()


app.include_router(router, prefix="/api/v1")
