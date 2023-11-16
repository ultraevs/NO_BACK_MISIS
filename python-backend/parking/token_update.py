from parking.parking_cfg import links
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import configparser


def get_tokens():
    config = configparser.ConfigParser()
    config.read('tokens.ini')
    if 'tokens' not in config:
        config.add_section('tokens')

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    service = Service(executable_path=r'C:\Users\Admin\Documents\parking\parking\chromedriver.exe')

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

    with open('config.ini', 'w') as f:
        config.write(f)
    
            