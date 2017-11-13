import requests
from bs4 import BeautifulSoup
import json
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

while True:
    #req = requests.get('http://web.humoruniv.com/board/humor/list.html?table=pds')
    req = requests.get('http://web.humoruniv.com/board/humor/list.html?table=pdswait')
    req.encoding = 'euc-kr'

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    list = soup.select('td.li_sbj')
    latest = list[0].text
    latestTitle = latest[1:latest.rfind('[')].rstrip(" \t\n\r")
    with open(os.path.join(BASE_DIR, 'latest.txt'), 'r', encoding="euc-kr") as f_read:
        before = f_read.readline()
        if before != latestTitle:
            print("새글 :",latestTitle)
        f_read.close()
    with open(os.path.join(BASE_DIR, 'latest.txt'), 'w', encoding="euc-kr") as f_write:
        f_write.write(latestTitle)
        f_write.close()
    time.sleep(1)

