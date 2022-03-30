# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from urllib.parse import urlparse
from urllib.parse import parse_qs
from bs4 import BeautifulSoup
from multiprocessing import Process
from time import sleep
from flask import Flask
from flask import jsonify
app = Flask(__name__)

DRIVER_PATH = './chromedriver'

username = 'TYJJ7557'
password = 'hQkD9!NWhRp8'

def waitSelect(driver):
    res = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    ranking = soup.find("tbody", {"id": "ranking_body"})
    timeout = time.time() + 60 * 1
    while len(ranking.contents) < 2 and time.time() < timeout:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ranking = soup.find("tbody", {"id": "ranking_body"})
    selectData = BeautifulSoup(driver.page_source, 'html.parser').find("tbody", {"id": "ranking_body"})
    data = []
    rows = selectData.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    for item in data:
        item.pop()
        print(item)
    return data


def process():
    print("bebebe")
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.maximize_window()
    driver.get('https://www.rakuten-sec.co.jp/')
    driver.find_element_by_id('form-login-id').send_keys(username)
    driver.find_element_by_id('form-login-pass').send_keys(password)
    driver.find_element_by_id('login-btn').click()
    print("ting ting")
    parsed_url = urlparse(driver.current_url)
    sessionID = parse_qs(parsed_url.query)['BV_SessionID'][0]
    print("bim bim")
    nextUrl = 'https://member.rakuten-sec.co.jp/app/market_top.do;BV_SessionID={}'.format(
        sessionID)
    driver.get(nextUrl)

    selectBox = driver.find_element_by_name("rankingType") 
    result = []
    print("------Data Động------")
    for index in range(len(selectBox.find_elements_by_tag_name("option"))):
      select = Select(driver.find_element_by_name("rankingType"))
      select.select_by_index(index)
      result.append(waitSelect(driver=driver))
      print("--------------")
    return(jsonify(result))

@app.route('/tobi')
def tobi():
  return "Bing"

@app.route('/')
def index():
  result = process()
  return result

if __name__ == "__main__":
  app.run(port=2608)


