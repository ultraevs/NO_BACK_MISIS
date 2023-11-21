from fastapi import APIRouter
from fastapi.responses import JSONResponse
import sys
sys.path.append('..')
from fastapi.responses import FileResponse
from parking import current_model
from pizda import detect
router = APIRouter(tags=["MAIN"])

model = current_model("segmentation.pt")


@router.get('/')
async def main():
    return FileResponse('/home/NO_BACK_MISIS/python-backend/static/main.html')


@router.post('/test')
async def test(cam_id: int):
    answer = detect(model, cam_id)
    return JSONResponse(content=answer)
