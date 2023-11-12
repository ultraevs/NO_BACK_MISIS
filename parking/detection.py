from get_image import get_image
from parking_cfg import parking_slots
from ultralytics import YOLO


def parking_info(model, place_id: int) -> dict:
    """
    Using YOLOv8 model to detect parking spots.
    place_id: 0 or 1 > camera id

    returns: [status, {parking_slot_id: occupied/free, ...}]
    """
    # get camera_frame
    print('[detection] Trying to get image...')
    status = get_image(place_id)
    slots_coords = parking_slots[place_id]
    print('[detection] ended image request')

    print('[detection] detecting via YOLO')
    results = model('img.jpg', save=True, verbose=False, conf=0.1)
    print('[detection] ended detection')
    #for result in results:
        #print(results)

    return [status]
