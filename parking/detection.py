from get_image import get_image
from parking_cfg import parking_slots
import os


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
    slots_coords = parking_slots[place_id]
    print('[detection] ended image request')

    print('[detection] detecting via YOLO')
    if status == 'exported':
        results = model(f'img_{place_id}.jpg', save=True, verbose=False, conf=0.1)
        print('[detection] ended detection')
    else:
        print('[detection] cant get image')
        if os.path.exists(f'img_{place_id}.jpg'):
            print('[!][detection] using previous image from backup')
            results = model(f'img_{place_id}.jpg', save=True, verbose=False, conf=0.1)
            return {'status': 'outdated', 'data': None}
        else:
            print('[!][detection] cant use previous image')
            return {'status': 'failed', 'data': None}

    #for result in results:
        #print(results)

    return {'status': status, 'data': None}
