from fastapi import APIRouter
from fastapi.responses import JSONResponse
import sys
sys.path.append('..')
from parking import current_model, detection
router = APIRouter(tags=["MAIN"])


@router.post('/test')
async def test(cam_id: int):
    model = current_model("segmentation.pt")
    answer = detection.parking_info(model, cam_id)
    return JSONResponse(content=answer)