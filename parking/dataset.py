import urllib.request
import os
for h in range(0, 24):
    for min in range(0, 60, 10):
        url = f'https://s2.moidom-stream.ru/s/public/0000091651-20231112{h:02d}{min:02d}-34.ts'
        print(url)
        try:
            urllib.request.urlretrieve(
                    url,
                    f'tmp.mp4'
                )
            try:
                os.remove('img.jpg')
            except: None
            os.system('ffmpeg -sseof -3 -i tmp.mp4 -update 1 -q:v 1 img.jpg -hide_banner -loglevel quiet')
            os.rename('img.jpg', f'{h:02d}{min:02d}.jpg')
        except Exception as E:
            print(E)
        