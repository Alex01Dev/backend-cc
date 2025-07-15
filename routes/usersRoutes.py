from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta

from config.db import get_db
from config.jwt import create_access_token, get_current_user

from models.usersModel import User as UserDB
from schemas.userSchemas import UserLogin, UserCreate, User, UserSimple
from controller.userController import (
    authenticate_user,
    get_user_by_username,
    get_user_by_username_or_email,
    get_user_by_id,
    create_user,
    get_active_users
)

user = APIRouter()
security = HTTPBearer()

@user.post("/login", response_model=dict, tags=["Authentication"])
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(
        db, username=user_data.username, password=user_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "logged_user": user.username,
        "user_email": user.email
    }

@user.post("/register", response_model=User, tags=["Users"])
async def register_new_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user_data.status = user_data.status or "Active"

    existing_user = get_user_by_username_or_email(
        db=db,
        username=user_data.username,
        email=user_data.email
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    return create_user(db=db, user=user_data)

@user.get("/users/{id}", response_model=User, tags=["Users"])
async def read_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = get_user_by_id(db=db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user.get("/user/{username}", tags=["Users"])
async def get_basic_user(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "registration_date": user.registration_date,
        "status": user.status
    }

@user.get("/users", response_model=List[UserSimple], tags=["Users"])
def get_active_users_list(db: Session = Depends(get_db)):
    users = get_active_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return [{"id": u.id, "username": u.username, "status": u.status} for u in users]
