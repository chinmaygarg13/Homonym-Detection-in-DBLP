import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import time
import re

options = Options()
options.headless = True
options.add_argument('--log-level=3')

def acm_affiliation(url):
    
    name_affiliation = {}

    driver = webdriver.Chrome(executable_path = r'E:\Softwares\chromedriver_win32\chromedriver.exe', options=options)
    driver.get(url)

    references = []
    
    try:
        
         
        soup = BeautifulSoup(driver.page_source,'html.parser')

        name = []
        affi =  []
        for td in soup.findAll('td'):
            name_exist = ""
            aff_exist = ""
            for a in td.findAll('a',href=True):
               
                if a.get('title')=='Author Profile Page':
                    name_exist=a.text
                    name.append(a.text)
                if a.get('title')=='Institutional Profile Page':
                    aff_exist=a.text
                    affi.append(a.text)


        
        if len(affi)==0:

            for element in soup.findAll('table',class_='medium-text'):
                #print(element)
                for td in element.findAll('td',valign='bottom'):
                    var=(td.text).replace('\n','')
                    var = var.replace('\t','')
                    affi.append(var)

        for i,val in enumerate(name):
            if len(affi)>i:
                name_affiliation[name[i]]=affi[i]

        #print(name_affiliation)

        
        
    except (NoSuchElementException,IndexError) :
            pass

    

    try:
        
        time.sleep(6)
        element = driver.find_element_by_id('tab-1015-btnWrap')
        #print(element)
        element.click()
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source,'html.parser')
        for data in soup.findAll(id='cf_layoutareareferences'):
            for ele in data.findAll(class_='tabbody'):
                for tag in ele.findAll('tr'):
                    var  = (tag.text).replace('\n','')
                    var = var.replace(u'\xa0', u' ')
                    var.lstrip('0123456789 ')
                    references.append(var)
        #print(references)
    except NoSuchElementException:
        pass
    driver.close()
    return name_affiliation, references
