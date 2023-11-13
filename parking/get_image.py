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
        1: 'http://136.169.144.5/1531895611/tracks-v1/index.fmp4.m3u8?token=9a6e23ca4b574e57ba0d9ebd04aff670',
        2: 'http://136.169.144.3/1549021886/tracks-v1/index.fmp4.m3u8?token=e3bc0fbf2d674cfc85a09be042ebb6c7'
    }
    status = False
    print('[download] trying links...')
    if place_id in [1, 2]:
        try:
            capture = cv2.VideoCapture(links[place_id])
            ret, frame = capture.read()
            status = True
            print('[download] link success, downloaded video')
            if os.path.exists('img.jpg'):
                os.remove('img.jpg')
            cv2.imwrite("img.jpg", frame)
        except Exception as e:
            print('[download] link failed')
            print(e)
            status = False
    else:
        print('PLACE_ID=0 IS OUTDATED, USE PLACE_ID=1/2')
        for second in range(0, 60):
            if len(str(second)) == 1:
                second = '0' + str(second)
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
                print('[download] link success, downloaded video')
                if os.path.exists('img.jpg'):
                    os.remove('img.jpg')
                status = True
                break

            except Exception as e:
                print('[download] link failed')
    return status

def get_image(place_id: int):
    """
    needs place_id: 0 or 1, creates img.jpg frame from camera, returns status
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