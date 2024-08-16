from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BiddingBasketSchema(BaseModel):
    game_id: int
    player_id: int

    class Config:
        orm_mode = True


class BiddingBasketCreate(BaseModel):
    pass


class BiddingBasketUpdate(BaseModel):
    pass


class BiddingBasketResponse(BaseModel):
    id: int
    game_id: int
    player_id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class BiddingBasket(BiddingBasketResponse):
    pass
