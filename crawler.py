#import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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
    df = pd.DataFrame(columns = ["title", "address", "price", "url"]) # the dataframe to return all the results to user
    
    while len(soup.select('.pageNext')) > 0:
        print("loading another pg")
        page_data = pd.DataFrame(columns = ["title", "address", "price", "url"]) # each page generates a dataframe
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        i = 0
        for name in soup.select('h3 a'):
            page_data.loc[str(i), 'title']  = name.text # returning title of that house)
            i +=1
        i = 0
        for address in soup.select('p.lightBox em'):
            page_data.loc[str(i), 'address'] = address.text # returning address
            i +=1
        i = 0
        for price in soup.select('.price i'):
            page_data.loc[str(i), 'address'] = price.text # returning address 
            i += 1
        df = df.append(page_data)

        
        if len(soup.select('.pageBar .last')) > 0:
            break
        browser.find_element_by_class_name('pageNext').click()

        soup = BeautifulSoup(browser.page_source, "lxml")

    return(df)

    
# open browser(Firefox)


# get to the target page

# click all params
def clicking(user_series):
    url = 'https://rent.591.com.tw/?'

    # choose the type
    type_to_span = {'不限': "0",
                    '整層住家': "1",
                    '獨立套房': "2",
                    '分租套房': "3",
                    '雅房': "4",}
    
    url = url + 'kind=' + type_to_span[user_series["housetype"]] + '&region=1&'
    
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
    
    # open window and link to 591
    print("loading url", url, ' into browser Firefox')
    browser = webdriver.Firefox()
    browser.get(url)
    
    time.sleep(1)
    print('start to click')

    # close the advertisement window
    browser.find_element_by_id("area-box-close").click()
    
    
    browser.find_element_by_xpath("//div[@id='search-location']/span").click()
    time.sleep(2)
    browser.find_element_by_xpath("//div[@id='search-location']/span").click()

    # click city
    xpath = u"(//a[contains(text(),"+ user_series['city']+u")])[2]"
    browser.find_element_by_xpath(xpath).click()

    # choose keyword
    keyword_bar = browser.find_element_by_class_name('searchInput')
    keyword_bar.send_keys(user_series['keyword'])
    browser.find_element_by_class_name("searchBtn").click()
    time.sleep(3)
    browser.find_element_by_class_name("searchBtn").click()
    
    # rule out rooftop add-ons
    if user_series['rooftop'] == '是':
        browser.find_element_by_xpath("//div[@id='container']/section[3]/section/div[6]/ul/li[2]/label").click()

    time.sleep(1)

    
    # choose the budget
    if user_series['budgetMax'] != '我太有錢':
        custom_min_bar = browser.find_element_by_class_name('rentPrice-min')
        if type(user_series['budgetMin']) == str: 
            custom_min_bar.send_keys(user_series['budgetMin'])
        else:
            custom_min_bar.send_keys('0')
            
        custom_max_bar = browser.find_element_by_class_name('rentPrice-max')
        custom_max_bar.send_keys(user_series['budgetMax'])
        
            

    # click search
    browser.find_element_by_class_name("search-input-btn").click()
    print("finish")
    # start crawler
    df = crawler(browser)
    return(df)
    #close the browser
    browser.quit()

def quit_browser():
    browser.quit()
