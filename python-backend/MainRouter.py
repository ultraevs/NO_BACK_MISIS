from fastapi import APIRouter
from fastapi.responses import JSONResponse
import sys
sys.path.append('..')
import parking
router = APIRouter(tags=["MAIN"])


@router.post('/test')
async def test(cam_id: int):
    model = parking.current_model("segmentation.pt")
    answer = parking.detection.parking_info(model, cam_id)
    return JSONResponse(content=answer)