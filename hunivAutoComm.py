from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

base_url = 'http://web.humoruniv.com/board/humor/'

driver = webdriver.PhantomJS('phantomjs파일 경로')
driver.implicitly_wait(3)

driver.get('https://web.humoruniv.com/user/login.html')
driver.find_element_by_name('id').send_keys('아이디')
driver.find_element_by_name('pw').send_keys('비밀번호')
driver.find_element_by_xpath('//*[@id="wrap_log"]/div[2]/table/tbody/tr[2]/td/table/tbody/tr[1]/td[3]/input').click()

while True:
    start = time.time()
    req = requests.get('http://web.humoruniv.com/board/humor/list.html?table=pdswait')
    req.encoding = 'euc-kr'

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    list = soup.select('td.li_sbj > a')
    latest = list[0].text

    url = base_url + list[0].get('href')
    latestTitle = latest[0:latest.rfind('[')].rstrip(" \t\n\r")

    with open(os.path.join(BASE_DIR, 'latest.txt'), 'r', encoding="euc-kr") as f_read:
        before = f_read.readline()
        if before != latestTitle:
            print("새글 :", latestTitle)
            driver.get(url)
            driver.find_element_by_xpath('//*[@id="cmt_wrap_write"]/table/tbody/tr[1]/td[2]/input').send_keys('입력할 댓글')
            driver.find_element_by_id('comment_form_submit').click()
        f_read.close()
    with open(os.path.join(BASE_DIR, 'latest.txt'), 'w', encoding="euc-kr") as f_write:
        f_write.write(latestTitle)
        f_write.close()

    end = time.time()
    print(start - end)
    time.sleep(1)
