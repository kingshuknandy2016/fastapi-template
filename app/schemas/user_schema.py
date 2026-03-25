from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str
    email: str
    role: str


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    email: str | None = None
    role: str | None = None


class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True
