from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.api.user.crud import (
    authenticate_user,
    create_user,
    get_user_by_email,
    get_user,
    get_all_users,
    change_user_email,
    change_user_password,
    top_account
)
from app.api.user.schema import UserCreate, UserResponse
from app.api.user.models import User
from typing import Optional, List

from app.db.session import get_db, get_current_user

router = APIRouter()


@router.get("/users/{user_id}", response_model=Optional[UserResponse])
async def get_user_by_id_route(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a user by their ID.
    """
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(status_code=403,
                            detail="Not authorized to access this user")

    user = await get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/email/{email}", response_model=Optional[UserResponse])
async def get_user_by_email_route(
    email: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a user by their email.
    """

    user = await get_user_by_email(db=db, email=email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not current_user.is_superuser and current_user.id != user.id:
        raise HTTPException(status_code=403,
                            detail="Not authorized to access this user")
    return user


@router.get("/users/", response_model=List[UserResponse])
async def get_all_users_route(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a list of all users, with pagination.
    Only accessible by superusers.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403,
                            detail="Not authorized to access all users")

    users = await get_all_users(db=db, skip=skip, limit=limit)
    return users


@router.post("/login", response_model=UserResponse)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
                     db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db,
                                   form_data.username,
                                   form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
    return user


@router.post("/sign-up", response_model=UserResponse)
async def sign_up_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    created_user = await create_user(db, user)
    return created_user


@router.post("/logout")
async def logout_user():
    # Implement token invalidation or session logout logic here
    return {"msg": "User logged out successfully"}


@router.put("/users/{user_id}/change-email", response_model=User)
async def change_email_route(
    user_id: int,
    new_email: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change the email of the user.
    """
    user = await change_user_email(db=db,
                                   user_id=user_id,
                                   new_email=new_email,
                                   current_user=current_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}/change-password", response_model=User)
async def change_password_route(
    user_id: int,
    new_password: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change the password of the user.
    """
    user = await change_user_password(db=db,
                                      user_id=user_id,
                                      new_password=new_password,
                                      current_user=current_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users/{user_id}/top-up", response_model=UserResponse)
async def top_up_balance_route(
    user_id: int,
    amount: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    """
    Top up the balance of the user.
    """
    if user_id != current_user:
        raise HTTPException(status_code=403,
                            detail="Not authorized to top up this account")

    user = await top_account(db=db, 
                             user_id=user_id,
                             amount=amount)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
