import requests
from bs4 import BeautifulSoup

def update(place_id: int)  -> str:
    urls = {
        1: 'http://136.169.144.5/1531895611/tracks-v1/index.fmp4.m3u8?token=ff78c86116204b46a1d60686ded45773',
        2: 'http://136.169.144.3/1549021886/tracks-v1/index.fmp4.m3u8?token=00582daae2b742ee89c7c7e2caf15127'
    }

    