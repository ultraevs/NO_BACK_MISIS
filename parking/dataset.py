import time
import cv2

urls = [
    'http://136.169.144.5/1531895611/tracks-v1/index.fmp4.m3u8?token=9a6e23ca4b574e57ba0d9ebd04aff670',
    'http://136.169.144.3/1549021886/tracks-v1/index.fmp4.m3u8?token=e3bc0fbf2d674cfc85a09be042ebb6c7'
]

print('starting')
img_id = 0
while True:
    t = 0
    for url in urls:
        try:
            capture = cv2.VideoCapture(url)
            ret, frame = capture.read()
            cv2.imwrite(f'{img_id}_{t}.jpg', frame)
            print(f'{img_id}_{t}.jpg -> saved')
        except: print('failed')
        t += 1

    img_id += 1
    time.sleep(900)