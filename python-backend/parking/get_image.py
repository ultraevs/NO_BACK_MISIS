import datetime
import os
import cv2
from parking.parking_cfg import links
import requests



def generate_time(place_id):
    # YYYYMMDDHHMM-SS
    current_time = datetime.datetime.now()
    if place_id == 0:
        time = current_time.strftime("%Y%m%d%H%M-")
    elif place_id == 1:
        time_1 = current_time.strftime("%Y/%m/%d/")
        time_H = int(current_time.strftime("%H"))-3
        time_M = int(current_time.strftime("%M"))-1
        if time_H < 0:
            time_H = 24 + time_H
        if time_M < 0:
            time_M = 59
        if len(str(time_M)) == 1:
            time_M = '0' + str(time_M)
        time = time_1 + str(time_H) + '/' + str(time_M) + '/'
    return time



def download(place_id):
    # downloading video from camera
    status = False
    print('[download] trying links...')
    if place_id in [1, 2]:
        try:
            print(f'loading from: {links[place_id]}')
            r = requests.get(links[place_id])
            if r.status_code == 200:
                capture = cv2.VideoCapture(links[place_id])
                ret, frame = capture.read()
                cv2.imwrite(f"img_{place_id}.jpg", frame)
                print('[download] link success, downloaded video')
                status = True
            elif r.status_code == 403:
                print('[download] token expired for: camera ' + str(place_id))
                status = False
            else:
                print(f'[download] unknown error (status code: {r.status_code})')
                status = False
        except Exception as e:
            print('[download] link failed')
            print(e)
            status = False

    return status

def get_image(place_id: int):
    """
    needs place_id: 1 or 2, creates img_{place_id}.jpg frame from camera, returns status
    """

    if os.path.exists('camera_feed.mp4'):
        os.remove('camera_feed.mp4')
    
    print('[get_image] requesting download')
    if download(place_id):
        print('[get_image] image saved')
        return 'exported'
    else:
        print('[get_image] download failed')
        return 'failed'