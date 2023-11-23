import sys
from datetime import timedelta
from email.message import EmailMessage
sys.path.append("..")
from pathlib import Path
from fastapi import Depends, APIRouter, HTTPException, Form, Cookie, BackgroundTasks
from fastapi.responses import RedirectResponse, FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import smtplib
from celery import Celery
from database import get_db, engine
from models import User
from sqlalchemy import select, insert
from passlib.context import CryptContext
from auth.manager import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, verify_token

router = APIRouter(tags=["AUTH"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router.mount("/static", StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"), name="static")
router.mount("/static/assets", StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static/assets"),
             name="static/assets")

smtp_user = 'NoBackMISIS@gmail.com'
smtp_pass = 'rhvx hnkp klkn ccje'
smtp_host = "smtp.gmail.com"
smtp_port = 465
celery = Celery('tasks', broker='redis://localhost:6379')


def get_email_template_dashboard(username: str, password: str, name: str):
    email = EmailMessage()
    email['Subject'] = 'Восстановление пароля'
    email['From'] = smtp_user
    email['To'] = username

    email.set_content(
        '<div>'
        f'<h1>Здравствуйте, {name}, Ваш актуальный пароль:</h1>'
        f'<p>{password}</p>'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_forgot(email: str, password: str, name: str):
    message = get_email_template_dashboard(email, password, name)
    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(smtp_user, smtp_pass)
        server.send_message(message)


@router.get('/register')
async def get_register():
    return FileResponse('/home/NO_BACK_MISIS/python-backend/static/sign.html')


@router.post("/register")
def register_user(email: str = Form(...), password: str = Form(...), name: str = Form(...),
                  session: Session = Depends(get_db)):
    user = User(email=email, password_hash=pwd_context.hash(password), name=name)
    session.add(user)
    session.commit()
    session.refresh(user)
    token_data = {"sub": user.id, "name": user.name}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=token_data, expires_delta=access_token_expires)
    response = JSONResponse(status_code=200, content={"status": 200, "data": "ACCEPT"})
    response.set_cookie(key="access_token", value=access_token.decode("utf-8"))
    return response


@router.get('/login')
async def get_login():
    return FileResponse('/home/NO_BACK_MISIS/python-backend/static/index.html')


@router.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...), session: Session = Depends(get_db)):
    query = select(User).where(User.email == email)
    user = session.execute(query).scalar()
    if not user:
        return JSONResponse(status_code=401, content={"status": 401, "data": "Нет такого юзера"})
    if not pwd_context.verify(password, user.password_hash):
        return JSONResponse(status_code=401, content={"status": 401, "data": "Неверный пароль"})
    token_data = {"sub": user.id, "name": user.name}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=token_data, expires_delta=access_token_expires)
    response = JSONResponse(status_code=200, content={"data": "ACCEPT"})
    response.set_cookie(key="access_token", value=access_token.decode("utf-8"))
    return response


@router.get("/profile")
async def profile(access_token: str = Cookie(None)):
    try:
        data = verify_token(access_token)
        return FileResponse('/home/NO_BACK_MISIS/python-backend/static/profile.html')
    except HTTPException:
        return RedirectResponse('/login', status_code=303)


@router.get("/forgot")
async def forgot(background_tasks: BackgroundTasks, email: str = Form(...), session: Session = Depends(get_db)):
    query = select(User).where(User.email == email)
    user = session.execute(query).scalar()
    background_tasks.add_task(send_email_forgot, email, user.password, user.name)
    return JSONResponse(status_code=200, content="Письмо Отправлено")
