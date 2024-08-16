from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CollectionBase(BaseModel):
    game_name: str
    game_status: str
    expires_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class CollectionCreate(CollectionBase):
    pass


class CollectionUpdate(CollectionBase):
    pass


class CollectionInDBBase(CollectionBase):
    game_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CollectionResponse(CollectionInDBBase):
    pass
