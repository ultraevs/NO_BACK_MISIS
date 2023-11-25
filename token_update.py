import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

while True:
    # load tokens from file
    with open('/home/NO_BACK_MISIS/python-backend/Detection/tokens.txt', 'r') as f:
            lines = f.readlines()
            token_1 = lines[0].strip()
            token_2 = lines[1].strip()

    # check if token active
    try:
        token_1 = requests.get(f'http://136.169.144.8/1537240875/tracks-v1/index.fmp4.m3u8?token={token_1}')
        token_2 = requests.get(f'http://136.169.144.3/1549021886/tracks-v1/index.fmp4.m3u8?token={token_2}')
    except:
        upd = True
    
    if token_1.status_code != 200 or token_2.status_code != 200:
        upd = True
    else:
        upd = False

    if upd:
        print('automatically updating tokens...', end='')
        WINDOW_SIZE = "1920,1080"
        chrome_options = Options()
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-path=/home/NO_BACK_MISIS/python-backend/Detection/driver.log")
        service = Service(executable_path='/home/NO_BACK_MISIS/python-backend/Detection/drv')
        updated_tokens = {}

        links = {
            1: 'http://maps.ufanet.ru/yanaul#1537240875',
            2: 'http://maps.ufanet.ru/yanaul#1549021886'
        }

        for i in [1, 2]:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            link = links[i]
            driver.get(link)
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[2]/div/div[3]/div[2]/div/div[1]/div/div[1]/iframe'))
                )
            except Exception as e:
                None
                

            html = driver.page_source
            driver.close()

            html_formatted = BeautifulSoup(html, 'html.parser')
            player = html_formatted.find(class_='ModalBodyPlayer')
            iframe = player.find('iframe')
            link = iframe.get('src')
            token = link.split('=')[1].split('&')[0]

            updated_tokens[i] = token
    
        with open('/home/NO_BACK_MISIS/python-backend/Detection/tokens.txt', 'w') as f:
            f.write(updated_tokens[1] + '\n')
            f.write(updated_tokens[2])
        print('success')
    else:
        print('tokens update not needed')
    time.sleep(300)