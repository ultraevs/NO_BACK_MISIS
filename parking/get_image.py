import urllib.request
import datetime
import os
from PIL import Image
import cv2



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

def frame():
    status, frame = cv2.VideoCapture('camera_feed.mp4').read()
    cv2.imwrite('img.jpg', frame)
    

def download(place_id):
    # downloading video from camera
    links = {
        0: 'https://s2.moidom-stream.ru/s/public/0000007683-',
        1: 'https://flussonic2.powernet.com.ru:8081/user90880/tracks-v1/'
        #   https://flussonic2.powernet.com.ru:8081/user90880/tracks-v1/2023/11/12/14/05/59-12308.ts
    }
    status = False
    for second in range(59, -1, -1):
        try:
            if place_id == 0:
                time = f'{generate_time(place_id)}{second}.ts'
            elif place_id == 1:
                time = f'{generate_time(place_id)}{second}-12308.ts'
            
            link = links[place_id] + time
            print(f'trying: {link}')
            urllib.request.urlretrieve(
                link,
                'camera_feed.mp4'
            )
            # if uccessfully downloaded, delete previous image
            if os.path.exists('img.jpg'):
                os.remove('img.jpg')
            status = True
            break

        except Exception as e:
            None
    return status

def get_image(place_id: int):
    """
    needs place_id: 0 or 1, creates img.jpg frame from camera, returns status
    """

    if os.path.exists('camera_feed.mp4'):
        os.remove('camera_feed.mp4')
    
    if download(place_id):
        if place_id == 0: # rotate image
            os.system('ffmpeg -sseof -3 -i camera_feed.mp4 -update 1 -q:v 1 img.jpg -loglevel panic -hide_banner')
            image = Image.open('img.jpg')
            image.rotate(45).save('img.jpg')
        elif place_id == 1:
            frame()
            image = Image.open('img.jpg')
            image.rotate(-7).save('img.jpg')

        return 'exported'
    else:
        return 'failed'