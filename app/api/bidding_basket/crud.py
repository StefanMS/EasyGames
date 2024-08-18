from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.api.bidding_basket.models import BiddingBasket
from app.api.collection.models import Collection
from app.api.user.models import User
from fastapi import HTTPException


async def create_bid(db: AsyncSession,
                     game_id: int,
                     current_user: User) -> BiddingBasket:

    if int(current_user.balance) > 0:
        current_user.balance = int(current_user.balance) - 1

        new_bid = BiddingBasket(
            game_id=game_id,
            player_id=current_user.id
        )
        db.add(new_bid)
        await db.commit()
        await db.refresh(new_bid)
        return new_bid
    else:
        raise HTTPException(status_code=403,
                            detail="Not authorized to create bids. \
                                    Insufficient funds")


async def get_all_bidding_baskets(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10) -> List[BiddingBasket]:
    result = await db.execute(select(BiddingBasket).offset(skip).limit(limit))
    return result.scalars().all()


async def get_bidding_basket_by_id(db: AsyncSession,
                                   bid_id: int) -> Optional[BiddingBasket]:
    result = await db.execute(select(BiddingBasket).filter(
                                    BiddingBasket.id == bid_id))
    return result.scalars().first()


async def user_filtered_collection(
    db: AsyncSession,
    active_games: List[Collection],
    current_user: User,
    skip: int = 0,
    limit: int = 10
) -> List[Dict[str, Any]]:
    games_json = []

    paginated_games = active_games[skip:skip + limit]

    for game in paginated_games:
        bidding_basket_count = await db.execute(
            select(BiddingBasket).filter_by(game_id=game.game_id)
        )
        game_capacity = bidding_basket_count.scalars().count()

        enrolled_user = await db.execute(
            select(BiddingBasket).filter_by(game_id=game.game_id,
                                            player_id=current_user.id)
        )
        enrolled_user_bool = enrolled_user.scalars().first() is not None

        now_timestamp = datetime.now().timestamp()
        countdown = now_timestamp - game.expires_at.timestamp()

        game_as_dict = {
            'id': game.game_id,
            'name': game.game_name,
            'status': game.game_status,
            'enrolled_user': enrolled_user_bool,
            'capacity': game_capacity,
            'countdown': {
                'days': str(f'{int(countdown // (3600 * 24))}'),
                'hours': str(f'{int((countdown % (3600 * 24)) // 3600)}')
            }
        }
        games_json.append(game_as_dict)

    return games_json


async def update_bid(db: AsyncSession,
                     bid_id: int,
                     **kwargs) -> BiddingBasket:

    result = await db.execute(select(BiddingBasket).filter_by(
                                        BiddingBasket.id == bid_id))
    bid = result.scalars().first()

    if not bid:
        return None

    for key, value in kwargs.items():
        if hasattr(bid, key):
            setattr(bid, key, value)

    await db.commit()
    await db.refresh(bid)
    return bid


async def delete_bid(db: AsyncSession,
                     bid_id: int) -> bool:
    result = await db.execute(select(BiddingBasket).filter_by(
        BiddingBasket.id == bid_id))
    bid = result.scalars().first()

    if not bid:
        return False

    await db.delete(bid)
    await db.commit()
    return True
