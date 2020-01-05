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
from acm import acm_affiliation
from science_direct import science_direct_affiliation
from ieee import ieee_affiliation
from link_springer import link_springer_affiliation

options = Options()
options.headless = True
options.add_argument('--log-level=3')

def affiliation_extracter(url):
        
    affiliation={}
    driver = webdriver.Chrome(executable_path = r'E:\Softwares\chromedriver_win32\chromedriver.exe', options=options)
    driver.get(url)
   # time.sleep(4)
    final_url = driver.current_url
    references=[]

    try:
        
        
        if final_url.find('acm')!=-1:
            affiliation,references = acm_affiliation(final_url)
            
            #print(affiliation)
            #print(references)

        if final_url.find('sciencedirect')!=-1:
            #print("science")
            affiliation,references = science_direct_affiliation(final_url)
             
           # print(affiliation)
           # print(references)

        if final_url.find('ieee')!=-1:       
            affiliation,references = ieee_affiliation(final_url)
            
            #print(affiliation)
            #print(references)

        if final_url.find('springer')!=-1:
            #print('springer')
            affiliation,references = link_springer_affiliation(final_url)
            
            #print(affiliation)
            #print(references)
            
    except NoSuchElementException:
        pass
    driver.close()
    return affiliation,references

#affiliation_extracter('https://link.springer.com/chapter/10.1007/11590316_83')
