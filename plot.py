#import
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import random
import time

# open browser(Firefox)
browser = webdriver.Firefox()
# get to the target page
browser.get('https://www.agoda.com/zh-tw/pages/agoda/default/DestinationSearchResult.aspx?city=4951&pagetypeid=103&origin=TW&cid=-209&tag=&gclid=&aid=130589&userId=d63bdf2f-e8f1-4ed1-b387-c5cda1cfa1d5&languageId=20&storefrontId=3&currencyCode=TWD&htmlLanguage=zh-tw&trafficType=User&cultureInfoName=zh-TW&checkIn=2017-12-08&checkOut=2017-12-09&los=1&rooms=1&adults=2&children=0&childages=&ckuid=d63bdf2f-e8f1-4ed1-b387-c5cda1cfa1d5')
# start crawler
soup = BeautifulSoup(browser.page_source, "lxml")
time.sleep(10)
browser.find_element_by_id('paginationNext').click()
time.sleep(10)

browser.quit()
