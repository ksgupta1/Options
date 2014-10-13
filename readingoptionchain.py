# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 22:13:28 2014

@author: Kshitij Gupta
"""

# Writing the program to read the options data from website and store it in the table for analysis

import urllib2
from bs4 import BeautifulSoup
import requests

import warnings
import pandas as pd

#html_content = urllib2.urlopen("http://google.com")
#soup = BeautifulSoup(html_content)
#req = requests.get('http://nasdaq.com/markets/ipos')
req = requests.get('http://www.nasdaq.com/symbol/vxx/option-chain')
soup = BeautifulSoup(req.content)
results= soup.findAll('div', attrs={'class': 'OptionsChain-chart'})



if len(results) > 1:
    warnings.warn("check code: more than one option chain result found")
    
tables = results[0].findAll('table')

if len(tables) > 0:
    warnings.warn("check code: more than one option chain table found")

rows = tables[0].findAll('tr')

headers = rows[0].findAll('th')

# Adding some more columns to update the name of the options and the date columns
colNames = [u'Date',u'callID']
for iheaders in headers:
    colNames.append(iheaders.contents[0])

colNames.append(u'putID')
 

#df = pd.DataFrame(columns = colNames)

df = pd.DataFrame() # empty data frame no columns defined, will be added later by the dictionary 


iterrows = iter(rows)
next(iterrows)
for irows in iterrows:    
    dic = {}
    vals = irows.findAll('td')
    
    if not vals[0].findAll('a'):
        warnings.warn("check code: href location changed")
    if len(vals) is not 16:
        warnings.warn("check code: td number is not 16")
    
    aval = vals[0].findAll('a')
    urlsplit = aval[0]['href'].split("/")
    dic["callID"] = [urlsplit[-1]]                       
           
    dic["Calls"] = [vals[0].string]
    dic["Last_C"] = [vals[1].string]
    dic["Chg_C"] = [vals[2].string]
    dic["Bid_C"] = [vals[3].string]
    dic["Ask_C"] = [vals[4].string]
    dic["Vol_C"] = [vals[5].string]
    dic["Open Int_C"] = [vals[6].string]
    dic["Root"] = [vals[7].string]           
    dic["Strike"] = [vals[8].string]
   
   
    dic["Puts"] = [vals[9].string]
    dic["Last_P"] = [vals[10].string]
    dic["Chg_P"] = [vals[11].string]
    dic["Bid_P"] = [vals[12].string]
    dic["Ask_P"] = [vals[13].string]
    dic["Vol_P"] = [vals[14].string]
    dic["Open Int_P"] = [vals[15].string]
           
    aval = vals[9].findAll('a')
    urlsplit = aval[0]['href'].split("/")
    dic["putID"] = [urlsplit[-1]]
           
    dic["Date"] =        
    data = pd.DataFrame(dic)

    df = df.append(data)    
        
# Next Steps: add dates and spanids for other index searches and create a database for it and begin 
# and begin analysis