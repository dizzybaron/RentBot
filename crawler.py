
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.keys import Keys
# import time that will help our scraper wait
import time
# import beautiful sout
from bs4 import BeautifulSoup
import random
# display to help ubuntu 16.06, geckodriver 0.18.0 work together
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()

import pandas as pd

# crawler function
    
def crawler(browser):
    
    soup = BeautifulSoup(browser.page_source, "lxml")

    title = []
    web_url = []
    address = []
    price = []
    
    while len(soup.select('.pageNext')) > 0:
        print("loading another pg")
        
        name = soup.select('h3 a')
        title = title + [x.text for x in name]
        web_url = web_url+[x.get('href') for x in name]
        address = address + soup.select('p.lightBox em')
        price = price + soup.select('.price i')
        print(len(web_url))
        if len(web_url) > 10:
            # if we have enough number of results
            return(title, web_url, address, price)
            break
        else:
            try:
                # clicking next page
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                browser.find_element_by_class_name('pageNext').click()
                soup = BeautifulSoup(browser.page_source, "lxml")
            except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
                print("last page or only one page")
           

    return(title, web_url, address, price)
# click all params
def clicking(user_series):
    url = 'https://rent.591.com.tw/?'

    # choose the type
    type_to_span = {'不限': "0",
                    '整層住家': "1",
                    '獨立套房': "2",
                    '分租套房': "3",
                    '雅房': "4",}
    
    url = url + 'kind=' + type_to_span[user_series["housetype"]] + 'o'
    
    # choose the size
    
    size_to_span = {'不限': '0,0',
                    '10坪以下': "0,10",
                    '10~20坪': "10,20"}
    url = url + 'area=' + size_to_span[user_series['size']] + '&'

    # choose the floor
    floor_url = {'不限': '0,0',
                 '1層': '0,1',
                 '2-6層': '2,6',
                 '6-12層': '6,12',
                 '12層以上':'12,'}
    url = url + 'floor=' + floor_url[user_series['floor']]
    
    # choose the elevator
    options = []
    if user_series['elevator'] == '是':
        if user_series['cook'] == '是':
            url = url + '&other=cook,lift'
        else:
            url = url + '&other=lift'
    else:
        if user_series['cook'] == '是':
            url = url + '&other=cook'
    
    # add keyword
    url = url + '&keyword=' + user_series['keyword']

    # add rooftop
    if user_series['rooftop'] == '是':
        url = url + '&no_cover=1'

    # ad budegt
    if user_series['budgetMax'] != '我太有錢':
        url = url + '&rentprice=0,' + user_series['budgetMax']
        

    # open window and link to 591
    print("loading url", url, ' into browser Firefox')
    try:
        browser = webdriver.Firefox()
        browser.get(url)

        print('start to click')

        # close the advertisement window
        print(browser.find_element_by_id("area-box-close"))
        browser.find_element_by_id("area-box-close").click()
        browser.find_element_by_xpath("//div[@id='search-location']/span").click()
        browser.find_element_by_xpath("//div[@id='search-location']/span").click()

        # click city
        xpath = u"(//a[contains(text(),"+ user_series['city']+u")])[2]"
        browser.find_element_by_xpath(xpath).click()

        # click search
        browser.find_element_by_class_name("search-input-btn").click()
        print("finish clicking")

        # start crawler
        df = crawler(browser)
        return(df)

        #close the browser
        browser.quit()
    except WebDriverException:
        browser.quit()


