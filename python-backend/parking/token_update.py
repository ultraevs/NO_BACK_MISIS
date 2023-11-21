import parking
from parking.parking_cfg import links
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import configparser


def get_tokens():
    config = configparser.ConfigParser()
    config.read(r'/home/NO_BACK_MISIS/python-backend/parking/tokens.ini')
    print(config)
    if 'tokens' not in config:
        config.add_section('tokens')
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    service = Service(executable_path=r'/home/NO_BACK_MISIS/python-backend/parking/chromedriver')

    for i in [1,2]:
        link = links[i]
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(link)

        time.sleep(4)

        html = driver.page_source
        driver.close()

        html_formatted = BeautifulSoup(html, 'html.parser')
        player = html_formatted.find(class_='ModalBodyPlayer')
        iframe = player.find('iframe')
        link = iframe.get('src')
        token = link.split('=')[1].split('&')[0]
        if token:
            print(token)
            config.set('tokens', f'token_{i}', token)

    with open(r'/home/NO_BACK_MISIS/python-backend/parking/config.ini', 'w') as f:
        config.write(f)
    
            
