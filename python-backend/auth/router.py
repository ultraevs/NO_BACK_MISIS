import sys
sys.path.append("..")
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from auth.manager import *
from sqlalchemy.orm import Session
from database import get_db, engine
from models import User
from sqlalchemy import select, insert

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    query = select(User).where(User.username == decoded_data["sub"])
    user = session.execute(query).scalar()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user


@router.post("/register")
def register_user(username: str = Form(...), password: str = Form(...), session: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    query = insert(User).values(username=username, hashed_password=hashed_password)
    session.execute(query)
    session.commit()

    jwt_token = create_jwt_token({"sub": username})
    return {"access_token": jwt_token, "token_type": "bearer"}


@router.post("/token")
def authenticate_user(username: str, password: str, session: Session = Depends(get_db)):
    query = select(User).where(User.username == username)
    user = session.execute(query).scalar()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    jwt_token = create_jwt_token({"sub": user.username})
    return {"access_token": jwt_token, "token_type": "bearer"}


@router.get('/me')
async def me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email}


@router.get('/my_profile')
async def my_profile(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email}