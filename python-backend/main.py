from fastapi import FastAPI, Request, status, Depends
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from MainRouter import router as main_router

app = FastAPI(title="URBATON")
origins = ["*"]
app.mount("/static", StaticFiles(directory="static/"), name="static")
app.include_router(main_router)

@app.exception_handler(404)
async def custom_404(_,__):
    return FileResponse('/home/NO_BACK_MISIS/python-backend/static/404.html')


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static/assets", StaticFiles(directory="static/assets"), name="/static/assets")
