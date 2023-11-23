from fastapi import FastAPI,  Form, Depends, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from HistoryOperations.router import router as history_router
from auth.router import router as auth_router
from Detection.router import router as detection_router
import logging

app = FastAPI(title="URBATON")
origins = ["*"]
app.mount("/static", StaticFiles(directory="static/"), name="static")
app.include_router(history_router)
app.include_router(auth_router)
app.include_router(detection_router)
logging.basicConfig(filename='work.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.get('/')
async def home():
    return FileResponse('/home/NO_BACK_MISIS/python-backend/static/main.html')


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
