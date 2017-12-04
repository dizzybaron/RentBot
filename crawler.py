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
# start crawler
soup = BeautifulSoup(browser.page_source, "lxml")
while len(soup.select('.pageNext')) > 0:
#    for price in soup.select('.price i'):
#        print(price.text)

#pending for resolution
#    for name in soup.select('h3 a'):
#        print(name.text)
    for address in soup.select('p.lightBox em'):
        print(address.text)

    time.sleep(random.randrange(1,5))
    browser.find_element_by_link_text(u"下一頁").click()
    soup = BeautifulSoup(browser.page_source, "lxml")
# close the browser
browser.close()
