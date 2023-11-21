import sys
sys.path.append("..")
from fastapi import Depends, APIRouter, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from auth.manager import *
from sqlalchemy.orm import Session
from database import get_db, engine
from models import User
from sqlalchemy import select, insert

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
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
    return RedirectResponse(url='/profile')


@router.post("/login")
def authenticate_user(username: str, password: str, session: Session = Depends(get_db)):
    query = select(User).where(User.username == username)
    user = session.execute(query).scalar()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    jwt_token = create_jwt_token({"sub": user.username})
    if get_current_user(jwt_token):
        return RedirectResponse(url='/profile')
    else:
        return {"status": 'huy'}