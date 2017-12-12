#import
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import random
import time
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()

# crawler function
def crawler():
    time.sleep(3)
    soup = BeautifulSoup(browser.page_source, "lxml")
    while len(soup.select('.pageNext')) > 0:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        for name in soup.select('h3 a'):
            print(name.text)
        for address in soup.select('p.lightBox em'):
            print(address.text)
        for price in soup.select('.price i'):
            print(price.text)
        if len(soup.select('.pageBar .last')) > 0:
            break
        browser.find_element_by_class_name('pageNext').click()
        time.sleep(random.randrange(5,10))
        soup = BeautifulSoup(browser.page_source, "lxml")

# open browser(Firefox)
browser = webdriver.Firefox()

# get to the target page
browser.get('https://rent.591.com.tw/?kind=0&region=1')
time.sleep(1)

# close the advertisement window
browser.find_element_by_id("area-box-close").click()

# choose city
def dis_city():
    print('選擇一個縣市：')
    print('北部：')
    print('1.台北市 / 2.新北市 / 3.桃園市 / 4.新竹市 / 5.新竹縣 / 6.宜蘭縣 / 7.基隆市')
    print('中部：')
    print('8.台中市 / 9.彰化縣 / 10.雲林縣 / 11.苗栗縣 / 12.南投縣')
    print('南部：')
    print('13. 高雄市 / 14.台南市 / 15.嘉義市 / 16.嘉義縣 / 17.屏東縣')
    print('東部：')
    print('18.台東縣 / 19.花蓮縣 / 20.澎湖縣 / 21.金門縣 / 22.連江縣')
dis_city()

city_choice = int(input("請輸入您的選擇(數字):"))
browser.find_element_by_xpath("//div[@id='search-location']/span").click()
time.sleep(2)
browser.find_element_by_xpath("//div[@id='search-location']/span").click()
if city_choice == 1:
    browser.find_element_by_xpath(u"(//a[contains(text(),'台北市')])[2]").click()
elif city_choice == 2:
    browser.find_element_by_xpath(u"(//a[contains(text(),'新北市')])[2]").click()
elif city_choice == 3:
    browser.find_element_by_xpath(u"(//a[contains(text(),'桃園市')])[2]").click()
elif city_choice == 4:
    browser.find_element_by_xpath(u"(//a[contains(text(),'新竹市')])[2]").click()
elif city_choice == 5:
    browser.find_element_by_xpath(u"(//a[contains(text(),'新竹縣')])[2]").click()
elif city_choice == 6:
    browser.find_element_by_xpath(u"(//a[contains(text(),'宜蘭縣')])[2]").click()
elif city_choice == 7:
    browser.find_element_by_xpath(u"(//a[contains(text(),'基隆市')])[2]").click()
elif city_choice == 8:
    browser.find_element_by_xpath(u"(//a[contains(text(),'台中市')])[2]").click()
elif city_choice == 9:
    browser.find_element_by_xpath(u"(//a[contains(text(),'彰化縣')])[2]").click()
elif city_choice == 10:
    browser.find_element_by_xpath(u"(//a[contains(text(),'雲林縣')])[2]").click()
elif city_choice == 11:
    browser.find_element_by_xpath(u"(//a[contains(text(),'苗栗縣')])[2]").click()
elif city_choice == 12:
    browser.find_element_by_xpath(u"(//a[contains(text(),'南投縣')])[2]").click()
elif city_choice == 13:
    browser.find_element_by_xpath(u"(//a[contains(text(),'高雄市')])[2]").click()
elif city_choice == 14:
    browser.find_element_by_xpath(u"(//a[contains(text(),'台南市')])[2]").click()
elif city_choice == 15:
    browser.find_element_by_xpath(u"(//a[contains(text(),'嘉義市')])[2]").click()
elif city_choice == 16:
    browser.find_element_by_xpath(u"(//a[contains(text(),'嘉義縣')])[2]").click()
elif city_choice == 17:
    browser.find_element_by_xpath(u"(//a[contains(text(),'屏東縣')])[2]").click()
elif city_choice == 18:
    browser.find_element_by_xpath(u"(//a[contains(text(),'台東縣')])[2]").click()
elif city_choice == 19:
    browser.find_element_by_xpath(u"(//a[contains(text(),'花蓮縣')])[2]").click()
elif city_choice == 20:
    browser.find_element_by_xpath(u"(//a[contains(text(),'澎湖縣')])[2]").click()
elif city_choice == 21:
    browser.find_element_by_xpath(u"(//a[contains(text(),'金門縣')])[2]").click()
elif city_choice == 22:
    browser.find_element_by_xpath(u"(//a[contains(text(),'連江縣')])[2]").click()
else:
    browser.find_element_by_xpath(u"(//a[contains(text(),'台北市')])[2]").click()
    print('你什麼都沒選，已預設為台北市')

# choose keyword
keyword_bar = browser.find_element_by_class_name('searchInput')
key_in_keyword_bar = str(input('請輸入關鍵字（社區、街道、商圈...）'))
keyword_bar.send_keys(key_in_keyword_bar)
browser.find_element_by_class_name("searchBtn").click()
time.sleep(3)
browser.find_element_by_class_name("searchBtn").click()

# Now use the filter to select ideal rental item
# choose the type
def disp_type():
    print('請輸入你想要的房型：')
    print('1. 整層住家')
    print('2. 獨立套房')
    print('3. 分租套房')
    print('4. 雅房')
disp_type()

type_choice = int(input("請輸入您的選擇(數字):"))
if type_choice == 1:
    browser.find_element_by_xpath("//div[@id='search-kind']/span[2]").click()
elif type_choice == 2:
    browser.find_element_by_xpath("//div[@id='search-kind']/span[3]").click()
elif type_choice == 3:
    browser.find_element_by_xpath("//div[@id='search-kind']/span[4]").click()
elif type_choice == 4:
    browser.find_element_by_xpath("//div[@id='search-kind']/span[5]").click()
else:
    browser.find_element_by_xpath("//div[@id='search-kind']/span").click()
# choose the size
def disp_size():
    print('請輸入你想要的坪數：')
    print('1. 10坪以下')
    print('2. 10~20坪')
disp_size()
size_choice = int(input("請輸入您的選擇(數字):"))
if size_choice == 1:
    browser.find_element_by_xpath("//div[@id='search-plain']/span[2]").click()
elif size_choice == 2:
    browser.find_element_by_xpath("//div[@id='search-plain']/span[3]").click()
else:
    browser.find_element_by_xpath("//div[@id='search-plain']/span").click()
# choose the floor
def disp_floor():
    print('請輸入你想要的樓層：')
    print('1. 1樓')
    print('2. 2~6樓')
    print('3. 6~12樓')
    print('4. 12樓以上')
disp_floor()
floor_choice = int(input("請輸入您的選擇(數字):"))
if floor_choice == 1:
    browser.find_element_by_xpath("(//button[@type='button'])[2]").click()
    browser.find_element_by_link_text(u"1層").click()
elif floor_choice == 2:
    browser.find_element_by_xpath("(//button[@type='button'])[2]").click()
    browser.find_element_by_link_text(u"2-6層").click()
elif floor_choice == 3:
    browser.find_element_by_xpath("(//button[@type='button'])[2]").click()
    browser.find_element_by_link_text(u"6-12層").click()
elif floor_choice == 4:
    browser.find_element_by_xpath("(//button[@type='button'])[2]").click()
    browser.find_element_by_link_text(u"12層以上").click()
else:
    browser.find_element_by_xpath("(//button[@type='button'])[2]").click()
    browser.find_element_by_link_text(u"不限").click()

# choose the elevator
def dis_elevator():
    print('是否要有電梯？')
    print('1. 是')
    print('2. 否')
dis_elevator()
elevator_choice = int(input("請輸入您的選擇(數字):"))
if elevator_choice == 1:
    browser.find_element_by_xpath("(//button[@type='button'])[5]").click()
    browser.find_element_by_xpath("//div[@id='rentOther']/ul/li[2]/a/label/em").click()
else:
    time.sleep(1)

# rule out rooftop add-ons
def dis_rooftop():
    print('是否要排除頂樓加蓋？')
    print('1. 是')
    print('2. 否')
dis_rooftop()
rooftop_choice = int(input("請輸入您的選擇(數字):"))
if rooftop_choice == 1:
    browser.find_element_by_xpath("//div[@id='container']/section[3]/section/div[6]/ul/li[2]/label").click()
else:
    time.sleep(1)

# choose cooking
def dis_cooking():
    print('是否需要開伙？')
    print('1. 需要')
    print('2. 不需要')
dis_cooking()
cooking_choice = int(input("請輸入您的選擇(數字):"))
if cooking_choice == 1:
    browser.find_element_by_xpath("(//button[@type='button'])[5]").click()
    browser.find_element_by_xpath("//div[@id='rentOther']/ul/li[4]/a/label/em").click()
else:
    time.sleep(1)

# choose the budget
custom_min_bar = browser.find_element_by_class_name('rentPrice-min')
key_in_custom_min_bar = str(input('請輸入預算下限'))
custom_min_bar.send_keys(key_in_custom_min_bar)
custom_max_bar = browser.find_element_by_class_name('rentPrice-max')
key_in_custom_max_bar = str(input('請輸入預算上限'))
custom_max_bar.send_keys(key_in_custom_max_bar)
browser.find_element_by_class_name("search-input-btn").click()

# start crawler
crawler()

#close the browser
browser.quit()
