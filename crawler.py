# import
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import urllib

# set destination
url = 'https://rent.591.com.tw/home/rent/index/r1s7k3.html?kind=1&region=1&section=7'

# request
req = urllib.request.Request(url,data=None,headers={'User-Agent': 'Mozilla/5.0'})

# now return the html
html = urllib.request.urlopen(req)

# find all links of the results, these are the rentals we are looking for
sp = BeautifulSoup(html, 'html.parser')

# name
for name in sp.select('h3 a'):
    print(name.text)

# price
for price in sp.select('.price i'):
    print(price.text)

# address
for address in sp.select('p.lightBox em'):
    print(address.text)

# size
#for size in sp.select('p.lightBox #text'):
#    print(size.text)
