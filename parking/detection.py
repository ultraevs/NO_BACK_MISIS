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
    status = get_image(place_id)
    print(status)
    slots_coords = parking_slots[place_id]

    results = model('img.jpg', save=True, verbose=False, conf=0.1)

    for result in results:
        print(results)


    return [status]
