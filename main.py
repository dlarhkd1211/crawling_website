from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('-no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('chromedriver.exe')#, options = chrome_options)

url = 'https://play.google.com/store/apps/details?id=co.fount.litchi&hl=ko&gl=US&showAllReviews=true'

driver.get(url)

f = open('review.txt', 'w', encoding='utf8')

while True:
  last_height = driver.execute_script("return document.body.scrollHeight")
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  sleep(1.0)
  new_height = driver.execute_script("return document.body.scrollHeight")
  if new_height == last_height:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1.0)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
      try:
        driver.find_element_by_xpath("//span[@class='RveJvd snByac']").click()
      except:
        break
    else:
      last_height = new_height
      continue

pageString = driver.page_source
bsObj = BeautifulSoup(pageString, 'lxml')

company = '파운트'
for link in bsObj.find_all(name = "div", attrs = {"class": "d15Mdf bAhLNe"}):
  name = link.find_all('span')
  f.write(name[0].get_text())
  f.write(';')
  f.write(str(name[1]).split('\"')[5])
  f.write(';')
  if name[-2].get_text() ==company:
    if name[-4].get_text() == '전체 리뷰':
      f.write(name[-3].get_text())
    else:
      f.write(name[-4].get_text())
  else:
    if name[-2].get_text() == '전체 리뷰':
      f.write(name[-1].get_text())
    else:
      f.write(name[-2].get_text())
  f.write('\n')
