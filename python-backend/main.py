from fastapi import FastAPI, Request, status, Depends
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from MainRouter import router as main_router
from HistoryRouter import router as history_router
from auth.router import router as auth_router
app = FastAPI(title="URBATON")
origins = ["*"]
app.mount("/static", StaticFiles(directory="static/"), name="static")
app.include_router(main_router)
app.include_router(history_router)
app.include_router(auth_router)


@app.exception_handler(404)
async def custom_404(_,__):
    return FileResponse('/static/404.html')


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
