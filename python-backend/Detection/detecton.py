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
from PIL import Image, ImageDraw
import shutil
import logging
import numpy as np

def crop_image(image_path, x1, y1, x2, y2, save_path):
    try:
        image = cv2.imread(image_path)
        cropped_image = image[y1:y2, x1:x2]
        cv2.imwrite(save_path, cropped_image)
    except Exception as e:
        print(e)


def get_tokens():
    logging.info('get_tokens() started')
    links = {
        1: 'http://maps.ufanet.ru/yanaul#1537240875',
        2: 'http://maps.ufanet.ru/yanaul#1549021886'
    }
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-path=/home/NO_BACK_MISIS/python-backend/Detection/driver.log")
    service = Service(executable_path='/home/NO_BACK_MISIS/python-backend/Detection/drv')
    updated_tokens = {}

    for i in [1, 2]:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logging.info('driver created')
        link = links[i]
        driver.get(link)
        logging.info('waiting for element')
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div/div[3]/div[2]/div/div[1]/div/div[1]/iframe'))
            )
        except Exception as e:
            logging.info('no element found')
            return False
            

        html = driver.page_source
        driver.close()
        logging.info('driver closed')

        html_formatted = BeautifulSoup(html, 'html.parser')
        player = html_formatted.find(class_='ModalBodyPlayer')
        iframe = player.find('iframe')
        link = iframe.get('src')
        token = link.split('=')[1].split('&')[0]
        logging.info('got token')

        updated_tokens[i] = token
    
    logging.info(f'got tokens: {updated_tokens}')
    return updated_tokens


def update_cfg():
    logging.info('writing tokens to file')
    new_tokens = get_tokens()
    if new_tokens:
        with open('Detection/tokens.txt', 'w') as f:
            f.write(new_tokens[1] + '\n')
            f.write(new_tokens[2])
        logging.info('update_cfg() -> True')
        return True
    else:
        logging.info('update_cfg() -> False')
        return False


def get_image():
    logging.info('starting get_image()')
    links = {
        1: 'http://136.169.144.8/1537240875/tracks-v1/index.fmp4.m3u8?token=',
        2: 'http://136.169.144.3/1549021886/tracks-v1/index.fmp4.m3u8?token='
    }
    try:
        with open('Detection/tokens.txt', 'r') as f:
            lines = f.readlines()
            token_1 = lines[0].strip()
            token_2 = lines[1].strip()
        logging.info('loaded tokens from file')
    except:
        with open('Detection/tokens.txt', 'w') as file:
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
                logging.info('unsuccessful request, attempting to update tokens')
                update_needed = True
                break
        except:
            logging.info('got error during request, attempting to update tokens')
            update_needed = True
            break

    if update_needed:
        if update_cfg():
            logging.info('successfully updated tokens')
        else:
            logging.info('tokens update failed, get_image() -> False')
            return False

    with open('Detection/tokens.txt', 'r') as f:
        lines = f.readlines()
        token_1 = lines[0].strip()
        token_2 = lines[1].strip()
    logging.info('loaded tokens from file')

    for i in [1,2]:
        success = True
        if i == 1:
            token = token_1
        else:
            token = token_2
        try:
            lnk = links[i] + token
            capture = cv2.VideoCapture(lnk)
            logging.info(f'getting image from: {lnk}')
            ret, frame = capture.read()
            cv2.imwrite(f"img{i}.jpg", frame)
        except Exception as e:
            success = False
            logging.info('failed to get image')
            break
    

    if not success:
        logging.info('get_image() -> False')
        return False
    else:
        logging.info('get_image() -> True')
        return True


def is_in_rect(x1, y1, x2, y2, x, y):
    return x1 <= x <= x2 and y1 <= y <= y2


def check_boxes(results, id_, plates_model, cymbols_model):
    print(os.path.getsize('img3.jpg'))
    logging.info('check_boxes() started')
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
            ((0.97, 0.66), (0.95, 0.50)) ],
        
        3: [((0.50, 0.50), (0.50, 0.50)),
            
            ]
    }

    coords = parking_slots[id_]
    logging.info('got parking coords')
    data = {}

    shutil.copy(f'img{id_}.jpg', 'result.jpg')
    logging.info('created result.jpg file')
    img = Image.open('result.jpg')
    width1, height1 = Image.open(f'img{id_}.jpg').size
    #width1, height1 = width1, height1*2

    # detect numbers only for camera 3
    names = cymbols_model.names
    if id_ == 3:
        data = {}
        for i in range(7):
            data[i] = ['occupied', None]
            # detect number on each img in folder
            results = plates_model(f'/home/NO_BACK_MISIS/python-backend/Detection/cam3_data/cropped_3_{i}.jpg', save=True, verbose=False, conf=0.4)
            for result in results:
                plate_boxes = result.boxes.xyxyn.tolist()

                cropped_3_w, cropped_3_h = Image.open(f'/home/NO_BACK_MISIS/python-backend/Detection/cam3_data/cropped_3_{i}.jpg').size
                for plate_box in plate_boxes:
                    plate_x1, plate_y1, plate_x2, plate_y2 = plate_box
                    plate_x1_n, plate_y1_n, plate_x2_n, plate_y2_n = int(round(plate_x1*cropped_3_w)), int(round(plate_y1*cropped_3_h)), int(round(plate_x2*cropped_3_w)), int(round(plate_y2*cropped_3_h))
                    #crop_image(f'/home/NO_BACK_MISIS/python-backend/Detection/cam3_data/cropped_3_{i}.jpg', plate_x1_n, plate_y1_n, plate_x2_n, plate_y2_n, f'/home/NO_BACK_MISIS/python-backend/Detection/cam3_data/plate_cropped_3_{i}.jpg')
            results = cymbols_model(f'/home/NO_BACK_MISIS/python-backend/Detection/cam3_data/plate_cropped_3_{i}.png', save=True, verbose=False, conf=0.65)
            for r in results:
                t = []
                # append all coords of boxes
                cymbols_boxes = r.boxes.xyxyn.tolist()
                for cymbols_box in cymbols_boxes:
                    cymbols_x1, cymbols_y1, cymbols_x2, cymbols_y2 = cymbols_box
                    t.append([min(cymbols_x1, cymbols_x2), None])

                # get all classnames and append to list
                j = 0
                for c in r.boxes.cls:
                    t[j][1] = names[int(c)]
                    j += 1
                
                sorted_t = sorted(t, key=lambda x: x[0])
                letters = [item[1] for item in sorted_t]
                result_string = ''.join(letters)
                data[i] = ["occupied", result_string]
                
        return data

    logging.info('checking parking slots and cars')
    for result in results:
        boxes = result.boxes.xyxyn.tolist()

        park_slot_id = 0
        for coord in coords:
            t = False
            coord1, coord2 = coord
            x1, y1 = coord1  # 1 dot coords
            x2, y2 = coord2  # 2 dot coords

            point_size = 10

            # check if 2 dots inside of any box
            for box in boxes:
                box_x1, box_y1, box_x2, box_y2 = box
                x1_n, y1_n, x2_n, y2_n = int(round(box_x1*width1)), int(round(box_y1*height1)), int(round(box_x2*width1)), int(round(box_y2*height1))
                if is_in_rect(min(box_x1, box_x2), min(box_y1, box_y2), max(box_x1, box_x2), max(box_y1, box_y2), 
                            x1, y1):
                    if is_in_rect(min(box_x1, box_x2), min(box_y1, box_y2), max(box_x1, box_x2), max(box_y1, box_y2),
                                  x2, y2):
                        t = True
                        data[park_slot_id] = ['occupied', None]
                        logging.info('cropping')
                        crop_image(f'img{id_}.jpg', x1_n, y1_n, x2_n, y2_n, fr'cropped_{id_}_{park_slot_id}.jpg')
                        # plates_results = plates_model(fr'cropped_{id_}_{park_slot_id}.jpg', save=True, verbose=False, conf=0.05)
                        # for plate_result in plates_results:
                        #     plate_boxes = plate_result.boxes.xyxyn.tolist()
                        #     for plate_box in plate_boxes:
                        #         pbox_x1, pbox_y1, pbox_x2, pbox_y2 = plate_box
                        #         pwidth1, pheight1 = Image.open(f'cropped_{id_}_{park_slot_id}.jpg').size
                        #         px1_n, py1_n, px2_n, py2_n = int(round(pbox_x1*pwidth1)), int(round(pbox_y1*pheight1)), int(round(pbox_x2*pwidth1)), int(round(pbox_y2*pheight1))
                        #         crop_image(f'cropped_{id_}_{park_slot_id}.jpg', px1_n, py1_n, px2_n, py2_n, fr'plate_cropped_{id_}_{park_slot_id}.jpg')
                        break
            if not t:
                data[park_slot_id] = ['free', False]
                
            park_slot_id += 1
    logging.info('done checking')
    img.save('result.jpg')
    logging.info('saved drawings to result.jpg')
    img.close()

    if data:
        logging.info('check_boxes() -> data')
        return data
    else:
        logging.info('check_boxes() -> None')
        return None


def detect(model, plates_model, cymbols_model, id_):
    for i in [1, 2, 3]:
        for ii in range(0, 10):
            try:
                os.remove(fr'/home/NO_BACK_MISIS/python-backend/cropped_{i}_{ii}.jpg')
                os.remove(fr'/home/NO_BACK_MISIS/python-backend/plate_cropped_{i}_{ii}.jpg')
                #os.remove(fr'/home/NO_BACK_MISIS/python-backend/Detection/cam3_data/plate_cropped_3_{i}.jpg')
            except: None
    if id_ not in [1,2,3]: return {'status': 'id failed', 'data': None}
    logging.info('starting detection')
    if get_image():
        logging.info('status = ok')
        status = 'ok'
    else:
        if os.path.exists(f'img{id_}.jpg'):
            logging.info('status = outdated')
            status = 'outdated'
        else:
            logging.info('status = failed')
            status = 'failed'

    if status != 'failed':
        logging.info('starting detection via YOLO')
        results = model(f'img{id_}.jpg', save=True, verbose=False, conf=0.3)
        if results:
            data = check_boxes(results, id_, plates_model, cymbols_model)
        else:
            logging.info('no results provided, data is empty')
            data = None
    else:
        data = None

    logging.info('detection end, returned status, data')
    return {'status': status, 'data': data}
