from fastapi import FastAPI,  Form, Depends, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from HistoryOperations.router import router as history_router
from auth.router import router as auth_router
from Detection.router import router as detection_router
from PDDTests.router import router as pdd_router
import logging

app = FastAPI(title="URBATON")
origins = ["*"]
app.mount("/static", StaticFiles(directory="static/"), name="static")
app.mount("/static/assets", StaticFiles(directory="static/assets"), name="static/assets")
app.mount("/runs/segment/predict2", StaticFiles(directory="/runs/segment/predict2"), name="/runs/segment/predict2")
app.include_router(history_router)
app.include_router(auth_router)
app.include_router(detection_router)
app.include_router(pdd_router)
logging.basicConfig(filename='work.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.get('/')
async def home():
    return FileResponse('/home/NO_BACK_MISIS/python-backend/static/main.html')


@app.get('/vanya')
async def vanya():
    return FileResponse("/home/NO_BACK_MISIS/python-backend/static/assets/photo_2023-11-25_11-05-58.jpg")


@app.get('/res')
async def res():
    return FileResponse("/home/NO_BACK_MISIS/python-backend/runs/segment/predict/img1.jpg")


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
