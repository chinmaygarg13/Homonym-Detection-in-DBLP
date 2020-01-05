from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd

import time
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

options = Options()
options.add_argument("--start-maximized")
options.add_argument('--log-level=3')
delay = 3

subjGroups = ['Algorithm', 'Database', 'Artificial intelligence', 'Distributed computing', 'Computer vision', 'Pattern recognition', 
            'Data mining', 'Information retrieval', 'Machine learning', 'Real-time computing', 'Computer network', 'Computer hardware', 'Computer architecture',
            'Programming language', 'Computer security', 'Web', 'Software engineering', 'Operating system', 'Parallel computing',
            'Speech recognition', 'Embedded system', 'Telecommunications', 'Knowledge management', 'Human-computer interaction', 'Human-computer', 'Multimedia'
            'Computer graphics (images)', 'Computer graphics','Natural language processing', 'Natural language', 'Computational science', 'Library science', 'Simulation', 'Computer engineering',
            'Theoretical computer science', 'Theoretical computer','Data science', 'Internet privacy']

website = "https://academic.microsoft.com/search?q="

def getSubjects(conf, type, title):
    subList = []
    subList2 = []
    subList3 = []
    if type == "conf":
        file = open("conference.txt", "r")
    elif type == "journal":
        file = open("journal.txt", "r")
    
    web2 = website + title
    driver2 =  webdriver.Chrome(executable_path = r'E:\Softwares\chromedriver_win32\chromedriver.exe', options=options)
    driver2.get(web2)

    for line in file:
        if conf in line:
            words = line.split(" > ")
            web = website + words[1]
            driver = webdriver.Chrome(executable_path = r'E:\Softwares\chromedriver_win32\chromedriver.exe', options=options)
            driver.get(web)

            try:
                #myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'main')))
                time.sleep(7)
                driver.save_screenshot("img.png")
                driver2.save_screenshot("img2.png")
                image = Image.open("img.png")
                image2 = Image.open("img2.png")
                w, h = image.size
                w = w/4
                image = image.crop((0, 0, w, h))
                image2 = image2.crop((0, 0, w, h))
                text = pytesseract.image_to_string(image, lang='eng')
                text2 = pytesseract.image_to_string(image2, lang='eng')
                #print(text)
                
                if "Top Topics" in text:
                    flag = 0
                    for lines in text.split('\n'):
                        if "Top Topics" in lines:
                            flag = 1
                        elif "Top Authors" in lines:
                            flag = 0
                            break
                        elif flag == 1:
                            #print(lines)
                            wordList = lines.split(" ")
                            if len(wordList) > 1:
                                for i in range(1, len(wordList)):
                                    if i >= len(wordList):
                                        break
                                    if wordList[i] == "":
                                        continue
                                    while len(wordList) > i and not wordList[i][0].isupper() and not wordList[i][0].isnumeric():
                                        wordList[i - 1] += (" " + wordList[i])
                                        wordList.pop(i)
                            
                            for item in wordList:
                                if item in subjGroups:
                                    if item == 'Theoretical computer':
                                        item = 'Theoretical computer science'
                                    elif item == 'Human-computer':
                                        item = 'Human-computer interaction'
                                    elif item == 'Computer graphics (images)':
                                        item = 'Computer graphics'
                                    elif item == 'Natural language':
                                        item = 'Natural language processing'
                                    subList.append(item)
                                elif len(item) > 0 and (item[0].isnumeric() or item[0].isupper()):
                                    if (item == 'World' or item == 'Wide' or item == 'MORE' or item == 'Computer science'
                                    or item == 'Computer engineering' or item == 'Engineering' or item == 'Information technology'):
                                        continue
                                    else:
                                        subList2.append(item)

                if "Top Topics" in text2:
                    flag = 0
                    for lines in text2.split('\n'):
                        if "Top Topics" in lines:
                            flag = 1
                        elif "Top Authors" in lines:
                            flag = 0
                            break
                        elif flag == 1:
                            #print(lines)
                            wordList = lines.split(" ")
                            if len(wordList) > 1:
                                for i in range(1, len(wordList)):
                                    if i >= len(wordList):
                                        break
                                    if wordList[i] == "":
                                        continue
                                    while len(wordList) > i and not wordList[i][0].isupper() and not wordList[i][0].isnumeric():
                                        wordList[i - 1] += (" " + wordList[i])
                                        wordList.pop(i)
                            
                            for item in wordList:
                                if len(item) > 0:
                                    if item == 'Theoretical computer':
                                        item = 'Theoretical computer science'
                                    elif item == 'Human-computer':
                                        item = 'Human-computer interaction'
                                    elif item == 'Computer graphics (images)':
                                        item = 'Computer graphics'
                                    elif item == 'Natural language':
                                        item = 'Natural language processing'
                                    elif len(item) > 0 and (item[0].isnumeric() or item[0].isupper()):
                                        if (item == 'World' or item == 'Wide' or item == 'MORE' or item == 'Computer science' 
                                        or item == 'Computer engineering' or item == 'Engineering' or item == 'Information technology'):
                                            continue
                                    subList3.append(item)
            except TimeoutException:
                print("Loading took too much time!")

            driver.close()
            driver2.close()
            subList_both = []
            subList_both.append(subList)
            subList_both.append(subList2)
            subList_both.append(subList3)
            #print(subList_both)
            return subList_both
    return ['']            

#getSubjects("ijbidm", "journal", "Discovery of web usage patterns using fuzzy mountain clustering.")