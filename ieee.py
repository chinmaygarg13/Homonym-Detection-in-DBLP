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

def ieee_affiliation(url):
    
    author_affi_mapping={}
    driver = webdriver.Chrome(executable_path = r'E:\Softwares\chromedriver_win32\chromedriver.exe', options=options)
    driver.get(url)

    try:
      
        time.sleep(4)
        element = driver.find_element_by_id('authors-header')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        element.click()
        time.sleep(4)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        author=[]
        affiliation=[]
        combo=[]
         
        for data in soup.findAll(class_='authors-accordion-container'):
            #print(data)
            for ele in data.findAll(class_='col-24-24'):
                name = ""
                for tag in ele.findAll('a'):
                    name=(tag.text).replace('\n','')
                    var = name.replace('\t','')
                    author.append(var)
                for tag in ele.findAll('div'):
                    name=(tag.text).replace('\n','')
                    var = name.replace('\t','')
                    combo.append(var)
                    
        author,affiliation = combo[::2],combo[1::2]
        for idx,val in enumerate(author):
            author_affi_mapping[val]=affiliation[idx]

        #print(author_affi_mapping)

    except NoSuchElementException:
        pass
    
    references = []

    try:
        
        time.sleep(6)
        element = driver.find_element_by_id('references-header')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        
       
        #print(element)
        element.click()
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source,'html.parser') 
        for data in soup.findAll(id='references-section-container'):
            for ele in data.findAll(class_='reference-container'):
                var = (ele.text).replace('\n','')
                var = var.replace('\t','')
                var.lstrip('0123456789')
                references.append(var)
                
        
        #print(references)
    except NoSuchElementException:
        pass
    driver.close()
    return author_affi_mapping,references
#print(element)
     
     
