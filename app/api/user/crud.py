from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.api.user.models import User
from app.api.user.schema import UserCreate
from typing import List
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_email(db: AsyncSession,
                            email: str) -> User:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_user(db: AsyncSession, user_id: int) -> User:
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def get_all_users(db: AsyncSession,
                        skip: int = 0,
                        limit: int = 10) -> List[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def change_user_email(
    db: AsyncSession,
    user_id: int,
    new_email: str,
    current_user: User
) -> User:
    user = await get_user(db, user_id)
    if not user:
        return None

    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, 
                            detail="Not authorized to change email")

    user.email = new_email
    await db.commit()
    await db.refresh(user)
    return user


async def change_user_password(
    db: AsyncSession,
    user_id: int,
    new_password: str,
    current_user: User
) -> User:
    user = await get_user(db, user_id)
    if not user:
        return None

    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, 
                            detail="Not authorized to change password")

    hashed_password = pwd_context.hash(new_password)
    user.password = hashed_password
    await db.commit()
    await db.refresh(user)
    return user


def verify_password(plain_password: str, 
                    hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(db: AsyncSession,
                            email: str,
                            password: str) -> User:
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


async def top_account(db: AsyncSession,
                      user_id: int,
                      amount: int) -> User:
    user = await get_user(db, user_id)
    if not user:
        return None
    try:
        if amount > 0 and type(amount) is int:
            user.balance += amount
            await db.commit()
            await db.refresh(user)
            return user
    except Exception as e:
        return f'An error has occured: {e}'
