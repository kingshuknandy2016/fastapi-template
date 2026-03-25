from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import container

router = APIRouter()


def get_user_service():
    if not container.user_service:
        raise RuntimeError("Service not initialized")
    return container.user_service


@router.get("/users/{user_id}")
def get_user(user_id: int, user_service=Depends(get_user_service)):
    try:
        return user_service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
