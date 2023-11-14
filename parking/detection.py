from parking.get_image import get_image
from parking.parking_cfg import parking_slots
import os


def is_in_rect(x1, y1, x2, y2, x, y):
    return x1 <= x <= x2 and y1 <= y <= y2


def parking_info(model, place_id: int) -> dict:
    """
    Using YOLOv8 model to detect parking spots.
    place_id: 0 or 1 > camera id

    returns: {status=status, data={parking_slot_id: occupied/free, ...}}

    'exported': successfully detected cars on image

    'failed': cant get image and cant use previous image

    'outdated': used previous image, but detected cars
    """
    # get camera_frame

    print('[detection] Trying to get image...')
    status = get_image(place_id)
    coords = parking_slots[place_id]
    print('[detection] ended image request')

    print('[detection] detecting via YOLO')
    if status == 'exported':
        print('[detection] ended detection')
    else:
        print('[detection] cant get image')
        if os.path.exists(f'img_{place_id}.jpg'):
            print('[!][detection] using previous image from backup')
            status = 'outdated'
        else:
            print('[!][detection] cant use previous image')
            status = 'failed'
            data = None
            
    if status != 'failed':
        data = {}
        results = model(f'img_{place_id}.jpg', save=False, verbose=False, conf=0.7)
        for result in results:
            boxes = result.boxes.xyxyn.tolist()
            park_slot_id = 0
            for coord in coords:
                t = False
                coord1, coord2 = coord
                x1, y1 = coord1 # 1 dot coords
                x2, y2 = coord2 # 2 dot coords

                # check if 2 dots inside of any box
                for box in boxes:
                    box_x1, box_y1, box_x2, box_y2 = box
                    if is_in_rect(min(box_x1, box_x2), min(box_y1, box_y2), max(box_x1, box_x2), max(box_y1, box_y2), x1, y1):
                        if is_in_rect(min(box_x1, box_x2), min(box_y1, box_y2), max(box_x1, box_x2), max(box_y1, box_y2), x2, y2):
                            t = True
                            data[park_slot_id] = 'occupied'
                            break
                if not t:
                    data[park_slot_id] = 'free'

                park_slot_id += 1

    return {'status': status, 'data': data}
