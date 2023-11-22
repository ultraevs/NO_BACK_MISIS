from fastapi import FastAPI,  Form, Depends, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db, engine
from models import User
from sqlalchemy import select
from HistoryOperations.router import router as history_router
from auth.router import router as auth_router
from Detection.router import router as detection_router
app = FastAPI(title="URBATON")
origins = ["*"]
app.mount("/static", StaticFiles(directory="static/"), name="static")
app.include_router(history_router)
app.include_router(auth_router)
app.include_router(detection_router)


@app.get('/')
async def home():
    return FileResponse('/home/NO_BACK_MISIS/python-backend/static/main.html')


@app.get('/profile')
async def profile(user_id: str = Cookie(...), session: Session = Depends(get_db)):
    query = select(User).where(User.id == user_id)
    user = session.execute(query).scalar()
    return {"status": 200, "name": user.name, "phone": user.phone}


@app.exception_handler(404)
async def custom_404(_, __):
    return FileResponse('/home/NO_BACK_MISIS/python-backend/static/404.html')


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
