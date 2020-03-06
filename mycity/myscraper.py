#!/usr/bin/env python3
#import os
import urllib
import json
#import facebook
import urllib.request
from bs4 import BeautifulSoup
import csv

import pandas as pd
import pandas_profiling

from pandas_profiling import ProfileReport
import numpy as np


with urllib.request.urlopen("https://inmuebles.mercadolibre.com.mx/casas/venta/saltillo%2C-coahuila") as url:
    s = url.read()
    print(type(s))
    

    soup = BeautifulSoup(s)
    print(type(soup))

    mercadolibreAll = soup.find_all("a")
    n=0
    for links in soup.find_all('a'):
        n=n+1
        #print (links.get('href'))
    
    
    print(n)
    
    
    
    # I'm guessing this would output the html source code ?
    #print(s)
    
 #Find the house prices   
    prices_soup=soup.find_all('div', class_='item__price') 
    print(type(prices_soup))
    n=0
    price=[]
    for myprice in prices_soup:
        price.append(myprice.get_text())
        n=n+1
        print (myprice.get_text())
        
    
    print(n)
    print(type(price))
    
 #Find the house area   
    area_soup=soup.find_all('div', class_='item__attrs') 
    print(type(area_soup))
    n=0
    area=[]
    for myarea in area_soup:
        area.append(myarea.get_text())
        n=n+1
        print (myarea.get_text())
        
    
    print(n)
    print(type(area))    
    
    #prices2=soup.find_all('div', class_='item__price').get_text()
    
    
    	
    # Create a zipped list of tuples from above lists
    zippedList =  list(zip(price, area))
    
    # Create a dataframe from zipped list
    df = pd.DataFrame(zippedList)#, columns = ['price' , 'area'], index=False) 
#
#    df = pd.DataFrame(columns=["price", "area"])
#    df["price"] = price
#    df["area"] = area

    df.to_csv("output.csv", index=False)   
    
    print(df.axes)

# Write Prices to csv file
#    with open('output.csv','wt') as result_file:
#        wr = csv.writer(result_file, dialect='excel')
#        wr.writerow(p1)
    
    #print(prices)
    
    #df = pd.read_csv('/Users/egetenmeyer/labpeers/mycity/output.csv')
    
    #df.describe()
    
    #prof = ProfileReport(df)
#    prof.to_file('output.html')