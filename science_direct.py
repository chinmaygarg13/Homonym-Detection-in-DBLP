from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common import keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

options = Options()
options.headless = True
options.add_argument('--log-level=3')

def science_direct_affiliation(url):

    author_affiliation_mapping = {}
    driver = webdriver.Chrome(executable_path = r'E:\Softwares\chromedriver_win32\chromedriver.exe', options=options)

    driver.get(url)

    #print('as')
   
    try:
        
        time.sleep(3)
        element = driver.find_element_by_css_selector('.show-hide-details.u-font-sans')
        element.click()
        time.sleep(6)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        author_affiliation_mapping = {}
        for data in soup.findAll(id='author-group'):
            author_count = 0
            affi_count = 0
            for ele in data.findAll(class_='author'):
                author_count += 1
            for ele in data.findAll(class_='affiliation'):
                affi_count += 1

            if author_count == affi_count and author_count == 1:
                author_name_temp = ""
                for ele in data.find(class_='author'):
                    
                    for name in ele.findAll(class_='text'):
                        author_name_temp += name.text+" "
                    author_name = author_name_temp[0:len(author_name_temp)-1]
                for ele in data.find(class_='affiliation'):
                    author_affiliation_mapping[author_name] = ele.text

                    
            elif author_count>1 and affi_count>1:
                author_key = {}
                affi_key = {}

                for ele in data.findAll(class_='author'):
                    author_name_temp = ""
                    for name in ele.findAll(class_='text'):
                        author_name_temp += name.text+" "
                    author_name = author_name_temp[0:len(author_name_temp)-1]  
                    key = ""
                    for ref in ele.find(class_='author-ref'):
                        key = ref.text
                        
                    author_key[author_name]=key
                    
             
                    
                for ele in data.findAll(class_='affiliation'):
                    key=""
                    affiliation=""
                    key = ele.text[0]
                    affiliation = ele.text[1:-1]
                    
                    affi_key[key]=affiliation
                #print(affi_key)

                for name,key in author_key.items():
                    author_affiliation_mapping[name]=affi_key[key]
                #print(author_affiliation_mapping)
                    
                        
            elif author_count>1 and affi_count==1:
                author_list=[]
                for ele in data.findAll(class_='author'):
                    author_name_temp = ""
                    for name in ele.findAll(class_='text'):
                        author_name_temp += name.text+" "
                    author_name = author_name_temp[0:len(author_name_temp)-1]
                    author_list.append(author_name)
                affi=""
                for ele in data.find(class_='affiliation'):
                    affi = ele.text

                for ele in author_list:
                    author_affiliation_mapping[ele]=affi
                
            #print(author_affiliation_mapping)

    except NoSuchElementException:
        pass

    references = []

    try:
       
           

        time.sleep(4)
        soup = BeautifulSoup(driver.page_source,'html.parser')

        for data in soup.findAll(class_='bibliography'):
            for element in data.findAll('dd'):
                references.append(element.text)
        #print(references)        
    except NoSuchElementException:
        pass

    

    
    driver.close()
    return author_affiliation_mapping,references
