from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime

from app.api.collection.crud import (
    get_collection_by_game_id,
    create_game,
    update_game_status,
    update_game_expiry,
    delete_game,
)
from app.api.collection.schema import CollectionCreate, CollectionResponse
from app.db.session import get_db, get_current_user
from app.api.user.models import User

router = APIRouter()


@router.get("/collections/{game_id}",
            response_model=Optional[CollectionResponse])
async def get_collection_route(game_id: int,
                               db: AsyncSession = Depends(get_db)):
    collection = await get_collection_by_game_id(db, game_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.post("/add-game", response_model=CollectionResponse)
async def add_game_route(
    game_name: str = Form(...),
    active_game: bool = Form(False),
    expires_at: Optional[datetime] = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    game_status = 'active' if active_game else 'inactive'
    game_data = CollectionCreate(game_name=game_name,
                                 game_status=game_status,
                                 expires_at=expires_at)
    new_game = await create_game(db=db,
                                 game=game_data,
                                 current_user=current_user)
    return new_game


@router.post("/activate-game/{game_id}",
             response_model=Optional[CollectionResponse])
async def activate_game_route(
    game_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    collection = await update_game_status(db=db,
                                          game_id=game_id,
                                          current_user=current_user)
    if not collection:
        raise HTTPException(status_code=404, detail="Game not found")
    return collection


@router.post("/update-expiry/{game_id}",
             response_model=Optional[CollectionResponse])
async def update_game_expiry_route(
    game_id: int,
    new_expiry: datetime,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    collection = await update_game_expiry(db=db,
                                          game_id=game_id,
                                          new_expiry=new_expiry,
                                          current_user=current_user)
    if not collection:
        raise HTTPException(status_code=404, detail="Game not found")
    return collection


@router.delete("/delete-game/{game_id}",
               response_model=Optional[CollectionResponse])
async def delete_game_route(
    game_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    collection = await delete_game(db=db,
                                   game_id=game_id,
                                   current_user=current_user)
    if not collection:
        raise HTTPException(status_code=404, detail="Game not found")
    return collection
