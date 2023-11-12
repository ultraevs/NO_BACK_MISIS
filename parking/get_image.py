import urllib.request
import datetime
import os

seconds = ['54', '44', '34', '24', '14', '04']


def generate_name():
    # YYYYMMDDHHMM-SS
    current_time = datetime.datetime.now()
    name = '0000091651-' + current_time.strftime("%Y%m%d%H%M-")
    return name
def download():
    # downloading video from camera
    status = False
    for second in seconds:
        try:
            time = f'{generate_name()}{second}'
            print(f'trying: {time}')
            urllib.request.urlretrieve(
                f'https://s2.moidom-stream.ru/s/public/{time}.ts',
                'camera_feed.mp4'
            )
            # if uccessfully downloaded, delete previous image
            if os.path.exists('img.jpg'):
                os.remove('img.jpg')
            status = True
            break

        except:
            # if not downloaded, skip and use previous image
            None
    return status

def get_image():
    if os.path.exists('camera_feed.mp4'):
        os.remove('camera_feed.mp4')
    
    if download():
        os.system('ffmpeg -sseof -3 -i camera_feed.mp4 -update 1 -q:v 1 img.jpg -hide_banner -loglevel quiet')
        print('Successfully updated image')
    else:
        print('Failed to update image, use previous image')

get_image()
