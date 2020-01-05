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

options = Options()
options.headless = True
options.add_argument('--log-level=3')

def link_springer_affiliation(url):
    
    name_affi_mapping={}

    driver = webdriver.Chrome(executable_path = r'E:\Softwares\chromedriver_win32\chromedriver.exe', options=options)
    driver.get(url)
    
    try:   

        time.sleep(4)
        #soup = BeautifulSoup(driver.page_source,'html.parser')
        #div = soup.find(class_ = 'authors')
        #for i in div.find_all('li'):
            #if i.text == 'Authors and affiliations':
                #print(i)
                #i.click()
        #element = driver.find_elements_by_css_selector('li a')
        #for a in element:
        #    if a.text=='Authors and affiliations':
        #        a.click()
        soup = BeautifulSoup(driver.page_source,'html.parser')

        name_key_map={}
        affi_key_map={}
       # piece = driver.find_element_by_xpath('/html/body/div[4]/main/div/div/article/div/div[1]/div[3]/div[2]/div/ol/li[1]/span[2]/span[2]')
        
        for data in soup.findAll(id='authorsandaffiliations'):
            
            for element in data.findAll(class_='u-mb-2'):
                name=""
                key_name=""
                for ele in element.find(class_='authors-affiliations__name'):
                    name = ele
                    name = name.replace(u'\xa0', u' ')
                for ele in element.find(class_='u-inline-list'):
                    key_name = (ele.text)
                name_key_map[name]=key_name
                 
            for element in data.find(class_='test-affiliations'):
                affi=""
                key_name=""
                for key in element.find(class_='affiliation__name'):
                    affi = key
                
                for key in element.find(class_='affiliation__count'):
                        key_name = key[0]
                        
                affi_key_map[key_name]=affi
           # print(affi_key_map)
           # print(name_key_map)

        for name,key in name_key_map.items():
            name_affi_mapping[name]=affi_key_map[key]
        #print(name_affi_mapping)

    except NoSuchElementException:
        pass

   

    
    references = []

    try:
        
        
        time.sleep(6)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        for data in soup.findAll(class_='BibliographyWrapper'):
            for element in data.findAll('li'):
                for tag in element.findAll(class_='CitationContent'):
                    var = (tag.text).replace(u'\xa0', u' ')
                    references.append(var)
                    #print(tag.text)
         
    except NoSuchElementException:
        pass
    driver.close()
    return name_affi_mapping,references 
        
