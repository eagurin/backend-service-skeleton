from pydantic import BaseModel, UUID4

class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str
    balance: str
