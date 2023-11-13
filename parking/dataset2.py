import urllib.request
import os

url = 'https://live.cmirit.ru/live/smart3_1920x1080.stream/media_w324693318_'


starting_number = 88067

is_downloaded = False
for x in range(starting_number, 99999):
    print('trying to find active url...')
    try:
        urllib.request.urlretrieve(
            url + str(x) + '.ts',
            str(x) + '.mp4'
        )
        print('active url found! starting from:', x)
        active = x
        break
    except: None 
for x in range(active+1, 99999):
    ok = False
    while not ok:
        print('trying...')
        try:
            urllib.request.urlretrieve(
                url + str(x) + '.ts',
                str(x) + '.mp4'
            )
            ok = True
        except: None
    print('downloaded: ' + str(x))
    # use ffmeg to export frames from video with fps = 1
    os.system(f'ffmpeg -i {x}.mp4 -vf fps=1/3 frames/frame_{x}_%05d.png')
    os.remove(f'{x}.mp4')