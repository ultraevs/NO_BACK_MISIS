import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import cv2
import os
from ultralytics import YOLO


def get_tokens():
    links = {
        1: 'http://maps.ufanet.ru/yanaul#1537240875',
        2: 'http://maps.ufanet.ru/yanaul#1549021886'
    }
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    service = Service(executable_path=r'/home/NO_BACK_MISIS/python-backend/parking/chromedriver')

    updated_tokens = {}
    for i in [1, 2]:
        link = links[i]
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(link)

        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div/div[3]/div[2]/div/div[1]/div/div[1]/iframe'))
            )
        except Exception as e:
            return False

        html = driver.page_source
        driver.close()

        html_formatted = BeautifulSoup(html, 'html.parser')
        player = html_formatted.find(class_='ModalBodyPlayer')
        iframe = player.find('iframe')
        link = iframe.get('src')
        token = link.split('=')[1].split('&')[0]

        updated_tokens[i] = token

    return updated_tokens


def update_cfg():
    new_tokens = get_tokens()
    if new_tokens:
        with open('../tokens.txt', 'w') as f:
            f.write(new_tokens[1] + '\n')
            f.write(new_tokens[2])
        return True
    else:
        return False


def get_image():
    links = {
        1: 'http://136.169.144.8/1537240875/tracks-v1/index.fmp4.m3u8?token=',
        2: 'http://136.169.144.3/1549021886/tracks-v1/index.fmp4.m3u8?token='
    }
    try:
        with open('../tokens.txt', 'r') as f:
            lines = f.readlines()
            token_1 = lines[0].strip()
            token_2 = lines[1].strip()
    except:
        print('no tokens file found')
        with open('../tokens.txt', 'w') as file:
            pass
        token_1 = ''
        token_2 = ''

    update_needed = False
    for i in range(1, 3):
        if i == 1:
            token = token_1
        else:
            token = token_2
        try:
            link = links[i] + token
            r = requests.get(link)
            if r.status_code != 200:
                print(f'tokens outdated ({r.status_code})')
                update_needed = True
                break
        except:
            update_needed = True
            break

    if update_needed:
        print('tokens outdated, updating')
        if update_cfg():
            print('tokens updated')
        else:
            print('tokens update failed')
            return False

    with open('../tokens.txt', 'r') as f:
        lines = f.readlines()
        token_1 = lines[0].strip()
        token_2 = lines[1].strip()

    print('loading images')

    for i in range(1, 3):
        success = True
        if i == 1:
            token = token_1
        else:
            token = token_2
        try:
            lnk = links[i] + token
            capture = cv2.VideoCapture(lnk)
            ret, frame = capture.read()
            cv2.imwrite(f"img{i}.jpg", frame)
        except Exception as e:
            print('failed to download image')
            print(e)
            success = False
            break

    if not success:
        return False
    else:
        return True


def is_in_rect(x1, y1, x2, y2, x, y):
    return x1 <= x <= x2 and y1 <= y <= y2


def check_boxes(results, id_):
    parking_slots = {
        1: [((0.02, 0.20), (0.02, 0.20)),
            ((0.12, 0.14), (0.15, 0.08)),
            ((0.18, 0.13), (0.23, 0.07)),
            ((0.26, 0.15), (0.30, 0.07)),
            ((0.36, 0.15), (0.40, 0.07)),
            ((0.48, 0.17), (0.50, 0.06)),
            ((0.60, 0.20), (0.60, 0.10)),
            ((0.72, 0.20), (0.70, 0.09)),
            ((0.84, 0.26), (0.82, 0.17)),
            ((0.93, 0.29), (0.90, 0.21)), ],

        2: [((0.30, 0.19), (0.24, 0.25)),
            ((0.37, 0.22), (0.34, 0.29)),
            ((0.46, 0.25), (0.43, 0.35)),
            ((0.55, 0.41), (0.56, 0.28)),
            ((0.70, 0.50), (0.70, 0.34)),
            ((0.86, 0.59), (0.83, 0.40)),
            ((0.97, 0.66), (0.95, 0.50))]
    }

    coords = parking_slots[id_]
    data = {}

    for result in results:
        boxes = result.boxes.xyxyn.tolist()
        park_slot_id = 0
        for coord in coords:
            t = False
            coord1, coord2 = coord
            x1, y1 = coord1  # 1 dot coords
            x2, y2 = coord2  # 2 dot coords

            # check if 2 dots inside of any box
            for box in boxes:
                box_x1, box_y1, box_x2, box_y2 = box
                if is_in_rect(min(box_x1, box_x2), min(box_y1, box_y2), max(box_x1, box_x2), max(box_y1, box_y2), x1,
                              y1):
                    if is_in_rect(min(box_x1, box_x2), min(box_y1, box_y2), max(box_x1, box_x2), max(box_y1, box_y2),
                                  x2, y2):
                        t = True
                        data[park_slot_id] = 'occupied'
                        break
            if not t:
                data[park_slot_id] = 'free'

            park_slot_id += 1

    if data:
        return data
    else:
        return None


def detect(model, id_):
    if get_image():
        print('successfully updated camera frames')
        status = 'ok'
    else:
        if os.path.exists(f'img{id}.jpg'):
            print('using previous images')
            status = 'outdated'
        else:
            print('previous images not found')
            status = 'failed'

    if status != 'failed':
        print('detecting')
        results = model(f'img{id_}.jpg', save=False, verbose=False, conf=0.7)
        if results:
            print('predicted, generating response')
            data = check_boxes(results, id_)
        else:
            data = None
    else:
        data = None

    return {'status': status, 'data': data}
