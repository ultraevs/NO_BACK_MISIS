import urllib.request
import datetime
import os



def generate_time():
    # YYYYMMDDHHMM-SS
    current_time = datetime.datetime.now()
    time = current_time.strftime("%Y%m%d%H%M-")
    return time
def download(place_id):
    # downloading video from camera
    links = {
        0: 'https://s2.moidom-stream.ru/s/public/0000007683-',
        1: ''
    }
    status = False
    for second in range(60, 0, -1):
        try:
            time = f'{generate_time()}{second}.ts'
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

        except:
            # if not downloaded, skip and use previous image
            None
    return status

def get_image(place_id):
    if os.path.exists('camera_feed.mp4'):
        os.remove('camera_feed.mp4')
    
    if download(place_id):
        os.system('ffmpeg -sseof -3 -i camera_feed.mp4 -update 1 -q:v 1 img.jpg -hide_banner -loglevel quiet')
        print('Successfully updated image')
    else:
        print('Failed to update image, use previous image')

place_id = 0

get_image(place_id)