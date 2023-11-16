from fastapi import FastAPI, Request, status, Depends
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from MainRouter import router as main_router


app = FastAPI(title="UTRBATON")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main_router)
#app.mount("/static", StaticFiles(directory="static/"), name="static")
# app.mount("/static/assets", StaticFiles(directory="static/assets"), name="/static/assets")
