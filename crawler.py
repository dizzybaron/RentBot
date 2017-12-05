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
browser.get('https://rent.591.com.tw/home/rent/index/r1s7k3.html?kind=1&region=1&section=7')
time.sleep(1)
browser.find_element_by_id("area-box-close").click()
browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')

# start crawler
soup = BeautifulSoup(browser.page_source, "lxml")
for address in soup.select('p.lightBox em'):
    print(address.text)
#browser.find_element_by_xpath("//a[5]/span").click()
browser.find_element_by_class_name('pageNext').click()

time.sleep(10)
browser.quit()
